##################################################
#This is an app to retrieve raw text from Rotten #
#Tomatoes 100 best films list                    #
##################################################

import nltk, requests, datetime, webbrowser
from bs4 import BeautifulSoup
from termcolor import colored
from urllib import request #to make the Reuters retrieval work
import json
import re

"""Defining functions"""

def main():
        review_links = []
        preview = []
        url = "https://www.rottentomatoes.com/top/bestofrt/"
        parser = "html.parser"
        html = requests.get(url)
        soup = BeautifulSoup(html.text, parser)   
        json_content = json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))
        for i in json_content['itemListElement']:
            if len(review_links) < 10:
                review_links.append(i['url'])
        
        for i in review_links:
            link = requests.get(i)
            page_content = link.content
            soup = BeautifulSoup(page_content, 'html.parser')
            for i in soup.find('span', attrs={'data-qa': 'critics-consensus'}):
                i = i.string
                preview.append(i)
                
                
        for i, (y, z) in enumerate(zip(review_links, preview)):
            print("\nURL:", y, "\nPreview: ", z, "\n*")
        print("***********")
        print()
                    
main()
