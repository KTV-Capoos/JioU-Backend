import requests

def get(url):
    """
    Get data from url
    Deserialises the API response into a Python Dictionary
    """
    return requests.get(url).json()