import inspect
from typing import get_type_hints
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

class SassBoolean():
    """Sass Boolean wrapper for custom functions."""

    def __init__(self, value):
        if isinstance(value, Value):
            if value.WhichOneof('value') != 'singleton':
                raise TypeError('Value is not a singleton')
            if value.singleton == SingletonValue.TRUE:
                self.value = True
            elif value.singleton == SingletonValue.FALSE:
                self.value = False
            else:
                raise TypeError('Value is not a boolean singleton')
        else:
            self.value = bool(value)
    
    def to_value(self):
        """Convert to Sass Value protobuf."""

        value = Value()

        value.singleton = SingletonValue.TRUE if self.value else SingletonValue.FALSE

        return value
    
    def __bool__(self):
        return self.value
        
class SassString():
    """Sass String wrapper for custom functions."""

    def __init__(self, text_or_value, quoted=False):
        if isinstance(text_or_value, Value):
            if text_or_value.WhichOneof('value') != 'string':
                raise TypeError('Value is not a string')
            self.text = text_or_value.string.text
            self.quoted = text_or_value.string.quoted
        else:
            self.text = text_or_value
            self.quoted = quoted
    
    def to_value(self):
        """Convert to Sass Value protobuf."""

        value = Value()

        value.string.text = str(self)
        value.string.quoted = False

        return value
    
    def __str__(self):
        return self.text if not self.quoted else f'"{self.text}"'

    def __eq__(self, other):
        if isinstance(other, SassString):
            return self.text == other.text
        if isinstance(other, str):
            return self.text == other.strip('"\'')
        return False

    def __hash__(self):  # allow use as dict key
        return hash(self.text)
    
class SassNumber():
    """Sass Number wrapper for custom functions."""

    def __init__(self, value, numerators: Sequence[str] = (), denominators: Sequence[str] = ()):
        if isinstance(value, Value):
            if value.WhichOneof('value') != 'number':
                raise TypeError('Value is not a number')
            self.value = value.number.value
            self.numerators = list(value.number.numerators)
            self.denominators = list(value.number.denominators)
        else:
            self.value = float(value)
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

    def __init__(self, value_or_space, channel1=None, channel2=None, channel3=None, alpha=1.0):
        if isinstance(value_or_space, Value):
            if value_or_space.WhichOneof('value') != 'color':
                raise TypeError('Value is not a color')
            self.space = value_or_space.color.space
            self.channel1 = value_or_space.color.channel1
            self.channel2 = value_or_space.color.channel2
            self.channel3 = value_or_space.color.channel3
            self.alpha = value_or_space.color.alpha
        else:
            # Allow hex string like "#rrggbb"
            if isinstance(value_or_space, str) and channel1 is None and channel2 is None and channel3 is None:
                hex_str = value_or_space.lstrip('#')
                if len(hex_str) == 6:
                    self.space = 'rgb'
                    self.channel1 = int(hex_str[0:2], 16)
                    self.channel2 = int(hex_str[2:4], 16)
                    self.channel3 = int(hex_str[4:6], 16)
                    self.alpha = alpha
                    return
                else:
                    raise TypeError('Hex color must be in #RRGGBB format')

            if channel1 is None or channel2 is None or channel3 is None:
                raise TypeError('channel1, channel2, and channel3 are required when creating from values')
            self.space = value_or_space
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

    def __init__(self, contents_or_value, separator: ListSeparator = ListSeparator.COMMA, bracketed: bool = False):
        if isinstance(contents_or_value, Value):
            if contents_or_value.WhichOneof('value') != 'list':
                raise TypeError('Value is not a list')
            self.contents = [value_to_python(v) for v in contents_or_value.list.contents]
            self.separator = contents_or_value.list.separator
            self.has_brackets = contents_or_value.list.has_brackets
        else:
            self.contents = list(contents_or_value)
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

    def __init__(self, entries_or_value):
        if isinstance(entries_or_value, Value):
            if entries_or_value.WhichOneof('value') != 'map':
                raise TypeError('Value is not a map')
            self.entries = {
                value_to_python(e.key): value_to_python(e.value)
                for e in entries_or_value.map.entries
            }
        else:
            self.entries = dict(entries_or_value)
    
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
        """Create a wrapper that converts protobuf arguments to Python types.

        Conversion is guided by the function's type hints when available.
        """
        hints = get_type_hints(func)
        params = list(inspect.signature(func).parameters.values())

        def wrapper(protobuf_args):
            python_args = []
            for i, arg in enumerate(protobuf_args):
                target_type = hints.get(params[i].name) if i < len(params) else None

                if target_type is Value:
                    python_args.append(arg)
                elif target_type is SassString:
                    python_args.append(SassString(arg))
                elif target_type is SassNumber:
                    python_args.append(SassNumber(arg))
                elif target_type is SassColor:
                    python_args.append(SassColor(arg))
                elif target_type is SassList:
                    python_args.append(SassList(arg))
                elif target_type is SassMap:
                    python_args.append(SassMap(arg))
                else:
                    python_args.append(value_to_python(arg))

            result = func(*python_args)
            return self._python_to_value(result)

        return wrapper

    def _python_to_value(self, py_value):
        """Convert Python value to Sass Value protobuf."""
        from .embedded_sass_pb2 import Value, SingletonValue
        
        # Check if it's already a Sass wrapper class
        if hasattr(py_value, 'to_value') and callable(py_value.to_value):
            return py_value.to_value()
        
        # Allow raw protobuf Value to pass through untouched
        if isinstance(py_value, Value):
            return py_value

        # Otherwise convert based on Python type
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