from olive.store.mongo_connection import MongoConnection
from olive.proto import zoodroom_pb2_grpc, zoodroom_pb2
from onion.core.store.leaf import LeafStore
from onion.core.onion import OnionService
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


@contextmanager
def grpc_server(cls, onion_store, app):
    """Instantiate a Onion server and return a stub for use in tests"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    zoodroom_pb2_grpc.add_OnionServiceServicer_to_server(cls(LeafStore, app), server)
    port = server.add_insecure_port('[::]:0')
    server.start()

    try:
        with grpc.insecure_channel('localhost:%d' % port) as channel:
            yield zoodroom_pb2_grpc.OnionServiceStub(channel)
    finally:
        server.stop(None)


class LeafTest(unittest.TestCase):
    def setUp(self):
        self.app = OnionAppTest(config_files=['/etc/onion/onion.yml'])
        self.app.__enter__()
        mongodb_cfg = self.app.config['onion']['mongodb']
        mongo = MongoConnection(mongodb_cfg, self.app)
        target_database = mongo.service_db
        self.sample_setting = self.app.config['onion']['sample_setting']
        self.leaf_store = LeafStore(target_database.leaf, self.app)
        self.grpc_server = grpc_server(OnionService, self.leaf_store, self.app)

    def test_add_leaf(self):
        with grpc_server(OnionService, self.leaf_store, self.app) as stub:
            response = stub.AddLeaf(zoodroom_pb2.AddLeafRequest(
                leaf_name='Leaf of Onion'
            ))
            self.assertNotEqual(response.leaf_id, '')
