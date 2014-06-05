from pytest import fixture


from jsonselect.jsonselect import Parser


@fixture
def parser(request):
    return Parser({})
