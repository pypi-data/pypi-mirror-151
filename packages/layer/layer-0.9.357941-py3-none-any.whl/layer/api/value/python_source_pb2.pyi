"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import layer.api.value.language_version_pb2
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class PythonSource(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    CONTENT_FIELD_NUMBER: builtins.int
    ENTRYPOINT_FIELD_NUMBER: builtins.int
    ENVIRONMENT_FIELD_NUMBER: builtins.int
    LANGUAGE_VERSION_FIELD_NUMBER: builtins.int
    content: typing.Text
    entrypoint: typing.Text
    environment: typing.Text
    """represents the python environment file usually pip requirements.txt"""

    @property
    def language_version(self) -> api.value.language_version_pb2.LanguageVersion: ...
    def __init__(self,
        *,
        content: typing.Text = ...,
        entrypoint: typing.Text = ...,
        environment: typing.Text = ...,
        language_version: typing.Optional[api.value.language_version_pb2.LanguageVersion] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["language_version",b"language_version"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["content",b"content","entrypoint",b"entrypoint","environment",b"environment","language_version",b"language_version"]) -> None: ...
global___PythonSource = PythonSource
