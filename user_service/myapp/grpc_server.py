import grpc
import logging
from concurrent import futures
from proto import user_service_pb2_grpc
from collections import namedtuple
from .grpc_handler import createUserHandler, authenticationHandler, getUserByIdHandler

UserStruct = namedtuple('UserStruct', ['name', 'email', 'password', 'role'])
logger = logging.getLogger('myapp')

class UserServiceServicer(user_service_pb2_grpc.UserServiceServicer):
    def Authentication(self, request, context):
        logger.info("Authentication %s", request)

        return authenticationHandler(request)
    
    def CreateUser(self, request, context):
        logger.info('CreateUser: %s', request)

        return createUserHandler(request)
    
    def GetUserById(self, request, context):
        logger.info('GetUserById: %s', str(request))

        return getUserByIdHandler(request)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server is running on port 50051...")
    server.start()
    server.wait_for_termination()
