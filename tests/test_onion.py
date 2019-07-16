from olive.proto import zoodroom_pb2_grpc, zoodroom_pb2
from decorator import contextmanager
from onion.main import OnionAppTest
from concurrent import futures
import unittest
import grpc


def test_onion():
    # test onion without any subcommands or arguments
    with OnionAppTest(config_files=['/etc/onion/onion.yml']) as app:
        app.run()
        assert app.exit_code == 0


def test_onion_debug():
    # test that debug mode is functional
    argv = ['--debug']
    with OnionAppTest(argv=argv) as app:
        app.run()
        assert app.debug is True


def test_command1():
    # test command1 without arguments
    argv = ['command1']
    with OnionAppTest(argv=argv) as app:
        app.run()
        data, output = app.last_rendered
        assert data['foo'] == 'bar'
        assert output.find('Foo => bar')

    # test command1 with arguments
    argv = ['command1', '--foo', 'not-bar']
    with OnionAppTest(argv=argv) as app:
        app.run()
        data, output = app.last_rendered
        assert data['foo'] == 'not-bar'
        assert output.find('Foo => not-bar')


@contextmanager
def add_leaf(cls):
    """Instantiate an Onion server and return a stub for use in tests"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    zoodroom_pb2_grpc.add_OnionServiceServicer_to_server(cls(), server)
    port = server.add_insecure_port('[::]:0')
    server.start()

    try:
        with grpc.insecure_channel('localhost:%d' % port) as channel:
            yield zoodroom_pb2_grpc.OnionServiceStub(channel)
    finally:
        server.stop(None)


class SurveyTest(unittest.TestCase):
    def test_add_leaf(self):
        # may do something extra for this mock if it's stateful
        class FakeAddLeaf(zoodroom_pb2_grpc.OnionServiceServicer):
            def AddLeaf(self, request, context):
                return zoodroom_pb2.AddLeafResponse()

        with add_leaf(FakeAddLeaf) as stub:
            response = stub.AddLeaf(zoodroom_pb2.AddLeafRequest(
                # TODO put proto fields here for request
            ))
            self.assertEqual(response.leaf_id, '')
