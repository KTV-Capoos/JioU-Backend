from ..api import get


def knn_endpoint():
    url = "https://api.github.com/users/jh123x"
    data = get(url)
    vector = []
    user_id = []
    # for i in data:

    assert data["login"] == "Jh123x"