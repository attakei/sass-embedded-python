import inspect
from collections.abc import Sequence


def value_to_python(value):
    """Convert Sass Value protobuf to Python type."""
    from .embedded_sass_pb2 import SingletonValue
    
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

    __slots__ = 'name', 'arguments', 'callable_'

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
        self.callable_ = callable_

    @property
    def signature(self):
        """Signature string of the function."""
        return '{}({})'.format(self.name, ', '.join(self.arguments))

    def __call__(self, *args, **kwargs):
        return self.callable_(*args, **kwargs)

    def __str__(self):
        return self.signature