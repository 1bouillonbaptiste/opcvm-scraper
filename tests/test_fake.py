from src.fake import get_foo


def test_get_foo():
    assert get_foo() == "foo"
