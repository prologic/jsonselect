from pytest import fixture


from jsonselect import select


@fixture
def obj(request):
    return {
        "hello": "world",
        "foo": [1, 2, 3],
        "bar": {
            "x": "y"
        }
    }


def test_syntax_error_returns_false(obj):
    assert select("gibberish", obj) is False


def test_no_results_returns_none(obj):
    assert select(".foobar", obj) is None
