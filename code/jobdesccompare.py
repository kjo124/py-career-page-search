from bs4 import BeautifulSoup
import os

htmlFiles = []
htmlFilesText = []


def getAllHTMLfilesInDirectory(directory):
    for entry in os.scandir(directory):
        if not os.path.isdir(entry.path):
            htmlFiles.append(entry.path)
        else:
            getAllHTMLfilesInDirectory(entry.path)


def exportFileText(htmlFiles):
    for file in htmlFiles:
        with open(file, 'rb') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            fileText = soup.get_text()
            fileText = fileText.replace('\n', ' ')
            htmlFilesText.append(fileText)
    for text in htmlFilesText:
        print(text)


def findCommonWords(htmlFilesText):
    string1 = htmlFilesText[2]
    string2 = htmlFilesText[3]
    string1_words = set(string1.split())
    string2_words = set(string2.split())

    # Any characters you want to ignore when comparing
    unwanted_characters = ".,!?"

    string1_words = {word.strip(unwanted_characters) for word in string1_words}
    string2_words = {word.strip(unwanted_characters) for word in string2_words}
    common_words = string1_words & string2_words
    print(common_words)


path = "/Users/kyleodin/Documents/GitHub/py-career-page-search/TermSearching/python/"

getAllHTMLfilesInDirectory(path)
exportFileText(htmlFiles)
# TODO: figure out a good way to compare a directory of HTML files to find common skills
# findCommonWords(htmlFilesText)
