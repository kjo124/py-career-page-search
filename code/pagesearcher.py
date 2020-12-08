import urllib.request
from bs4 import BeautifulSoup

url = "https://boards.greenhouse.io/paytronix/jobs/2332500?gh_src=0e280c641us"

response = urllib.request.urlopen(url)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')


# to run: python3.9 /Users/kyleodin/Documents/GitHub/py-career-page-search/code/pagesearcher.py

# Documentation of soup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# print(soup.get_text())
# print(soup.prettify())


# assign text to jobs
# create full text of all jobs with only spaces between all terms
# create html from full text of jobs
file1 = open("/Users/kyleodin/Documents/GitHub/py-career-page-search/files/output.html", "w+")
file1.writelines(soup.get_text())
# open in online text editor in chrome
# contrl-a and copy categoriesraw from filters tab
# open glossary tab and control-a copy Glossary
# create a dicationary of terms

# go back to fill text file and count all terms from dicationary
# arange in assending order
# assign terms to jobs
# evaluate for to long term goals to inprove on
