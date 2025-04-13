from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OutputStyle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EXPANDED: _ClassVar[OutputStyle]
    COMPRESSED: _ClassVar[OutputStyle]

class Syntax(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SCSS: _ClassVar[Syntax]
    INDENTED: _ClassVar[Syntax]
    CSS: _ClassVar[Syntax]

class LogEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WARNING: _ClassVar[LogEventType]
    DEPRECATION_WARNING: _ClassVar[LogEventType]
    DEBUG: _ClassVar[LogEventType]

class ProtocolErrorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PARSE: _ClassVar[ProtocolErrorType]
    PARAMS: _ClassVar[ProtocolErrorType]
    INTERNAL: _ClassVar[ProtocolErrorType]

class ListSeparator(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    COMMA: _ClassVar[ListSeparator]
    SPACE: _ClassVar[ListSeparator]
    SLASH: _ClassVar[ListSeparator]
    UNDECIDED: _ClassVar[ListSeparator]

class SingletonValue(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRUE: _ClassVar[SingletonValue]
    FALSE: _ClassVar[SingletonValue]
    NULL: _ClassVar[SingletonValue]

class CalculationOperator(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PLUS: _ClassVar[CalculationOperator]
    MINUS: _ClassVar[CalculationOperator]
    TIMES: _ClassVar[CalculationOperator]
    DIVIDE: _ClassVar[CalculationOperator]
EXPANDED: OutputStyle
COMPRESSED: OutputStyle
SCSS: Syntax
INDENTED: Syntax
CSS: Syntax
WARNING: LogEventType
DEPRECATION_WARNING: LogEventType
DEBUG: LogEventType
PARSE: ProtocolErrorType
PARAMS: ProtocolErrorType
INTERNAL: ProtocolErrorType
COMMA: ListSeparator
SPACE: ListSeparator
SLASH: ListSeparator
UNDECIDED: ListSeparator
TRUE: SingletonValue
FALSE: SingletonValue
NULL: SingletonValue
PLUS: CalculationOperator
MINUS: CalculationOperator
TIMES: CalculationOperator
DIVIDE: CalculationOperator

class InboundMessage(_message.Message):
    __slots__ = ("compile_request", "canonicalize_response", "import_response", "file_import_response", "function_call_response", "version_request")
    class VersionRequest(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: int
        def __init__(self, id: _Optional[int] = ...) -> None: ...
    class CompileRequest(_message.Message):
        __slots__ = ("string", "path", "style", "source_map", "importers", "global_functions", "alert_color", "alert_ascii", "verbose", "quiet_deps", "source_map_include_sources", "charset", "silent", "fatal_deprecation", "silence_deprecation", "future_deprecation")
        class StringInput(_message.Message):
            __slots__ = ("source", "url", "syntax", "importer")
            SOURCE_FIELD_NUMBER: _ClassVar[int]
            URL_FIELD_NUMBER: _ClassVar[int]
            SYNTAX_FIELD_NUMBER: _ClassVar[int]
            IMPORTER_FIELD_NUMBER: _ClassVar[int]
            source: str
            url: str
            syntax: Syntax
            importer: InboundMessage.CompileRequest.Importer
            def __init__(self, source: _Optional[str] = ..., url: _Optional[str] = ..., syntax: _Optional[_Union[Syntax, str]] = ..., importer: _Optional[_Union[InboundMessage.CompileRequest.Importer, _Mapping]] = ...) -> None: ...
        class Importer(_message.Message):
            __slots__ = ("path", "importer_id", "file_importer_id", "node_package_importer", "non_canonical_scheme")
            PATH_FIELD_NUMBER: _ClassVar[int]
            IMPORTER_ID_FIELD_NUMBER: _ClassVar[int]
            FILE_IMPORTER_ID_FIELD_NUMBER: _ClassVar[int]
            NODE_PACKAGE_IMPORTER_FIELD_NUMBER: _ClassVar[int]
            NON_CANONICAL_SCHEME_FIELD_NUMBER: _ClassVar[int]
            path: str
            importer_id: int
            file_importer_id: int
            node_package_importer: NodePackageImporter
            non_canonical_scheme: _containers.RepeatedScalarFieldContainer[str]
            def __init__(self, path: _Optional[str] = ..., importer_id: _Optional[int] = ..., file_importer_id: _Optional[int] = ..., node_package_importer: _Optional[_Union[NodePackageImporter, _Mapping]] = ..., non_canonical_scheme: _Optional[_Iterable[str]] = ...) -> None: ...
        STRING_FIELD_NUMBER: _ClassVar[int]
        PATH_FIELD_NUMBER: _ClassVar[int]
        STYLE_FIELD_NUMBER: _ClassVar[int]
        SOURCE_MAP_FIELD_NUMBER: _ClassVar[int]
        IMPORTERS_FIELD_NUMBER: _ClassVar[int]
        GLOBAL_FUNCTIONS_FIELD_NUMBER: _ClassVar[int]
        ALERT_COLOR_FIELD_NUMBER: _ClassVar[int]
        ALERT_ASCII_FIELD_NUMBER: _ClassVar[int]
        VERBOSE_FIELD_NUMBER: _ClassVar[int]
        QUIET_DEPS_FIELD_NUMBER: _ClassVar[int]
        SOURCE_MAP_INCLUDE_SOURCES_FIELD_NUMBER: _ClassVar[int]
        CHARSET_FIELD_NUMBER: _ClassVar[int]
        SILENT_FIELD_NUMBER: _ClassVar[int]
        FATAL_DEPRECATION_FIELD_NUMBER: _ClassVar[int]
        SILENCE_DEPRECATION_FIELD_NUMBER: _ClassVar[int]
        FUTURE_DEPRECATION_FIELD_NUMBER: _ClassVar[int]
        string: InboundMessage.CompileRequest.StringInput
        path: str
        style: OutputStyle
        source_map: bool
        importers: _containers.RepeatedCompositeFieldContainer[InboundMessage.CompileRequest.Importer]
        global_functions: _containers.RepeatedScalarFieldContainer[str]
        alert_color: bool
        alert_ascii: bool
        verbose: bool
        quiet_deps: bool
        source_map_include_sources: bool
        charset: bool
        silent: bool
        fatal_deprecation: _containers.RepeatedScalarFieldContainer[str]
        silence_deprecation: _containers.RepeatedScalarFieldContainer[str]
        future_deprecation: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, string: _Optional[_Union[InboundMessage.CompileRequest.StringInput, _Mapping]] = ..., path: _Optional[str] = ..., style: _Optional[_Union[OutputStyle, str]] = ..., source_map: bool = ..., importers: _Optional[_Iterable[_Union[InboundMessage.CompileRequest.Importer, _Mapping]]] = ..., global_functions: _Optional[_Iterable[str]] = ..., alert_color: bool = ..., alert_ascii: bool = ..., verbose: bool = ..., quiet_deps: bool = ..., source_map_include_sources: bool = ..., charset: bool = ..., silent: bool = ..., fatal_deprecation: _Optional[_Iterable[str]] = ..., silence_deprecation: _Optional[_Iterable[str]] = ..., future_deprecation: _Optional[_Iterable[str]] = ...) -> None: ...
    class CanonicalizeResponse(_message.Message):
        __slots__ = ("id", "url", "error", "containing_url_unused")
        ID_FIELD_NUMBER: _ClassVar[int]
        URL_FIELD_NUMBER: _ClassVar[int]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        CONTAINING_URL_UNUSED_FIELD_NUMBER: _ClassVar[int]
        id: int
        url: str
        error: str
        containing_url_unused: bool
        def __init__(self, id: _Optional[int] = ..., url: _Optional[str] = ..., error: _Optional[str] = ..., containing_url_unused: bool = ...) -> None: ...
    class ImportResponse(_message.Message):
        __slots__ = ("id", "success", "error")
        class ImportSuccess(_message.Message):
            __slots__ = ("contents", "syntax", "source_map_url")
            CONTENTS_FIELD_NUMBER: _ClassVar[int]
            SYNTAX_FIELD_NUMBER: _ClassVar[int]
            SOURCE_MAP_URL_FIELD_NUMBER: _ClassVar[int]
            contents: str
            syntax: Syntax
            source_map_url: str
            def __init__(self, contents: _Optional[str] = ..., syntax: _Optional[_Union[Syntax, str]] = ..., source_map_url: _Optional[str] = ...) -> None: ...
        ID_FIELD_NUMBER: _ClassVar[int]
        SUCCESS_FIELD_NUMBER: _ClassVar[int]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        id: int
        success: InboundMessage.ImportResponse.ImportSuccess
        error: str
        def __init__(self, id: _Optional[int] = ..., success: _Optional[_Union[InboundMessage.ImportResponse.ImportSuccess, _Mapping]] = ..., error: _Optional[str] = ...) -> None: ...
    class FileImportResponse(_message.Message):
        __slots__ = ("id", "file_url", "error", "containing_url_unused")
        ID_FIELD_NUMBER: _ClassVar[int]
        FILE_URL_FIELD_NUMBER: _ClassVar[int]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        CONTAINING_URL_UNUSED_FIELD_NUMBER: _ClassVar[int]
        id: int
        file_url: str
        error: str
        containing_url_unused: bool
        def __init__(self, id: _Optional[int] = ..., file_url: _Optional[str] = ..., error: _Optional[str] = ..., containing_url_unused: bool = ...) -> None: ...
    class FunctionCallResponse(_message.Message):
        __slots__ = ("id", "success", "error", "accessed_argument_lists")
        ID_FIELD_NUMBER: _ClassVar[int]
        SUCCESS_FIELD_NUMBER: _ClassVar[int]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        ACCESSED_ARGUMENT_LISTS_FIELD_NUMBER: _ClassVar[int]
        id: int
        success: Value
        error: str
        accessed_argument_lists: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, id: _Optional[int] = ..., success: _Optional[_Union[Value, _Mapping]] = ..., error: _Optional[str] = ..., accessed_argument_lists: _Optional[_Iterable[int]] = ...) -> None: ...
    COMPILE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    CANONICALIZE_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    IMPORT_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    FILE_IMPORT_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_CALL_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    VERSION_REQUEST_FIELD_NUMBER: _ClassVar[int]
    compile_request: InboundMessage.CompileRequest
    canonicalize_response: InboundMessage.CanonicalizeResponse
    import_response: InboundMessage.ImportResponse
    file_import_response: InboundMessage.FileImportResponse
    function_call_response: InboundMessage.FunctionCallResponse
    version_request: InboundMessage.VersionRequest
    def __init__(self, compile_request: _Optional[_Union[InboundMessage.CompileRequest, _Mapping]] = ..., canonicalize_response: _Optional[_Union[InboundMessage.CanonicalizeResponse, _Mapping]] = ..., import_response: _Optional[_Union[InboundMessage.ImportResponse, _Mapping]] = ..., file_import_response: _Optional[_Union[InboundMessage.FileImportResponse, _Mapping]] = ..., function_call_response: _Optional[_Union[InboundMessage.FunctionCallResponse, _Mapping]] = ..., version_request: _Optional[_Union[InboundMessage.VersionRequest, _Mapping]] = ...) -> None: ...

class OutboundMessage(_message.Message):
    __slots__ = ("error", "compile_response", "log_event", "canonicalize_request", "import_request", "file_import_request", "function_call_request", "version_response")
    class VersionResponse(_message.Message):
        __slots__ = ("id", "protocol_version", "compiler_version", "implementation_version", "implementation_name")
        ID_FIELD_NUMBER: _ClassVar[int]
        PROTOCOL_VERSION_FIELD_NUMBER: _ClassVar[int]
        COMPILER_VERSION_FIELD_NUMBER: _ClassVar[int]
        IMPLEMENTATION_VERSION_FIELD_NUMBER: _ClassVar[int]
        IMPLEMENTATION_NAME_FIELD_NUMBER: _ClassVar[int]
        id: int
        protocol_version: str
        compiler_version: str
        implementation_version: str
        implementation_name: str
        def __init__(self, id: _Optional[int] = ..., protocol_version: _Optional[str] = ..., compiler_version: _Optional[str] = ..., implementation_version: _Optional[str] = ..., implementation_name: _Optional[str] = ...) -> None: ...
    class CompileResponse(_message.Message):
        __slots__ = ("success", "failure", "loaded_urls")
        class CompileSuccess(_message.Message):
            __slots__ = ("css", "source_map")
            CSS_FIELD_NUMBER: _ClassVar[int]
            SOURCE_MAP_FIELD_NUMBER: _ClassVar[int]
            css: str
            source_map: str
            def __init__(self, css: _Optional[str] = ..., source_map: _Optional[str] = ...) -> None: ...
        class CompileFailure(_message.Message):
            __slots__ = ("message", "span", "stack_trace", "formatted")
            MESSAGE_FIELD_NUMBER: _ClassVar[int]
            SPAN_FIELD_NUMBER: _ClassVar[int]
            STACK_TRACE_FIELD_NUMBER: _ClassVar[int]
            FORMATTED_FIELD_NUMBER: _ClassVar[int]
            message: str
            span: SourceSpan
            stack_trace: str
            formatted: str
            def __init__(self, message: _Optional[str] = ..., span: _Optional[_Union[SourceSpan, _Mapping]] = ..., stack_trace: _Optional[str] = ..., formatted: _Optional[str] = ...) -> None: ...
        SUCCESS_FIELD_NUMBER: _ClassVar[int]
        FAILURE_FIELD_NUMBER: _ClassVar[int]
        LOADED_URLS_FIELD_NUMBER: _ClassVar[int]
        success: OutboundMessage.CompileResponse.CompileSuccess
        failure: OutboundMessage.CompileResponse.CompileFailure
        loaded_urls: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, success: _Optional[_Union[OutboundMessage.CompileResponse.CompileSuccess, _Mapping]] = ..., failure: _Optional[_Union[OutboundMessage.CompileResponse.CompileFailure, _Mapping]] = ..., loaded_urls: _Optional[_Iterable[str]] = ...) -> None: ...
    class LogEvent(_message.Message):
        __slots__ = ("type", "message", "span", "stack_trace", "formatted", "deprecation_type")
        TYPE_FIELD_NUMBER: _ClassVar[int]
        MESSAGE_FIELD_NUMBER: _ClassVar[int]
        SPAN_FIELD_NUMBER: _ClassVar[int]
        STACK_TRACE_FIELD_NUMBER: _ClassVar[int]
        FORMATTED_FIELD_NUMBER: _ClassVar[int]
        DEPRECATION_TYPE_FIELD_NUMBER: _ClassVar[int]
        type: LogEventType
        message: str
        span: SourceSpan
        stack_trace: str
        formatted: str
        deprecation_type: str
        def __init__(self, type: _Optional[_Union[LogEventType, str]] = ..., message: _Optional[str] = ..., span: _Optional[_Union[SourceSpan, _Mapping]] = ..., stack_trace: _Optional[str] = ..., formatted: _Optional[str] = ..., deprecation_type: _Optional[str] = ...) -> None: ...
    class CanonicalizeRequest(_message.Message):
        __slots__ = ("id", "importer_id", "url", "from_import", "containing_url")
        ID_FIELD_NUMBER: _ClassVar[int]
        IMPORTER_ID_FIELD_NUMBER: _ClassVar[int]
        URL_FIELD_NUMBER: _ClassVar[int]
        FROM_IMPORT_FIELD_NUMBER: _ClassVar[int]
        CONTAINING_URL_FIELD_NUMBER: _ClassVar[int]
        id: int
        importer_id: int
        url: str
        from_import: bool
        containing_url: str
        def __init__(self, id: _Optional[int] = ..., importer_id: _Optional[int] = ..., url: _Optional[str] = ..., from_import: bool = ..., containing_url: _Optional[str] = ...) -> None: ...
    class ImportRequest(_message.Message):
        __slots__ = ("id", "importer_id", "url")
        ID_FIELD_NUMBER: _ClassVar[int]
        IMPORTER_ID_FIELD_NUMBER: _ClassVar[int]
        URL_FIELD_NUMBER: _ClassVar[int]
        id: int
        importer_id: int
        url: str
        def __init__(self, id: _Optional[int] = ..., importer_id: _Optional[int] = ..., url: _Optional[str] = ...) -> None: ...
    class FileImportRequest(_message.Message):
        __slots__ = ("id", "importer_id", "url", "from_import", "containing_url")
        ID_FIELD_NUMBER: _ClassVar[int]
        IMPORTER_ID_FIELD_NUMBER: _ClassVar[int]
        URL_FIELD_NUMBER: _ClassVar[int]
        FROM_IMPORT_FIELD_NUMBER: _ClassVar[int]
        CONTAINING_URL_FIELD_NUMBER: _ClassVar[int]
        id: int
        importer_id: int
        url: str
        from_import: bool
        containing_url: str
        def __init__(self, id: _Optional[int] = ..., importer_id: _Optional[int] = ..., url: _Optional[str] = ..., from_import: bool = ..., containing_url: _Optional[str] = ...) -> None: ...
    class FunctionCallRequest(_message.Message):
        __slots__ = ("id", "name", "function_id", "arguments")
        ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        FUNCTION_ID_FIELD_NUMBER: _ClassVar[int]
        ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
        id: int
        name: str
        function_id: int
        arguments: _containers.RepeatedCompositeFieldContainer[Value]
        def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., function_id: _Optional[int] = ..., arguments: _Optional[_Iterable[_Union[Value, _Mapping]]] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    COMPILE_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    LOG_EVENT_FIELD_NUMBER: _ClassVar[int]
    CANONICALIZE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    IMPORT_REQUEST_FIELD_NUMBER: _ClassVar[int]
    FILE_IMPORT_REQUEST_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_CALL_REQUEST_FIELD_NUMBER: _ClassVar[int]
    VERSION_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    error: ProtocolError
    compile_response: OutboundMessage.CompileResponse
    log_event: OutboundMessage.LogEvent
    canonicalize_request: OutboundMessage.CanonicalizeRequest
    import_request: OutboundMessage.ImportRequest
    file_import_request: OutboundMessage.FileImportRequest
    function_call_request: OutboundMessage.FunctionCallRequest
    version_response: OutboundMessage.VersionResponse
    def __init__(self, error: _Optional[_Union[ProtocolError, _Mapping]] = ..., compile_response: _Optional[_Union[OutboundMessage.CompileResponse, _Mapping]] = ..., log_event: _Optional[_Union[OutboundMessage.LogEvent, _Mapping]] = ..., canonicalize_request: _Optional[_Union[OutboundMessage.CanonicalizeRequest, _Mapping]] = ..., import_request: _Optional[_Union[OutboundMessage.ImportRequest, _Mapping]] = ..., file_import_request: _Optional[_Union[OutboundMessage.FileImportRequest, _Mapping]] = ..., function_call_request: _Optional[_Union[OutboundMessage.FunctionCallRequest, _Mapping]] = ..., version_response: _Optional[_Union[OutboundMessage.VersionResponse, _Mapping]] = ...) -> None: ...

class ProtocolError(_message.Message):
    __slots__ = ("type", "id", "message")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    type: ProtocolErrorType
    id: int
    message: str
    def __init__(self, type: _Optional[_Union[ProtocolErrorType, str]] = ..., id: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class SourceSpan(_message.Message):
    __slots__ = ("text", "start", "end", "url", "context")
    class SourceLocation(_message.Message):
        __slots__ = ("offset", "line", "column")
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        LINE_FIELD_NUMBER: _ClassVar[int]
        COLUMN_FIELD_NUMBER: _ClassVar[int]
        offset: int
        line: int
        column: int
        def __init__(self, offset: _Optional[int] = ..., line: _Optional[int] = ..., column: _Optional[int] = ...) -> None: ...
    TEXT_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    start: SourceSpan.SourceLocation
    end: SourceSpan.SourceLocation
    url: str
    context: str
    def __init__(self, text: _Optional[str] = ..., start: _Optional[_Union[SourceSpan.SourceLocation, _Mapping]] = ..., end: _Optional[_Union[SourceSpan.SourceLocation, _Mapping]] = ..., url: _Optional[str] = ..., context: _Optional[str] = ...) -> None: ...

class Value(_message.Message):
    __slots__ = ("string", "number", "list", "map", "singleton", "compiler_function", "host_function", "argument_list", "calculation", "compiler_mixin", "color")
    class String(_message.Message):
        __slots__ = ("text", "quoted")
        TEXT_FIELD_NUMBER: _ClassVar[int]
        QUOTED_FIELD_NUMBER: _ClassVar[int]
        text: str
        quoted: bool
        def __init__(self, text: _Optional[str] = ..., quoted: bool = ...) -> None: ...
    class Number(_message.Message):
        __slots__ = ("value", "numerators", "denominators")
        VALUE_FIELD_NUMBER: _ClassVar[int]
        NUMERATORS_FIELD_NUMBER: _ClassVar[int]
        DENOMINATORS_FIELD_NUMBER: _ClassVar[int]
        value: float
        numerators: _containers.RepeatedScalarFieldContainer[str]
        denominators: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, value: _Optional[float] = ..., numerators: _Optional[_Iterable[str]] = ..., denominators: _Optional[_Iterable[str]] = ...) -> None: ...
    class Color(_message.Message):
        __slots__ = ("space", "channel1", "channel2", "channel3", "alpha")
        SPACE_FIELD_NUMBER: _ClassVar[int]
        CHANNEL1_FIELD_NUMBER: _ClassVar[int]
        CHANNEL2_FIELD_NUMBER: _ClassVar[int]
        CHANNEL3_FIELD_NUMBER: _ClassVar[int]
        ALPHA_FIELD_NUMBER: _ClassVar[int]
        space: str
        channel1: float
        channel2: float
        channel3: float
        alpha: float
        def __init__(self, space: _Optional[str] = ..., channel1: _Optional[float] = ..., channel2: _Optional[float] = ..., channel3: _Optional[float] = ..., alpha: _Optional[float] = ...) -> None: ...
    class List(_message.Message):
        __slots__ = ("separator", "has_brackets", "contents")
        SEPARATOR_FIELD_NUMBER: _ClassVar[int]
        HAS_BRACKETS_FIELD_NUMBER: _ClassVar[int]
        CONTENTS_FIELD_NUMBER: _ClassVar[int]
        separator: ListSeparator
        has_brackets: bool
        contents: _containers.RepeatedCompositeFieldContainer[Value]
        def __init__(self, separator: _Optional[_Union[ListSeparator, str]] = ..., has_brackets: bool = ..., contents: _Optional[_Iterable[_Union[Value, _Mapping]]] = ...) -> None: ...
    class Map(_message.Message):
        __slots__ = ("entries",)
        class Entry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: Value
            value: Value
            def __init__(self, key: _Optional[_Union[Value, _Mapping]] = ..., value: _Optional[_Union[Value, _Mapping]] = ...) -> None: ...
        ENTRIES_FIELD_NUMBER: _ClassVar[int]
        entries: _containers.RepeatedCompositeFieldContainer[Value.Map.Entry]
        def __init__(self, entries: _Optional[_Iterable[_Union[Value.Map.Entry, _Mapping]]] = ...) -> None: ...
    class CompilerFunction(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: int
        def __init__(self, id: _Optional[int] = ...) -> None: ...
    class HostFunction(_message.Message):
        __slots__ = ("id", "signature")
        ID_FIELD_NUMBER: _ClassVar[int]
        SIGNATURE_FIELD_NUMBER: _ClassVar[int]
        id: int
        signature: str
        def __init__(self, id: _Optional[int] = ..., signature: _Optional[str] = ...) -> None: ...
    class CompilerMixin(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: int
        def __init__(self, id: _Optional[int] = ...) -> None: ...
    class ArgumentList(_message.Message):
        __slots__ = ("id", "separator", "contents", "keywords")
        class KeywordsEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: Value
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Value, _Mapping]] = ...) -> None: ...
        ID_FIELD_NUMBER: _ClassVar[int]
        SEPARATOR_FIELD_NUMBER: _ClassVar[int]
        CONTENTS_FIELD_NUMBER: _ClassVar[int]
        KEYWORDS_FIELD_NUMBER: _ClassVar[int]
        id: int
        separator: ListSeparator
        contents: _containers.RepeatedCompositeFieldContainer[Value]
        keywords: _containers.MessageMap[str, Value]
        def __init__(self, id: _Optional[int] = ..., separator: _Optional[_Union[ListSeparator, str]] = ..., contents: _Optional[_Iterable[_Union[Value, _Mapping]]] = ..., keywords: _Optional[_Mapping[str, Value]] = ...) -> None: ...
    class Calculation(_message.Message):
        __slots__ = ("name", "arguments")
        class CalculationValue(_message.Message):
            __slots__ = ("number", "string", "interpolation", "operation", "calculation")
            NUMBER_FIELD_NUMBER: _ClassVar[int]
            STRING_FIELD_NUMBER: _ClassVar[int]
            INTERPOLATION_FIELD_NUMBER: _ClassVar[int]
            OPERATION_FIELD_NUMBER: _ClassVar[int]
            CALCULATION_FIELD_NUMBER: _ClassVar[int]
            number: Value.Number
            string: str
            interpolation: str
            operation: Value.Calculation.CalculationOperation
            calculation: Value.Calculation
            def __init__(self, number: _Optional[_Union[Value.Number, _Mapping]] = ..., string: _Optional[str] = ..., interpolation: _Optional[str] = ..., operation: _Optional[_Union[Value.Calculation.CalculationOperation, _Mapping]] = ..., calculation: _Optional[_Union[Value.Calculation, _Mapping]] = ...) -> None: ...
        class CalculationOperation(_message.Message):
            __slots__ = ("operator", "left", "right")
            OPERATOR_FIELD_NUMBER: _ClassVar[int]
            LEFT_FIELD_NUMBER: _ClassVar[int]
            RIGHT_FIELD_NUMBER: _ClassVar[int]
            operator: CalculationOperator
            left: Value.Calculation.CalculationValue
            right: Value.Calculation.CalculationValue
            def __init__(self, operator: _Optional[_Union[CalculationOperator, str]] = ..., left: _Optional[_Union[Value.Calculation.CalculationValue, _Mapping]] = ..., right: _Optional[_Union[Value.Calculation.CalculationValue, _Mapping]] = ...) -> None: ...
        NAME_FIELD_NUMBER: _ClassVar[int]
        ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
        name: str
        arguments: _containers.RepeatedCompositeFieldContainer[Value.Calculation.CalculationValue]
        def __init__(self, name: _Optional[str] = ..., arguments: _Optional[_Iterable[_Union[Value.Calculation.CalculationValue, _Mapping]]] = ...) -> None: ...
    STRING_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    LIST_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    SINGLETON_FIELD_NUMBER: _ClassVar[int]
    COMPILER_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    HOST_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    ARGUMENT_LIST_FIELD_NUMBER: _ClassVar[int]
    CALCULATION_FIELD_NUMBER: _ClassVar[int]
    COMPILER_MIXIN_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    string: Value.String
    number: Value.Number
    list: Value.List
    map: Value.Map
    singleton: SingletonValue
    compiler_function: Value.CompilerFunction
    host_function: Value.HostFunction
    argument_list: Value.ArgumentList
    calculation: Value.Calculation
    compiler_mixin: Value.CompilerMixin
    color: Value.Color
    def __init__(self, string: _Optional[_Union[Value.String, _Mapping]] = ..., number: _Optional[_Union[Value.Number, _Mapping]] = ..., list: _Optional[_Union[Value.List, _Mapping]] = ..., map: _Optional[_Union[Value.Map, _Mapping]] = ..., singleton: _Optional[_Union[SingletonValue, str]] = ..., compiler_function: _Optional[_Union[Value.CompilerFunction, _Mapping]] = ..., host_function: _Optional[_Union[Value.HostFunction, _Mapping]] = ..., argument_list: _Optional[_Union[Value.ArgumentList, _Mapping]] = ..., calculation: _Optional[_Union[Value.Calculation, _Mapping]] = ..., compiler_mixin: _Optional[_Union[Value.CompilerMixin, _Mapping]] = ..., color: _Optional[_Union[Value.Color, _Mapping]] = ...) -> None: ...

class NodePackageImporter(_message.Message):
    __slots__ = ("entry_point_directory",)
    ENTRY_POINT_DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    entry_point_directory: str
    def __init__(self, entry_point_directory: _Optional[str] = ...) -> None: ...
