from olive.proto import zoodroom_pb2_grpc
from marshmallow import ValidationError
from olive.proto.rpc import Response
import traceback


class OnionService(zoodroom_pb2_grpc.OnionServiceServicer):
    def __init__(self, leaf_store, app):
        self.leaf_store = leaf_store
        self.app = app

    def AddLeaf(self, request: AddLeafRequest, context) -> AddLeafResponse:
        try:
            # TODO to be implemented
            return Response.message(

            )
        except ValueError as ve:
            self.app.log.error('Schema value error:\r\n{}'.format(traceback.format_exc()))
            return Response.message(
                error={
                    'code': 'value_error',
                    'message': str(ve),
                    'details': []
                }
            )
        except ValidationError as ve:
            self.app.log.error('Schema validation error:\r\n{}'.format(ve.messages))
            return Response.message(
                error={
                    'code': 'invalid_schema',
                    'message': 'Given data is not valid!',
                    'details': []
                }
            )
        except Exception:
            self.app.log.error('An error occurred: {}'.format(traceback.format_exc()))
            return Response.message(
                error={
                    'code': 'server_error',
                    'message': 'Server is in maintenance mode',
                    'details': []
                }
            )
