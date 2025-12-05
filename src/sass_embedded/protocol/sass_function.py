import inspect
from collections.abc import Sequence

from .embedded_sass_pb2 import SingletonValue, Value, ListSeparator



def value_to_python(value):
    """Convert Sass Value protobuf to Python type."""
    
    which = value.WhichOneof('value')
    if which == 'string':
        return value.string.text
    elif which == 'number':
        return value.number.value
    elif which == 'singleton':
        # singleton is an enum: TRUE=0, FALSE=1, NULL=2
        if value.singleton == SingletonValue.TRUE:
            return True
        elif value.singleton == SingletonValue.FALSE:
            return False
        else:  # NULL
            return None
    elif which == 'list':
        return [value_to_python(v) for v in value.list.contents]
    elif which == 'map':
        return {value_to_python(e.key): value_to_python(e.value) for e in value.map.entries}
    elif which == 'color':
        # Return color as hex string for simplicity
        c = value.color
        if c.space == 'rgb':
            return f"#{int(c.channel1):02x}{int(c.channel2):02x}{int(c.channel3):02x}"
        return value  # Return as-is if not RGB
    else:
        return value  # Return protobuf object for unsupported types
    
class SassString():
    """Sass String wrapper for custom functions."""

    def __init__(self, text, quoted=False):
        self.text = text
        self.quoted = quoted

    def __init__(self, value: Value):
        if value.WhichOneof('value') != 'string':
            raise TypeError('Value is not a string')
        self.text = value.string.text
        self.quoted = value.string.quoted
    
    def to_value(self):
        """Convert to Sass Value protobuf."""

        value = Value()

        value.string.text = str(self)
        value.string.quoted = False

        return value
    
    def __str__(self):
        return self.text if not self.quoted else f'"{self.text}"'
    
class SassNumber():
    """Sass Number wrapper for custom functions."""

    def __init__(self, value: Value):
        if value.WhichOneof('value') != 'number':
            raise TypeError('Value is not a number')
        self.value = value.number.value
        self.numerators = list(value.number.numerators)
        self.denominators = list(value.number.denominators)

    def __init__(self, value: float, numerators: Sequence[str] = (), denominators: Sequence[str] = ()):
        self.value = value
        self.numerators = list(numerators)
        self.denominators = list(denominators)
    
    def to_value(self):
        """Convert to Sass Value protobuf."""

        value = Value()

        value.number.value = self.value
        if self.numerators:
            value.number.numerators.extend(self.numerators)
        if self.denominators:
            value.number.denominators.extend(self.denominators)

        return value
    
    def __float__(self):
        return float(self.value)
    
    def __int__(self):
        return int(self.value)
    
class SassColor():
    """Sass Color wrapper for custom functions."""

    def __init__(self, value: Value):
        if value.WhichOneof('value') != 'color':
            raise TypeError('Value is not a color')
        self.space = value.color.space
        self.channel1 = value.color.channel1
        self.channel2 = value.color.channel2
        self.channel3 = value.color.channel3
        self.alpha = value.color.alpha

    def __init__(self, space: str, channel1: float, channel2: float, channel3: float, alpha: float = 1.0):
        self.space = space
        self.channel1 = channel1
        self.channel2 = channel2
        self.channel3 = channel3
        self.alpha = alpha
    
    def to_value(self):
        """Convert to Sass Value protobuf."""

        value = Value()

        value.color.space = self.space
        value.color.channel1 = self.channel1
        value.color.channel2 = self.channel2
        value.color.channel3 = self.channel3
        value.color.alpha = self.alpha

        return value
    
class SassList():
    """Sass List wrapper for custom functions."""

    def __init__(self, value: Value):
        if value.WhichOneof('value') != 'list':
            raise TypeError('Value is not a list')
        self.contents = [value_to_python(v) for v in value.list.contents]
        self.separator = value.list.separator
        self.has_brackets = value.list.has_brackets

    def __init__(self, contents: Sequence, separator: ListSeparator = ListSeparator.COMMA, bracketed: bool = False):
        self.contents = list(contents)
        self.separator = separator
        self.has_brackets = bracketed
    
    def to_value(self):
        """Convert to Sass Value protobuf."""

        value = Value()

        value.list.separator = self.separator
        value.list.has_brackets = self.has_brackets
        for item in self.contents:
            v = Value()
            # Assuming item is already a Value protobuf or convertible
            if isinstance(item, Value):
                v.CopyFrom(item)
            else:
                # Simple conversion for basic types
                if isinstance(item, str):
                    v.string.text = item
                elif isinstance(item, (int, float)):
                    v.number.value = float(item)
                elif isinstance(item, bool):
                    v.singleton = SingletonValue.TRUE if item else SingletonValue.FALSE
                else:
                    raise TypeError(f'Unsupported list item type: {type(item)}')
            value.list.contents.append(v)

        return value
    
