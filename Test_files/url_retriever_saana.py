import nltk, requests, datetime, webbrowser, re, pprint
from bs4 import BeautifulSoup
from termcolor import colored
from urllib import request
from nltk import word_tokenize

"""This program retrieves news titles from www.bbc.com/world """
"""and tries to extract the corresponding links but this feature does not work yet"""


def main():
    url = "https://www.bbc.com/news/world"
    html = request.urlopen(url).read().decode('utf8')

    soup = BeautifulSoup(html, 'html.parser')

    linkit = []
    lista =[]
    
    for i in soup.find_all(class_="gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor"):
        i = i.get_text()
        i = str(i).strip()
        i = str(i).replace('  ',' ')
        if len(lista) < 10:
            lista.append(i)

                        
    #this for-loop extracts the url links corresponding the headlines
    for link in soup.find_all(class_="gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor"):
        link = link.get("href")
        if len(linkit) < 10: #appends 10 first headlines to a list
            if link[0] == "/":
                link = "https://bbc.com" + link
            linkit.append(link)
        
    print(*lista, sep ='\n*\n')
    print(*linkit, sep ='\n*\n')

main()
