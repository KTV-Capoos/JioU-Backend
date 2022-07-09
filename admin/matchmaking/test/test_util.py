from ..api import get


def test_get():
    url = "https://api.github.com/users/jh123x"
    data = get(url)
    assert data["login"] == "Jh123x"