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

headers = {
        'USER-AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0 ACCEPT text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8 ACCEPT-LANGUAGE en-US,en;q=0.5 ACCEPT-ENCODING gzip, deflate, br'
}

"""Defining functions"""

def main():
        review_links = [] #links to individual film pages
        preview = [] #links to critics consensuses
        titles = []

        url = "https://www.rottentomatoes.com/top/bestofrt/?year=2020" #best 100 films 2016 url
        parser = "html.parser"
        html = requests.get(url, headers)
        soup = BeautifulSoup(html.text, parser) #parses the 100 best films page
        f = open("text_data_list.txt", "a")
        json_content = json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents)) #loads the json script from parsed html page into a python dictionary
        for i in json_content['itemListElement']: #iterates through dictionary
            review_links.append(i['url']) #extracts the url from the dictionary
        
        for i in review_links: #iterates through links to individual pages
            print("Still working...")
            link = requests.get(i) #retrieves the URLs
            page_content = link.content #extracts URL contents from individual film pages
            soup = BeautifulSoup(page_content, 'html.parser') #parses the film page
            for i in soup.find_all(class_="what-to-know__section-body"): #looks for the tagging for critics consensus
                i = i.get_text() #extracts only the text int he paragraph
                i = re.sub("Read critic reviews", "", i)
                i = re.sub("\n", " ", i)
                i = re.sub("\"", "", i)
                preview.append(i)
            for c in soup.find("title"): #extracts page title
                c = re.sub("- Rotten Tomatoes", "", c) #resubs everything else than film's name
                titles.append("mv_title"+c+" mv_title")
            time.sleep(1)
        f.write("[\n")
        for i, (k, y, z) in enumerate(zip(titles, review_links, preview)):
            f.write("\""+k)
            f.write(z+"\", ")
            #print("Film: ", k, "\nURL:", y, "\nPreview: ", z, "\n*")
        print("Finished.")
        print()
        f.write("]")
        f.close()        
main()
