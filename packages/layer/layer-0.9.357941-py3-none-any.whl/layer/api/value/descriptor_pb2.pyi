"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import layer.api.ids_pb2
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class DescriptorCommand(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class StoreDataset(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        class PartitionInfo(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor
            PARTITION_ID_FIELD_NUMBER: builtins.int
            TASK_ID_FIELD_NUMBER: builtins.int
            STORAGE_LOCATION_FIELD_NUMBER: builtins.int
            partition_id: typing.Text
            task_id: typing.Text
            storage_location: typing.Text
            def __init__(self,
                *,
                partition_id: typing.Text = ...,
                task_id: typing.Text = ...,
                storage_location: typing.Text = ...,
                ) -> None: ...
            def ClearField(self, field_name: typing_extensions.Literal["partition_id",b"partition_id","storage_location",b"storage_location","task_id",b"task_id"]) -> None: ...

        DATASET_NAME_FIELD_NUMBER: builtins.int
        DATA_SOURCE_NAME_FIELD_NUMBER: builtins.int
        BUILD_ID_FIELD_NUMBER: builtins.int
        PARTITION_INFO_FIELD_NUMBER: builtins.int
        dataset_name: typing.Text
        data_source_name: typing.Text
        @property
        def build_id(self) -> api.ids_pb2.DatasetBuildId: ...
        @property
        def partition_info(self) -> global___DescriptorCommand.StoreDataset.PartitionInfo: ...
        def __init__(self,
            *,
            dataset_name: typing.Text = ...,
            data_source_name: typing.Text = ...,
            build_id: typing.Optional[api.ids_pb2.DatasetBuildId] = ...,
            partition_info: typing.Optional[global___DescriptorCommand.StoreDataset.PartitionInfo] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["build_id",b"build_id","partition_info",b"partition_info"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["build_id",b"build_id","data_source_name",b"data_source_name","dataset_name",b"dataset_name","partition_info",b"partition_info"]) -> None: ...

    STORE_DATASET_FIELD_NUMBER: builtins.int
    @property
    def store_dataset(self) -> global___DescriptorCommand.StoreDataset: ...
    def __init__(self,
        *,
        store_dataset: typing.Optional[global___DescriptorCommand.StoreDataset] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["command",b"command","store_dataset",b"store_dataset"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["command",b"command","store_dataset",b"store_dataset"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["command",b"command"]) -> typing.Optional[typing_extensions.Literal["store_dataset"]]: ...
global___DescriptorCommand = DescriptorCommand
