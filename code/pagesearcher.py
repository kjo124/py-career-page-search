import html2text
import urllib.request

url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"

response = urllib.request.urlopen(url)
html = response.read()


print(html)
