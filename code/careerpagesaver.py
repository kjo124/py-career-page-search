import urllib.request
from bs4 import BeautifulSoup
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
            if not "//www.greenhouse.io/" in str(link.get('href')):
                print(link.get('href'))
                unrefinedURLS.append(str(link.get('href')))
    return unrefinedURLS


def filterJobsOnUI(unrefinedURLS):
    baseURL = input("Enter baseURL: ")
    matching = [s for s in unrefinedURLS if baseURL in s]
    return matching


def saveURLs(jobURLs):
    for url in jobURLs:
        fileName = url.replace('/', '.')
        htmlFileName = fileName + ".html"
        # output html to files
        # TODO: Make this save to a company directory
        htmlOutputFile = open(
            "/Users/kyleodin/Documents/GitHub/py-career-page-search/Test/%s" % htmlFileName, "w+")
        response = urllib.request.urlopen(url)
        html = response.read()
        # Documentation of soup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
        soup = BeautifulSoup(html, 'html.parser')
        # html to files
        htmlOutputFile.writelines(soup.prettify())


urlsFile = open(
    "/Users/kyleodin/Documents/GitHub/py-career-page-search/files/urls", "r")
urls = []
for line in urlsFile:
    # print(line.rstrip())
    # use "# " to comment out URLs
    if not "# " in line.rstrip():
        urls.append(line.rstrip())
        print(line.rstrip())


# outputFile = open("/Users/kyleodin/Documents/GitHub/py-career-page-search/files/output", "a+")


for url in urls:
    unrefinedURLS = getURLsFromPage(url)
    jobURLs = filterJobsOnUI(unrefinedURLS)
    jobURLs.append(url)
    saveURLs(jobURLs)
