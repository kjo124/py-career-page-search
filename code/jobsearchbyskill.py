from bs4 import BeautifulSoup
import mysql.connector
import os
from shutil import copyfile
from pathlib import Path

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

directoryPath = "/Users/kyleodin/Documents/GitHub/py-career-page-search/savedHTML/"

htmlFiles = []


def getAllHTMLfilesInDirectory(directory):
    for entry in os.scandir(directory):
        if not os.path.isdir(entry.path):
            if "Career Page.html" not in str(entry):
                htmlFiles.append(entry.path)
        else:
            getAllHTMLfilesInDirectory(entry.path)


def copyMatchingHTMLfiles(files, searchTerms):
    for term in searchTerms:
        path = "/Users/kyleodin/Documents/GitHub/py-career-page-search/TermSearching/" + term + "/"
        Path(path).mkdir(parents=True, exist_ok=True)
        for file in files:
            with open(file) as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                fileText = soup.get_text()
                fileText = fileText.replace('\n', '').replace(' ', '').lower()
                term = term.replace('\n', '').replace(' ', '').lower()
                if term in fileText:
                    print("matching file:" + file)
                    copyfile(
                        file, "/Users/kyleodin/Documents/GitHub/py-career-page-search/TermSearching/" + term + "/" + os.path.basename(file))


searchTerms = ["java", "sql"]
getAllHTMLfilesInDirectory(directoryPath)
copyMatchingHTMLfiles(htmlFiles, searchTerms)
