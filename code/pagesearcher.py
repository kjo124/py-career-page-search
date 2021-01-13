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
termsList = []

cursor.execute("SHOW TABLES")
for x in cursor:
    print(x)

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
                termLengthCheck = len(terms)
                regex = re.compile(category)
                terms = regex.sub('', terms)
                # when term changes length and is > 0
                if len(terms) != termLengthCheck:
                    terms = terms[:-1]
                    if len(terms) == 0:
                        terms = category
                    termsList.append(terms)
                    # Add term and category to terms database
                    sql = "SELECT * FROM terms WHERE term ='" + terms + "'"
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        print("THIS IS IN THE TERM TABLE")
                    else:
                        # TODO: terms are not staying in the table for some reason
                        print("ADDING NEW TERM")
                        sql = "INSERT INTO terms (term, category) VALUES (%s,%s)"
                        val = (terms, category)
                        print(sql)
                        cursor.execute(sql, val)
                        db.commit()

        # TODO: refine this number
        if len(line) > 83:
            pass  # glossary of term, do nothing
    if line == "Glossary\n":
        readyForterms = 1

# print(termsList)
cursor.execute("SELECT * FROM terms")
result = cursor.fetchall()
for x in result:
    print(x)
# TODO: create the wordCount database, it has (key) terms, categories, and counts
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
# TODO: create a method that takes in a plaintext file, a category #
# array, a term array, and returns an array of terms and counts
# TODO: Create a database with Jobs, terms, counts, percentOfTotalCount # and limit by top 5 terms
# TODO: Print wordCount output decending by counts and remove 0 counts
# arange in assending order
termDict = dict(sorted(termDict.items(), key=lambda item: item[1]))
# remove last item
print(termDict)
# assign terms to jobs
# evaluate for to long terms goals to inprove on
