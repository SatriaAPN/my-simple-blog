from django.core.management.base import BaseCommand
from myapp.grpc_server import serve


class Command(BaseCommand):
    help = 'Start the gRPC server'

    def handle(self, *args, **kwargs):
        serve()
