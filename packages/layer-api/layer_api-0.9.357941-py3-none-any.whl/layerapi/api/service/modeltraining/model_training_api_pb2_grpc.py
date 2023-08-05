# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from layerapi.api.service.modeltraining import model_training_api_pb2 as api_dot_service_dot_modeltraining_dot_model__training__api__pb2


class ModelTrainingAPIStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetSourceCodeUploadCredentials = channel.unary_unary(
                '/api.ModelTrainingAPI/GetSourceCodeUploadCredentials',
                request_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetSourceCodeUploadCredentialsRequest.SerializeToString,
                response_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetSourceCodeUploadCredentialsResponse.FromString,
                )
        self.StartModelTraining = channel.unary_unary(
                '/api.ModelTrainingAPI/StartModelTraining',
                request_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.StartModelTrainingRequest.SerializeToString,
                response_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.StartModelTrainingResponse.FromString,
                )
        self.CancelModelTraining = channel.unary_unary(
                '/api.ModelTrainingAPI/CancelModelTraining',
                request_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.CancelModelTrainingRequest.SerializeToString,
                response_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.CancelModelTrainingResponse.FromString,
                )
        self.GetModelTrainStatus = channel.unary_unary(
                '/api.ModelTrainingAPI/GetModelTrainStatus',
                request_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetModelTrainStatusRequest.SerializeToString,
                response_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetModelTrainStatusResponse.FromString,
                )
        self.StartHyperparameterTuning = channel.unary_unary(
                '/api.ModelTrainingAPI/StartHyperparameterTuning',
                request_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.StartHyperparameterTuningRequest.SerializeToString,
                response_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.StartHyperparameterTuningResponse.FromString,
                )
        self.CancelHyperparameterTuning = channel.unary_unary(
                '/api.ModelTrainingAPI/CancelHyperparameterTuning',
                request_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.CancelHyperparameterTuningRequest.SerializeToString,
                response_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.CancelHyperparameterTuningResponse.FromString,
                )
        self.GetHyperparameterTuningStatus = channel.unary_unary(
                '/api.ModelTrainingAPI/GetHyperparameterTuningStatus',
                request_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetHyperparameterTuningStatusRequest.SerializeToString,
                response_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetHyperparameterTuningStatusResponse.FromString,
                )
        self.CreateHyperparameterTuning = channel.unary_unary(
                '/api.ModelTrainingAPI/CreateHyperparameterTuning',
                request_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.CreateHyperparameterTuningRequest.SerializeToString,
                response_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.CreateHyperparameterTuningResponse.FromString,
                )
        self.GetHyperparameterTuning = channel.unary_unary(
                '/api.ModelTrainingAPI/GetHyperparameterTuning',
                request_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetHyperparameterTuningRequest.SerializeToString,
                response_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetHyperparameterTuningResponse.FromString,
                )
        self.UpdateHyperparameterTuning = channel.unary_unary(
                '/api.ModelTrainingAPI/UpdateHyperparameterTuning',
                request_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.UpdateHyperparameterTuningRequest.SerializeToString,
                response_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.UpdateHyperparameterTuningResponse.FromString,
                )
        self.StoreHyperparameterTuningMetadata = channel.unary_unary(
                '/api.ModelTrainingAPI/StoreHyperparameterTuningMetadata',
                request_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.StoreHyperparameterTuningMetadataRequest.SerializeToString,
                response_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.StoreHyperparameterTuningMetadataResponse.FromString,
                )
        self.GetOrCreateLatestPendingHyperparameterTuningId = channel.unary_unary(
                '/api.ModelTrainingAPI/GetOrCreateLatestPendingHyperparameterTuningId',
                request_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetOrCreateLatestPendingHyperparameterTuningIdRequest.SerializeToString,
                response_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetOrCreateLatestPendingHyperparameterTuningIdResponse.FromString,
                )


class ModelTrainingAPIServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetSourceCodeUploadCredentials(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StartModelTraining(self, request, context):
        """model train
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CancelModelTraining(self, request, context):
        """CancelModelTraining is not guaranteed to succeed and shall return return immediately.
        A client can use the GetModelTrainStatus to know if cancellation eventually succeeds.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetModelTrainStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StartHyperparameterTuning(self, request, context):
        """hpt model train
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CancelHyperparameterTuning(self, request, context):
        """CancelHyperparameterTuning is not guaranteed to succeed and shall return return immediately.
        A client can use the GetHyperparameterTuningStatus to know if cancellation eventually succeeds.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetHyperparameterTuningStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateHyperparameterTuning(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetHyperparameterTuning(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateHyperparameterTuning(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StoreHyperparameterTuningMetadata(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetOrCreateLatestPendingHyperparameterTuningId(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ModelTrainingAPIServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetSourceCodeUploadCredentials': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSourceCodeUploadCredentials,
                    request_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetSourceCodeUploadCredentialsRequest.FromString,
                    response_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetSourceCodeUploadCredentialsResponse.SerializeToString,
            ),
            'StartModelTraining': grpc.unary_unary_rpc_method_handler(
                    servicer.StartModelTraining,
                    request_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.StartModelTrainingRequest.FromString,
                    response_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.StartModelTrainingResponse.SerializeToString,
            ),
            'CancelModelTraining': grpc.unary_unary_rpc_method_handler(
                    servicer.CancelModelTraining,
                    request_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.CancelModelTrainingRequest.FromString,
                    response_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.CancelModelTrainingResponse.SerializeToString,
            ),
            'GetModelTrainStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.GetModelTrainStatus,
                    request_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetModelTrainStatusRequest.FromString,
                    response_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetModelTrainStatusResponse.SerializeToString,
            ),
            'StartHyperparameterTuning': grpc.unary_unary_rpc_method_handler(
                    servicer.StartHyperparameterTuning,
                    request_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.StartHyperparameterTuningRequest.FromString,
                    response_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.StartHyperparameterTuningResponse.SerializeToString,
            ),
            'CancelHyperparameterTuning': grpc.unary_unary_rpc_method_handler(
                    servicer.CancelHyperparameterTuning,
                    request_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.CancelHyperparameterTuningRequest.FromString,
                    response_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.CancelHyperparameterTuningResponse.SerializeToString,
            ),
            'GetHyperparameterTuningStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.GetHyperparameterTuningStatus,
                    request_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetHyperparameterTuningStatusRequest.FromString,
                    response_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetHyperparameterTuningStatusResponse.SerializeToString,
            ),
            'CreateHyperparameterTuning': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateHyperparameterTuning,
                    request_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.CreateHyperparameterTuningRequest.FromString,
                    response_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.CreateHyperparameterTuningResponse.SerializeToString,
            ),
            'GetHyperparameterTuning': grpc.unary_unary_rpc_method_handler(
                    servicer.GetHyperparameterTuning,
                    request_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetHyperparameterTuningRequest.FromString,
                    response_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetHyperparameterTuningResponse.SerializeToString,
            ),
            'UpdateHyperparameterTuning': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateHyperparameterTuning,
                    request_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.UpdateHyperparameterTuningRequest.FromString,
                    response_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.UpdateHyperparameterTuningResponse.SerializeToString,
            ),
            'StoreHyperparameterTuningMetadata': grpc.unary_unary_rpc_method_handler(
                    servicer.StoreHyperparameterTuningMetadata,
                    request_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.StoreHyperparameterTuningMetadataRequest.FromString,
                    response_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.StoreHyperparameterTuningMetadataResponse.SerializeToString,
            ),
            'GetOrCreateLatestPendingHyperparameterTuningId': grpc.unary_unary_rpc_method_handler(
                    servicer.GetOrCreateLatestPendingHyperparameterTuningId,
                    request_deserializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetOrCreateLatestPendingHyperparameterTuningIdRequest.FromString,
                    response_serializer=api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetOrCreateLatestPendingHyperparameterTuningIdResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'api.ModelTrainingAPI', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ModelTrainingAPI(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetSourceCodeUploadCredentials(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/api.ModelTrainingAPI/GetSourceCodeUploadCredentials',
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetSourceCodeUploadCredentialsRequest.SerializeToString,
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetSourceCodeUploadCredentialsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StartModelTraining(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/api.ModelTrainingAPI/StartModelTraining',
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.StartModelTrainingRequest.SerializeToString,
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.StartModelTrainingResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CancelModelTraining(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/api.ModelTrainingAPI/CancelModelTraining',
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.CancelModelTrainingRequest.SerializeToString,
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.CancelModelTrainingResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetModelTrainStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/api.ModelTrainingAPI/GetModelTrainStatus',
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetModelTrainStatusRequest.SerializeToString,
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetModelTrainStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StartHyperparameterTuning(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/api.ModelTrainingAPI/StartHyperparameterTuning',
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.StartHyperparameterTuningRequest.SerializeToString,
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.StartHyperparameterTuningResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CancelHyperparameterTuning(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/api.ModelTrainingAPI/CancelHyperparameterTuning',
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.CancelHyperparameterTuningRequest.SerializeToString,
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.CancelHyperparameterTuningResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetHyperparameterTuningStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/api.ModelTrainingAPI/GetHyperparameterTuningStatus',
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetHyperparameterTuningStatusRequest.SerializeToString,
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetHyperparameterTuningStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateHyperparameterTuning(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/api.ModelTrainingAPI/CreateHyperparameterTuning',
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.CreateHyperparameterTuningRequest.SerializeToString,
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.CreateHyperparameterTuningResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetHyperparameterTuning(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/api.ModelTrainingAPI/GetHyperparameterTuning',
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetHyperparameterTuningRequest.SerializeToString,
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetHyperparameterTuningResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateHyperparameterTuning(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/api.ModelTrainingAPI/UpdateHyperparameterTuning',
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.UpdateHyperparameterTuningRequest.SerializeToString,
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.UpdateHyperparameterTuningResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StoreHyperparameterTuningMetadata(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/api.ModelTrainingAPI/StoreHyperparameterTuningMetadata',
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.StoreHyperparameterTuningMetadataRequest.SerializeToString,
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.StoreHyperparameterTuningMetadataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetOrCreateLatestPendingHyperparameterTuningId(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/api.ModelTrainingAPI/GetOrCreateLatestPendingHyperparameterTuningId',
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetOrCreateLatestPendingHyperparameterTuningIdRequest.SerializeToString,
            api_dot_service_dot_modeltraining_dot_model__training__api__pb2.GetOrCreateLatestPendingHyperparameterTuningIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