class SassMap():
    """Sass Map wrapper for custom functions."""

    def __init__(self, value: Value):
        if value.WhichOneof('value') != 'map':
            raise TypeError('Value is not a map')
        self.entries = {
            value_to_python(e.key): value_to_python(e.value)
            for e in value.map.entries
        }

    def __init__(self, entries: dict):
        self.entries = dict(entries)
    
    def to_value(self):
        """Convert to Sass Value protobuf."""

        value = Value()

        for k, v in self.entries.items():
            entry = value.map.entries.add()
            # Assuming k and v are already Value protobufs or convertible
            if isinstance(k, Value):
                entry.key.CopyFrom(k)
            else:
                if isinstance(k, str):
                    entry.key.string.text = k
                elif isinstance(k, (int, float)):
                    entry.key.number.value = float(k)
                elif isinstance(k, bool):
                    entry.key.singleton = SingletonValue.TRUE if k else SingletonValue.FALSE
                else:
                    raise TypeError(f'Unsupported map key type: {type(k)}')
            if isinstance(v, Value):
                entry.value.CopyFrom(v)
            else:
                if isinstance(v, str):
                    entry.value.string.text = v
                elif isinstance(v, (int, float)):
                    entry.value.number.value = float(v)
                elif isinstance(v, bool):
                    entry.value.singleton = SingletonValue.TRUE if v else SingletonValue.FALSE
                else:
                    raise TypeError(f'Unsupported map value type: {type(v)}')

        return value
    
class SassValue:
    """Generic Sass Value wrapper for custom functions."""

    def __init__(self, value: Value):
        self.value = value
    
    def to_value(self):
        """Convert to Sass Value protobuf."""
        return self.value
    
    def to_python(self):
        """Convert to Python type."""
        return value_to_python(self.value)

class SassFunction:
    """Custom function for Sass.  It can be instantiated using
    :meth:`from_lambda()` and :meth:`from_named_function()` as well.

    :param name: the function name
    :type name: :class:`str`
    :param arguments: the argument names
    :type arguments: :class:`collections.abc.Sequence`
    :param callable_: the actual function to be called
    :type callable_: :class:`collections.abc.Callable`

    .. versionadded:: 0.7.0

    """

    __slots__ = 'name', 'arguments', 'callable_', '_original_callable'

    @classmethod
    def from_lambda(cls, name, lambda_):
        """Make a :class:`SassFunction` object from the given ``lambda_``
        function.  Since lambda functions don't have their name, it need
        its ``name`` as well.  Arguments are automatically inspected.

        :param name: the function name
        :type name: :class:`str`
        :param lambda_: the actual lambda function to be called
        :type lambda_: :class:`types.LambdaType`
        :returns: a custom function wrapper of the ``lambda_`` function
        :rtype: :class:`SassFunction`

        """
        a = inspect.getfullargspec(lambda_)
        varargs, varkw, defaults, kwonlyargs = (
            a.varargs, a.varkw, a.defaults, a.kwonlyargs,
        )

        if varargs or varkw or defaults or kwonlyargs:
            raise TypeError(
                'functions cannot have starargs or defaults: {} {}'.format(
                    name, lambda_,
                ),
            )
        return cls(name, a.args, lambda_)

    @classmethod
    def from_named_function(cls, function):
        """Make a :class:`SassFunction` object from the named ``function``.
        Function name and arguments are automatically inspected.

        :param function: the named function to be called
        :type function: :class:`types.FunctionType`
        :returns: a custom function wrapper of the ``function``
        :rtype: :class:`SassFunction`

        """
        if not getattr(function, '__name__', ''):
            raise TypeError('function must be named')
        return cls.from_lambda(function.__name__, function)

    def __init__(self, name, arguments, callable_):
        if not isinstance(name, str):
            raise TypeError('name must be a string, not ' + repr(name))
        elif not isinstance(arguments, Sequence):
            raise TypeError(
                'arguments must be a sequence, not ' +
                repr(arguments),
            )
        elif not callable(callable_):
            raise TypeError(repr(callable_) + ' is not callable')
        self.name = name
        self.arguments = tuple(
            arg if arg.startswith('$') else '$' + arg
            for arg in arguments
        )
        # Wrap the callable to handle protobuf arguments
        self._original_callable = callable_
        self.callable_ = self._make_wrapper(callable_)

    def _make_wrapper(self, func):
        """Create a wrapper that converts protobuf arguments to Python types."""
        def wrapper(protobuf_args):
            # Convert protobuf Value objects to Python types
            python_args = [value_to_python(arg) for arg in protobuf_args]
            # Call the original function with converted args
            result = func(*python_args)
            # Convert result back to protobuf Value
            return self._python_to_value(result)
        return wrapper

    def _python_to_value(self, py_value):
        """Convert Python value to Sass Value protobuf."""
        from .embedded_sass_pb2 import Value, SingletonValue
        
        value = Value()
        if isinstance(py_value, bool):
            value.singleton = SingletonValue.TRUE if py_value else SingletonValue.FALSE
        elif py_value is None:
            value.singleton = SingletonValue.NULL
        elif isinstance(py_value, str):
            value.string.text = py_value
        elif isinstance(py_value, (int, float)):
            value.number.value = float(py_value)
        elif isinstance(py_value, list):
            for item in py_value:
                value.list.contents.append(self._python_to_value(item))
        elif isinstance(py_value, dict):
            for k, v in py_value.items():
                entry = value.map.entries.add()
                entry.key.CopyFrom(self._python_to_value(k))
                entry.value.CopyFrom(self._python_to_value(v))
        else:
            raise TypeError(f"Unsupported return type: {type(py_value)}")
        return value

    @property
    def signature(self):
        """Signature string of the function."""
        return '{}({})'.format(self.name, ', '.join(self.arguments))

    def __call__(self, *args, **kwargs):
        return self.callable_(*args, **kwargs)

    def __str__(self):
        return self.signature