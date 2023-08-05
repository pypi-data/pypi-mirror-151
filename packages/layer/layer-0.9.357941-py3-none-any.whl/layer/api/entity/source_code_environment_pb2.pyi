"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import layer.api.value.dependency_pb2
import layer.api.value.source_code_pb2
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class SourceCodeEnvironment(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    SOURCE_CODE_FIELD_NUMBER: builtins.int
    DEPENDENCY_FILE_FIELD_NUMBER: builtins.int
    @property
    def source_code(self) -> api.value.source_code_pb2.SourceCode: ...
    @property
    def dependency_file(self) -> api.value.dependency_pb2.DependencyFile: ...
    def __init__(self,
        *,
        source_code: typing.Optional[api.value.source_code_pb2.SourceCode] = ...,
        dependency_file: typing.Optional[api.value.dependency_pb2.DependencyFile] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["dependency_file",b"dependency_file","source_code",b"source_code"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["dependency_file",b"dependency_file","source_code",b"source_code"]) -> None: ...
global___SourceCodeEnvironment = SourceCodeEnvironment
