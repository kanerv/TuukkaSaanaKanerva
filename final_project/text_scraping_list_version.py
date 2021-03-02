##################################################
#This is an app to retrieve raw text from Rotten #
#Tomatoes 100 best films list                    #
##################################################

import nltk, requests, datetime, webbrowser
from bs4 import BeautifulSoup
from termcolor import colored
from urllib import request
import json
import re
import time
import random


headers = {
        'USER-AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0 ACCEPT text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8 ACCEPT-LANGUAGE en-US,en;q=0.5 ACCEPT-ENCODING gzip, deflate, br REFERER https://www.rottentomatoes.com/top/bestofrt/'
}
"""Defining functions"""

def scraper(url):                
        review_links = [] #links to individual film pages
        preview = [] #links to critics consensuses
        titles = []
        
        parser = "html.parser"
        html = requests.get(url, headers)
        soup = BeautifulSoup(html.text, parser) #parses the 100 best films page
        f = open("text_data_list.txt", "a")
        json_content = json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents)) #loads the json script from parsed html page into a python dictionary
        for i in json_content['itemListElement']: #iterates through dictionary
                review_links.append(i['url']) #extracts the url from the dictionary
        
        for i in review_links: #iterates through links to individual pages
            link = requests.get(i, headers) #retrieves the URLs
            page_content = link.content #extracts URL contents from individual film pages
            soup = BeautifulSoup(page_content, 'html.parser') #parses the film page
            for c in soup.find("title"): #extracts page title
                c = re.sub("- Rotten Tomatoes", "", c) #resubs everything else than film's name
                c = re.sub("Rotten Tomatoes: Movies", "", c)
                c = re.sub("--", "-", c)
                print("Title: "+c)
                f.write("\"mv_title "+c+" mv_title ")

            for i in soup.find_all(class_="what-to-know__section-body"): #looks for the tagging for critics consensus
                i = i.get_text() #extracts only the text int he paragraph
                i = re.sub("Read critic reviews", "", i)
                i = re.sub("\n", " ", i)
                i = re.sub("\"", "", i)
                i = re.sub("--", "-", i)
                print("Review: "+i)
                f.write(i+"\", ")
           
            time.sleep(random.uniform(1.1, 10.1))

        print("Finished.")
        f.close()

def main():
        scraper("https://www.rottentomatoes.com/top/bestofrt/?year=2020")      
main()
