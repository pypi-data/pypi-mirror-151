"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _LoggedDataType:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _LoggedDataTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_LoggedDataType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    LOGGED_DATA_TYPE_INVALID: _LoggedDataType.ValueType  # 0
    LOGGED_DATA_TYPE_TEXT: _LoggedDataType.ValueType  # 1
    LOGGED_DATA_TYPE_TABLE: _LoggedDataType.ValueType  # 2
    LOGGED_DATA_TYPE_BLOB: _LoggedDataType.ValueType  # 3
    LOGGED_DATA_TYPE_NUMBER: _LoggedDataType.ValueType  # 4
    LOGGED_DATA_TYPE_BOOLEAN: _LoggedDataType.ValueType  # 5
class LoggedDataType(_LoggedDataType, metaclass=_LoggedDataTypeEnumTypeWrapper):
    pass

LOGGED_DATA_TYPE_INVALID: LoggedDataType.ValueType  # 0
LOGGED_DATA_TYPE_TEXT: LoggedDataType.ValueType  # 1
LOGGED_DATA_TYPE_TABLE: LoggedDataType.ValueType  # 2
LOGGED_DATA_TYPE_BLOB: LoggedDataType.ValueType  # 3
LOGGED_DATA_TYPE_NUMBER: LoggedDataType.ValueType  # 4
LOGGED_DATA_TYPE_BOOLEAN: LoggedDataType.ValueType  # 5
global___LoggedDataType = LoggedDataType

