import urllib.request
from bs4 import BeautifulSoup
import re
import mysql.connector

mySQLpasswordFile = open(
    "/Users/kyleodin/Documents/GitHub/py-career-page-search/MySQLpassword.txt", "r")

mySQLpassword = mySQLpasswordFile.readline().rstrip()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=mySQLpassword,
    database='pyCareerPageSearch'

)

cursor = db.cursor()


# ran these:
# cursor.execute("CREATE DATABASE pyCareerPageSearch")
# cursor.execute( "CREATE TABLE jobs (jobURL VARCHAR(255) PRIMARY KEY, jobHTMLoutputfile VARCHAR(255))")
# cursor.execute("SHOW TABLES")
# for x in cursor:
#    print(x)


# to run: python3.9 /Users/kyleodin/Documents/GitHub/py-career-page-search/code/pagesearcher.py

urls = ["https://jobs.lever.co/boweryfarming/c0de7734-9fe3-4191-a1de-39f19d1a7579",
        "https://boards.greenhouse.io/indigo/jobs/2404630", "https://boards.greenhouse.io/indigo/jobs/2249194"]

outputFile = open("/Users/kyleodin/Documents/GitHub/py-career-page-search/files/output", "a+")

for url in urls:
    sql = "SELECT * FROM jobs WHERE jobURL ='" + url + "'"
    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result) > 0:
        print("THIS IS IN THE TABLE")
    else:
        # TODO:
        # add new entery to table
        # output html to filters
        # amend output file with soup.get_text()

        # old code:
        # response = urllib.request.urlopen(url)
        # html = response.read()
        # Documentation of soup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
        # soup = BeautifulSoup(html, 'html.parser')
        # outputFile.writelines(soup.get_text())
        # print(soup.get_text())
        # print(soup.prettify())
        pass

# assign text to jobs
# create full text of all jobs with only spaces between all terms
# create html from full text of jobs


# open in online text editor in chrome
# contrl-a and copy categoriesraw from filters tab
# open glossary tab and control-a copy Glossary
# create a dicationary of terms
# TODO: probably just make a big database here
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

# print(termsList)

# go back to fill text file and count all terms from dicationary
# create dictionary
termDict = {}

for term in termsList:
    termDict[term] = 0

fileCounting = open(
    "/Users/kyleodin/Documents/GitHub/py-career-page-search/files/output", "r")

# go through line by line, make the line and term lowercase striped of
# whitespace and count the terms
for line in fileCounting:
    for term in termsList:
        c = 0
        # Does a pretty good job at searching though the page
        lineCopy = line.lower()
        termCopy = term.lower()
        if termCopy in lineCopy:
            c = len(re.findall(rf"[^a-z]{re.escape(termCopy)}[^a-z]", lineCopy))
            if c > 0:
                c += termDict[term]
                termDict[term] = c

# arange in assending order
termDict = dict(sorted(termDict.items(), key=lambda item: item[1]))
# remove last item
termDict.pop("")
# print(termDict)
# assign terms to jobs
# evaluate for to long terms goals to inprove on
