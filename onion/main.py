from olive.store.mongo_connection import MongoConnection
from onion.core.store.leaf_store import LeafStore
from olive.proto.rpc import GRPCServerBase
from onion.core.onion import OnionService
from olive.proto import zoodroom_pb2_grpc
from cement.core.exc import CaughtSignal
from onion.controllers.base import Base
from olive.exc import OnionServiceError
from cement import App, TestApp


class OnionApp(App):
    """Onion primary application."""

    class Meta:
        label = 'onion'

        # configuration defaults
        # config_defaults = CONFIG

        # call sys.exit() on close
        close_on_exit = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'redis',
        ]

        # configuration handler
        config_handler = 'yaml'

        cache_handler = 'redis'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # register handlers
        handlers = [
            Base
        ]

    def run(self):
        mongodb_cfg = self.config['onion']['mongodb']
        self.log.debug('initiating MongoDB configuration...')
        mongo = MongoConnection(mongodb_cfg, self)
        self.log.info('current database: {}'.format(mongo))
        target_database = mongo.service_db
        leaf_store = LeafStore(target_database.leaf, self)
        self.log.info('current service name: ' + self._meta.label)

        # Set a cached value
        # TODO use cache where its needed
        # self.cache.set(key='my_key', value='my value', time=20)

        # Passing self for app is suggested by Cement Core Developer:
        #   - https://github.com/datafolklabs/cement/issues/566
        cs = OnionServer(service_name=self._meta.label,
                         leaf_store=leaf_store,
                         app=self)
        cs.start()


class OnionServer(GRPCServerBase):
    def __init__(self, service_name, leaf_store, app):
        super(OnionServer, self).__init__(service=service_name, app=app)

        # add class to gRPC server
        service = OnionService(leaf_store=leaf_store,
                               app=app)
        # adds a OnionService to a gRPC.Server
        zoodroom_pb2_grpc.add_OnionServiceServicer_to_server(service, self.server)


class OnionAppTest(TestApp, OnionApp):
    """A sub-class of OnionService that is better suited for testing."""

    class Meta:
        label = 'onion'


def main():
    with OnionApp() as app:
        try:
            app.run()
        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except OnionServiceError as e:
            print('OnionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
