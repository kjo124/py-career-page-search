import urllib.request
from bs4 import BeautifulSoup
import mysql.connector
from pathlib import Path
import re
import os

mySQLpasswordFile = open(
    "/Users/kyleodin/Documents/GitHub/py-career-page-search/MySQLpassword.txt", "r")

mySQLpassword = mySQLpasswordFile.readline().rstrip()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=mySQLpassword,
    database='pyCareerPageSearch'

)

# https://stackoverflow.com/a/33632767
cursor = db.cursor(buffered=True)

# ran these:
# cursor.execute("CREATE DATABASE pyCareerPageSearch")
# cursor.execute( "CREATE TABLE jobs (jobURL VARCHAR(255) PRIMARY KEY, jobHTMLoutputfile VARCHAR(255))")
# cursor.execute("SHOW TABLES")
# for x in cursor:
#    print(x)


# to run: python3.9 /Users/kyleodin/Documents/GitHub/py-career-page-search/code/pagesearcher.py
# after running:
# output file will need to be open in online text editor in Chrome
# open GlossaryTech pugin
# contrl-a and copy categoriesraw from filters tab
# open glossary tab and control-a copy Glossary
# rerun program

def getURLsFromPage(careerPageURL):
    unrefinedURLS = []
    url = careerPageURL
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        if "http" in str(link.get('href')):
            print(link.get('href'))
            unrefinedURLS.append(str(link.get('href')))
    return unrefinedURLS


def filterJobsOnUI(unrefinedURLS):
    baseURL = input("Enter baseURL: ")
    matching = [s for s in unrefinedURLS if baseURL in s]
    return matching


def saveURLs(jobURLs, companyName):
    # create companyName directory
    path = "/Users/kyleodin/Documents/GitHub/py-career-page-search/savedHTML/" + companyName + "/"
    Path(path).mkdir(parents=True, exist_ok=True)
    for url in jobURLs[:-1]:

        # output html to files
        # TODO: Make this save to a company directory

        response = urllib.request.urlopen(url)
        html = response.read()
        # Documentation of soup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
        soup = BeautifulSoup(html, 'html.parser')
        # save file as Title
        fileName = soup.title.string
        # remove / from file name
        fileName = re.sub('/', '', fileName)
        fileName = fileName + ".html"
        print(fileName)
        htmlFileName = path + fileName
        htmlOutputFile = open(
            htmlFileName, "w+")
        # html to files
        htmlOutputFile.writelines(soup.prettify())
    else:
        response = urllib.request.urlopen(jobURLs[-1])
        html = response.read()
        # Documentation of soup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
        soup = BeautifulSoup(html, 'html.parser')
        # save file as Title
        fileName = "Career Page"
        # remove / from file name
        fileName = re.sub('/', '', fileName)
        fileName = fileName + ".html"
        print(fileName)
        htmlFileName = path + fileName
        htmlOutputFile = open(
            htmlFileName, "w+")
        # html to files
        htmlOutputFile.writelines(soup.prettify())


urlsFile = open(
    "/Users/kyleodin/Documents/GitHub/py-career-page-search/files/urls", "r")
urls = []
for line in urlsFile:
    # print(line.rstrip())
    # use "# " to comment out URLs
    if "# " not in line.rstrip():
        urls.append(line.rstrip())
        print(line.rstrip())


for url in urls:
    if os.path.isfile(url):
        companyName = url.split("/")
        companyName = companyName[-1]
        companyName = companyName.split(".")
        companyName = companyName[0]
        print(companyName)
        # TODO: make this take in a manual download instead since some scripting can hide the job URLS
    else:
        # get company name
        companyName = url.split("/")
        companyName = companyName[2]
        unrefinedURLS = getURLsFromPage(url)
        jobURLs = filterJobsOnUI(unrefinedURLS)
        jobURLs.append(url)
        saveURLs(jobURLs, companyName)
