from __future__ import print_function


from pytest import raises, skip
from py.path import local as localpath


from jsonselect.jsonselect import Parser, SelectorSyntaxError


from .utils import get_tests, items_equal


def pytest_generate_tests(metafunc):
    root_path = localpath(__file__).new(basename="")

    argvalues = []
    ids = []

    for level in range(1, 4):
        test_path = root_path.join(
            "..", "conformance_tests", "upstream", "level_{0:d}".format(level)
        )

        tests = list(get_tests(test_path))
        argvalues.extend([(level,) + test[:3] for test in tests])
        ids.extend(
            [
                "level_{0:d}_{1:s}".format(level, test[-1])
                for test in tests
            ]
        )

    test_path = root_path.join(
        "..", "conformance_tests", "custom"
    )

    tests = list(get_tests(test_path))
    argvalues.extend([(None,) + test[:3] for test in tests])
    ids.extend(["custom_{0:s}".format(test[-1]) for test in tests])

    metafunc.parametrize(metafunc.fixturenames, argvalues, ids=ids)


def test(level, selector, document, output):
    if level == 3:
        skip("Level 3 not implemented!")

    parser = Parser(document)

    try:
        if output[0][:5] == "Error":
            with raises(SelectorSyntaxError):
                parser.parse(selector)
            return
    except (IndexError, TypeError, KeyError):
        pass

    selection = parser.parse(selector)

    msg = "{}\n{}\n!=\n{}".format(selector, selection, output)

    print("Creating: test_{0:s}".format(selector))

    if all((hasattr(i, "__iter__") for i in (selection, output))):
        assert items_equal(selection, output), msg
    else:
        assert selection == output, msg
