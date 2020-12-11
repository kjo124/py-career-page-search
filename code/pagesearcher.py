import urllib.request
from bs4 import BeautifulSoup
import re

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
file1 = open("/Users/kyleodin/Documents/GitHub/py-career-page-search/files/output", "w+")
file1.writelines(soup.get_text())
# open in online text editor in chrome
# contrl-a and copy categoriesraw from filters tab
# open glossary tab and control-a copy Glossary
# create a dicationary of terms
categoriesFile = open(
    "/Users/kyleodin/Documents/GitHub/py-career-page-search/files/categoriesraw", "r")
categoriesList = []

readyForCategories = 0
for line in categoriesFile:
    if line == "Hiring Software Engineers?\n":  # end of file
        break
    if readyForCategories == 1:
        category = line[1:]
        # remove digits from string
        # See this for next line: https://stackoverflow.com/a/12851835
        category = ''.join([i for i in category if not i.isdigit()])
        category = category[:-2]
        categoriesList.append(category)
    if line == "Reset all filters\n":
        readyForCategories = 1

# print(categoriesList)

termsFile = open(
    "/Users/kyleodin/Documents/GitHub/py-career-page-search/files/glossary", "r")
termsList = []

readyForterms = 0
for line in termsFile:
    if "%" in line:  # end of file
        break
    if readyForterms == 1:
        if line == "\n":
            pass
        elif "See also:" in line:
            pass  # See also line, do nothing
        elif len(line) < 83:
            terms = line
            terms = terms[:-1]
            # remove category from line
            for category in categoriesList:
                regex = re.compile(category)
                terms = regex.sub('', terms)
            terms = terms[:-1]
            termsList.append(terms)
            # maybe just create a database of each of these
        if len(line) > 83:
            pass  # glossary of term, do nothing
    if line == "Glossary\n":
        readyForterms = 1

print(termsList)
# go back to fill text file and count all terms from dicationary
# string.count(substring, start=…, end=…)
# arange in assending order
# assign terms to jobs
# evaluate for to long terms goals to inprove on
