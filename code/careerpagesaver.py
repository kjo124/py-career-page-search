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

def getJobs(careerPageURL):
    url = careerPageURL
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        print(link.get('href'))


urlsFile = open(
    "/Users/kyleodin/Documents/GitHub/py-career-page-search/files/urls", "r")
urls = []
for line in urlsFile:
    # print(line.rstrip())
    urls.append(line.rstrip())


# outputFile = open("/Users/kyleodin/Documents/GitHub/py-career-page-search/files/output", "a+")

# TODO split up HTML saving function from this
# TODO: Save a career page and all children pages
# TODO: make /files/output take in a directory of HTML files
for url in urls:
    getJobs(url)
