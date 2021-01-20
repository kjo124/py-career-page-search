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

directoryPath = "/Users/kyleodin/Documents/GitHub/py-career-page-search/savedHTML/"

htmlFiles = []


def getAllHTMLfilesInDirectory(directory):
    for entry in os.scandir(directory):
        if not os.path.isdir(entry.path):
            htmlFiles.append(entry.path)
        else:
            getAllHTMLfilesInDirectory(entry.path)


def copyMatchingHTMLfiles(files, searchTerm):
    for file in files:
        with open(file) as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            fileText = soup.get_text()
            fileText = fileText.replace('\n', '').replace(' ', '').lower()
            searchTerm = searchTerm.replace('\n', '').replace(' ', '').lower()
            if searchTerm in fileText:
                # copy HTML and place into a searchTerm directory
                print("matching file:" + file)


getAllHTMLfilesInDirectory(directoryPath)
copyMatchingHTMLfiles(htmlFiles, "javA")
