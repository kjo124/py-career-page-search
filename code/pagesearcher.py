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

urlsFile = open(
    "/Users/kyleodin/Documents/GitHub/py-career-page-search/files/urls", "r")
urls = []
for line in urlsFile:
    # print(line.rstrip())
    urls.append(line.rstrip())


outputFile = open("/Users/kyleodin/Documents/GitHub/py-career-page-search/files/output", "a+")

# TODO split up HTML saving function from this
# TODO: Save a career page and all children pages
# TODO: make /files/output take in a directory of HTML files
for url in urls:
    sql = "SELECT * FROM jobs WHERE jobURL ='" + url + "'"
    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result) > 0:
        print("THIS IS IN THE TABLE")
        pass
    else:
        # add new entery to table
        sql = "INSERT INTO jobs (jobURL, jobHTMLoutputfile) VALUES (%s, %s)"
        id = url.replace('/', '.')
        htmlFileName = id + ".html"
        val = (url, htmlFileName)
        cursor.execute(sql, val)
        # output html to files
        htmlOutputFile = open(
            "/Users/kyleodin/Documents/GitHub/py-career-page-search/savedHTML/%s" % htmlFileName, "w+")
        response = urllib.request.urlopen(url)
        html = response.read()
        # Documentation of soup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
        soup = BeautifulSoup(html, 'html.parser')
        # html to files
        htmlOutputFile.writelines(soup.prettify())
        # amend output file with soup.get_text()
        # create plaintext from full text of jobs
        outputFile.writelines(soup.get_text())

# jobs table has been created, its has jobURLs and jobHTMLoutputfile names
# cursor.execute("SELECT * FROM jobs")
# result = cursor.fetchall()
# for x in result:
#    print(x)


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

# categoryList has been created, use this to search for and remove
# terms in glossary file
# print(categoriesList)

# create the terms database, it has categories and terms (key)
# Run this:
# cursor.execute("CREATE TABLE terms (term VARCHAR(255) PRIMARY KEY, category VARCHAR(255))")

termsFile = open(
    "/Users/kyleodin/Documents/GitHub/py-career-page-search/files/glossary", "r")

# cursor.execute("SHOW TABLES")
# for x in cursor:
#    print(x)


readyForterms = 0
# TODO: do this only if termsFile has changed
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
                termLengthCheck = len(terms)
                regex = re.compile(category)
                terms = regex.sub('', terms)
                # when term changes length and is > 0
                if len(terms) != termLengthCheck:
                    terms = terms[:-1]
                    # remove spaces
                    terms = str.strip(terms)
                    if len(terms) == 0:
                        terms = category
                    # Add term and category to terms database
                    sql = "SELECT * FROM terms WHERE term ='" + terms + "'"
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        print("THIS IS IN THE TERM TABLE")
                    else:
                        print("ADDING NEW TERM")
                        sql = "INSERT INTO terms (term, category) VALUES (%s,%s)"
                        val = (terms, category)
                        print(sql)
                        cursor.execute(sql, val)
                        # commit to db
                        db.commit()

        # TODO: refine this number
        if len(line) > 83:
            pass  # glossary of term, do nothing
    if line == "Glossary\n":
        readyForterms = 1

# cursor.execute("SELECT * FROM terms")
# result = cursor.fetchall()
# for x in result:
#    print(x)

cursor.execute("SELECT term FROM terms")
result = cursor.fetchall()
termsList = []
# construct termsList from result
for x in result:
    termsList.append(x[0])

# TODO: create the termCounts database, it has (key) terms, categories, and counts
# ran these:
# cursor.execute("CREATE TABLE termCounts (term VARCHAR(255) PRIMARY KEY, count INT)")
# go back to fill text file and count all terms from dicationary
# create dictionary
termDict = {}
for term in termsList:
    termDict[term] = 0

fileCounting = open(
    "/Users/kyleodin/Documents/GitHub/py-career-page-search/files/output", "r")

# go through line by line, make the line and term lowercase striped of
# whitespace and count the terms
# TODO: do this only if fileCounting has changed
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


# TODO: Create a database with Jobs, terms, counts, percentOfTotalCount # and limit by top 5 terms
for term in termsList:
    count = termDict[term]
    # cursor.execute("INSERT INTO termCounts VALUES (%s, %s)", (term, int(count)))
    sql = "UPDATE termCounts SET count = " + str(count) + " WHERE term = '" + term + "'"
    print(sql)
    cursor.execute(sql)


db.commit()

# arange in decending order and remove 0 counts
cursor.execute("SELECT * FROM termCounts WHERE count > 0 ORDER BY count DESC")
result = cursor.fetchall()
for x in result:
    print(x)


# TOD0: assign terms to jobs
# evaluate for to long terms goals to inprove on
