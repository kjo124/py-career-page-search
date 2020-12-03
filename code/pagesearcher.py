import urllib.request
from bs4 import BeautifulSoup

url = "https://boards.greenhouse.io/paytronix/jobs/2471269?gh_src=2c6509dd1us"

response = urllib.request.urlopen(url)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')


# python3.9 /Users/kyleodin/Documents/GitHub/py-career-page-search/code/pagesearcher.py

# Documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# print(soup.get_text())
# print(soup.prettify())
