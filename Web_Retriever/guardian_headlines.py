"""This program accesses the Guardian World News website, retrieves text from it and
prints the ten top headlines."""

import nltk, requests
from bs4 import BeautifulSoup
lista = []
cleanlist = []

def main():
    url = "https://www.theguardian.com/world"
    html = requests.get(url)
  #  html[:60]
    page = html.content
    soup = BeautifulSoup(page, 'html.parser')
    for i in soup.find_all(class_="fc-item__title"):
        i = i.get_text()
        i = str(i).strip()
        if len(lista) < 10:
            lista.append(i)
    for i in lista:
        i = str(i).replace('  ',' ')
        cleanlist.append(i)
    print(*cleanlist, sep ='\n')
main()