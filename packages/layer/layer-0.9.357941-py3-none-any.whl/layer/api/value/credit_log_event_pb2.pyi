"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import layer.api.entity.entity_pb2
import layer.api.ids_pb2
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import google.protobuf.timestamp_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class CreditLogEvent(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TIME_FIELD_NUMBER: builtins.int
    PERFORMED_BY_ID_FIELD_NUMBER: builtins.int
    ENTITY_DESCRIPTION_FIELD_NUMBER: builtins.int
    ENTITY_PATH_FIELD_NUMBER: builtins.int
    CREDITS_DIFFERENCE_FIELD_NUMBER: builtins.int
    ENTITY_TYPE_FIELD_NUMBER: builtins.int
    ENTITY_NAME_FIELD_NUMBER: builtins.int
    DURATION_FIELD_NUMBER: builtins.int
    FABRIC_FIELD_NUMBER: builtins.int
    PROJECT_NAME_FIELD_NUMBER: builtins.int
    ACCOUNT_ID_FIELD_NUMBER: builtins.int
    @property
    def time(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    @property
    def performed_by_id(self) -> api.ids_pb2.UserId: ...
    entity_description: typing.Text
    entity_path: typing.Text
    credits_difference: typing.Text
    """This is a hack due to GraphQL's inability to work with bytes and longs"""

    entity_type: api.entity.entity_pb2.EntityType.ValueType
    entity_name: typing.Text
    duration: typing.Text
    """This is a hack due to GraphQL's inability to work with bytes and longs"""

    fabric: typing.Text
    project_name: typing.Text
    @property
    def account_id(self) -> api.ids_pb2.AccountId: ...
    def __init__(self,
        *,
        time: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
        performed_by_id: typing.Optional[api.ids_pb2.UserId] = ...,
        entity_description: typing.Text = ...,
        entity_path: typing.Text = ...,
        credits_difference: typing.Text = ...,
        entity_type: api.entity.entity_pb2.EntityType.ValueType = ...,
        entity_name: typing.Text = ...,
        duration: typing.Text = ...,
        fabric: typing.Text = ...,
        project_name: typing.Text = ...,
        account_id: typing.Optional[api.ids_pb2.AccountId] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["account_id",b"account_id","performed_by_id",b"performed_by_id","time",b"time"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["account_id",b"account_id","credits_difference",b"credits_difference","duration",b"duration","entity_description",b"entity_description","entity_name",b"entity_name","entity_path",b"entity_path","entity_type",b"entity_type","fabric",b"fabric","performed_by_id",b"performed_by_id","project_name",b"project_name","time",b"time"]) -> None: ...
global___CreditLogEvent = CreditLogEvent
