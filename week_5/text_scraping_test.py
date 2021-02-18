##################################################
#This is an app to retrieve raw text from a      #
#list of hyperlinks, e.g. guardian headline page #
##################################################

import nltk, requests, datetime, webbrowser
from bs4 import BeautifulSoup
from termcolor import colored
from urllib import request #to make the Reuters retrieval work

"""Defining functions"""

def main():
        lista2 = []
        cleanlist2 = []
        linkit2 = []
        test = []
        url = "https://www.theguardian.com/world"
        html = requests.get(url)
        page = html.content
        soup = BeautifulSoup(page, 'html.parser')
   
        for i in soup.find_all(class_="fc-item__title"):
            i = i.get_text()
            i = str(i).strip()
            i = str(i).replace('  ',' ')
            if len(lista2) < 10:
                lista2.append(i)
                
        #this for-loop extracts the url links corresponding the headlines
        for link in soup.find_all(class_="fc-item__link"):
            link = link.get("href")
            if len(linkit2) < 10: #appends 10 first headlines to a list
                linkit2.append(link)

        
        for i in linkit2:
            link = requests.get(i)
            page_content = link.content
            soup = BeautifulSoup(page_content, 'html.parser')
            for i in soup.find_all(class_='css-38z03z'):
                i = i.string
                test.append(i)
                
                
        for i, (x, y, z) in enumerate(zip(lista2, linkit2, test)):
            print(x, "\nURL:", y, "\nPreview: ", z, "\n*")
        #print(*lista2, sep ='\n*\n')
        print("***********")
        print()
                    
main()
