import nltk, requests, datetime, webbrowser, re, pprint
from bs4 import BeautifulSoup
from termcolor import colored
from urllib import request
from nltk import word_tokenize

"""This program retrieves news titles from www.reuters.com/world """
"""and tries to extract the corresponding links but this feature does not work yet"""


def main():
    url = "https://www.reuters.com/world"
    html = request.urlopen(url).read().decode('utf8')
    #html [:60]

    soup = BeautifulSoup(html, 'html.parser')#.get_text()

    linkit = []
    lista =[]
    
    for i in soup.find_all(class_="story-title"):
        i = i.get_text()
        i = str(i).strip()
        i = str(i).replace('  ',' ')
        if len(lista) < 10:
            lista.append(i)

                        
    #this for-loop extracts the url links corresponding the headlines
    for link in soup.find_all(class_="story-content"):              #The link retrieving doesn't work
        link = link.get("href")
        if len(linkit) < 10: #appends 10 first headlines to a list
            linkit.append(link)
        
    print(*lista, sep ='\n*\n')
    #print(linkit)

main()
