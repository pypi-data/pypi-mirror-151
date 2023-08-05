"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class DatasetSchema(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class Field(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        NAME_FIELD_NUMBER: builtins.int
        NULLABLE_FIELD_NUMBER: builtins.int
        TYPE_FIELD_NUMBER: builtins.int
        name: typing.Text
        nullable: builtins.bool
        @property
        def type(self) -> global___DatasetSchema.FieldType: ...
        def __init__(self,
            *,
            name: typing.Text = ...,
            nullable: builtins.bool = ...,
            type: typing.Optional[global___DatasetSchema.FieldType] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["type",b"type"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["name",b"name","nullable",b"nullable","type",b"type"]) -> None: ...

    class FieldType(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        NAME_FIELD_NUMBER: builtins.int
        name: typing.Text
        def __init__(self,
            *,
            name: typing.Text = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["name",b"name"]) -> None: ...

    FIELDS_FIELD_NUMBER: builtins.int
    @property
    def fields(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___DatasetSchema.Field]: ...
    def __init__(self,
        *,
        fields: typing.Optional[typing.Iterable[global___DatasetSchema.Field]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["fields",b"fields"]) -> None: ...
global___DatasetSchema = DatasetSchema
