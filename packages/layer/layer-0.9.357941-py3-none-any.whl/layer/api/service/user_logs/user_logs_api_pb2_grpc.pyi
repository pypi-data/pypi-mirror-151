"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import layer.api.service.user_logs.user_logs_api_pb2
import grpc
import typing

class UserLogsAPIStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    GetPipelineRunLogs: grpc.UnaryUnaryMultiCallable[
        api.service.user_logs.user_logs_api_pb2.GetPipelineRunLogsRequest,
        api.service.user_logs.user_logs_api_pb2.GetPipelineRunLogsResponse]

    GetPipelineRunLogsPerEntity: grpc.UnaryUnaryMultiCallable[
        api.service.user_logs.user_logs_api_pb2.GetPipelineRunLogsPerEntityRequest,
        api.service.user_logs.user_logs_api_pb2.GetPipelineRunLogsPerEntityResponse]

    GetPipelineRunLogsStreaming: grpc.UnaryStreamMultiCallable[
        api.service.user_logs.user_logs_api_pb2.GetPipelineRunLogsStreamingRequest,
        api.service.user_logs.user_logs_api_pb2.GetPipelineRunLogsStreamingResponse]


class UserLogsAPIServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def GetPipelineRunLogs(self,
        request: api.service.user_logs.user_logs_api_pb2.GetPipelineRunLogsRequest,
        context: grpc.ServicerContext,
    ) -> api.service.user_logs.user_logs_api_pb2.GetPipelineRunLogsResponse: ...

    @abc.abstractmethod
    def GetPipelineRunLogsPerEntity(self,
        request: api.service.user_logs.user_logs_api_pb2.GetPipelineRunLogsPerEntityRequest,
        context: grpc.ServicerContext,
    ) -> api.service.user_logs.user_logs_api_pb2.GetPipelineRunLogsPerEntityResponse: ...

    @abc.abstractmethod
    def GetPipelineRunLogsStreaming(self,
        request: api.service.user_logs.user_logs_api_pb2.GetPipelineRunLogsStreamingRequest,
        context: grpc.ServicerContext,
    ) -> typing.Iterator[api.service.user_logs.user_logs_api_pb2.GetPipelineRunLogsStreamingResponse]: ...


def add_UserLogsAPIServicer_to_server(servicer: UserLogsAPIServicer, server: grpc.Server) -> None: ...
