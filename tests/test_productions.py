from pytest import raises


from jsonselect.jsonselect import lex, LexingError


def test_lex_expr():
    tokens = lex("(n+2), object")
    assert tokens == [
        ("expr", "(n+2)"),
        ("operator", ","),
        ("type", "object")
    ]

    with raises(LexingError):
        lex("(import sys; sys.exit(0))")


def test_eval_args(parser):
    assert parser.expr_production("(1 + 2)")(None) == 3
