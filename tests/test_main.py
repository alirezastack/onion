from onion.main import OnionAppTest


def test_onion(tmp):
    with OnionAppTest() as app:
        res = app.run()
        print(res)
        raise Exception


def test_command1(tmp):
    argv = ['command1']
    with OnionAppTest(argv=argv) as app:
        app.run()
