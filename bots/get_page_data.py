import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession


def page_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')


def render_JS(URL):
    session = HTMLSession()
    page = session.get(URL)
    page.html.render()
    return page.html
