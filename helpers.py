"""
Various helpers
"""
import requests
from bs4 import BeautifulSoup

def get_soup(url):
    """
    Makes a request to the given url and returns a BeautifulSoup instance of the html
    """
    res = requests.get(url)
    return BeautifulSoup(res.content, "html.parser")