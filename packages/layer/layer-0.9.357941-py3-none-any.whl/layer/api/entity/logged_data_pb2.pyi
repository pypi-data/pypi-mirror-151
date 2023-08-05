"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import layer.api.value.logged_data_type_pb2
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import google.protobuf.timestamp_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class LoggedData(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    UNIQUE_TAG_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    CREATED_TIME_FIELD_NUMBER: builtins.int
    UPDATED_TIME_FIELD_NUMBER: builtins.int
    TEXT_FIELD_NUMBER: builtins.int
    URL_FIELD_NUMBER: builtins.int
    unique_tag: typing.Text
    type: api.value.logged_data_type_pb2.LoggedDataType.ValueType
    @property
    def created_time(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    @property
    def updated_time(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    text: typing.Text
    url: typing.Text
    def __init__(self,
        *,
        unique_tag: typing.Text = ...,
        type: api.value.logged_data_type_pb2.LoggedDataType.ValueType = ...,
        created_time: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
        updated_time: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
        text: typing.Text = ...,
        url: typing.Text = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["created_time",b"created_time","data",b"data","text",b"text","updated_time",b"updated_time","url",b"url"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["created_time",b"created_time","data",b"data","text",b"text","type",b"type","unique_tag",b"unique_tag","updated_time",b"updated_time","url",b"url"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["data",b"data"]) -> typing.Optional[typing_extensions.Literal["text","url"]]: ...
global___LoggedData = LoggedData
