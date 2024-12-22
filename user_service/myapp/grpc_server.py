from concurrent import futures
import grpc

from myapp.generated.proto import user_service_pb2, user_service_pb2_grpc

class UserServiceServicer(user_service_pb2_grpc.UserServiceServicer):
    def Authentication(self, request, context):
        return user_service_pb2.AuthResponse(authToken="berhasil", isAuthenticated=True)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server is running on port 50051...")
    server.start()
    server.wait_for_termination()
