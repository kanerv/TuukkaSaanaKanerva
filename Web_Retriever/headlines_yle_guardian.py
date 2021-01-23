"""This program accesses the Guardian World News website, retrieves text from it and
prints the ten top headlines."""

import nltk, requests, datetime, webbrowser
from bs4 import BeautifulSoup
from termcolor import colored


def main():
    open_site = "refresh"
    while open_site == "refresh":
        lista = []
        cleanlist = []
        url = "https://yle.fi/uutiset/tuoreimmat"
        #next lines of code extract the source code of the website and analyse its contents
        html = requests.get(url)
        page = html.content
        soup = BeautifulSoup(page, 'html.parser')
        #this for-loop finds all cases of the html class that have headlines.
        for i in soup.find_all(class_="Typography__StyledResponsiveTypography-sc-1his0m9-1 dxkrlB link-accent"):
            i = i.get_text() #cleans html markup
            i = str(i).strip() #cleans extra white rows
            if len(lista) < 10: #appends 10 first headlines to a list
                lista.append(i)
        for i in lista:
            i = str(i).replace('  ',' ') #cleans extra white space and hyphenation from the headlines
            i = str(i).replace('­','')
            cleanlist.append(i)
        print()
        print (colored(" __     ___      ______ _____  _____ _____            _____ _____ ____  ", "blue"))
        print (colored(" \ \   / / |    |  ____|_   _|/ ____|  __ \     /\   |  __ \_   _/ __ \ ", "blue"))
        print (colored("  \ \_/ /| |    | |__    | | | (___ | |__) |   /  \  | |  | || || |  | |", "blue"))
        print (colored("   \   / | |    |  __|   | |  \___ \|  _  /   / /\ \ | |  | || || |  | |", "blue"))
        print (colored("    | |  | |____| |____ _| |_ ____) | | \ \  / ____ \| |__| || || |__| |", "blue"))
        print (colored("    |_|  |______|______|_____|_____/|_|  \_\/_/    \_\_____/_____\____/ ", "blue"))
        print()
        now = datetime.datetime.now() #creates a variable that contains current time
        print("Kello on tällä hetkellä", now.strftime("%Y-%m-%d %H:%M:%S")) #print current time
        print()
        print("Tuoreimmat kymmenen uutista ovat:\n")
        print(*cleanlist, sep ='\n*\n') #prints headlines on separate rows
        
        """The following code is exactly the same as the first half until "open_site" """
        lista2 = []
        cleanlist2 = []
        url = "https://www.theguardian.com/world"
        html = requests.get(url)
        page = html.content
        soup = BeautifulSoup(page, 'html.parser')
        for i in soup.find_all(class_="fc-item__title"):
            i = i.get_text()
            i = str(i).strip()
            if len(lista2) < 10:
                lista2.append(i)
        for i in lista2:
            i = str(i).replace('  ',' ')
            cleanlist2.append(i)
        print("***********")
        print()
        print(colored("   _____                     _ _             ", "cyan"))
        print(colored("  / ____|                   | (_)            ", "cyan"))
        print(colored(" | |  __ _   _  __ _ _ __ __| |_  __ _ _ __  ", "cyan"))
        print(colored(" | | |_ | | | |/ _` | '__/ _` | |/ _` | '_ \ ", "cyan"))
        print(colored(" | |__| | |_| | (_| | | | (_| | | (_| | | | |", "cyan"))
        print(colored("  \_____|\__,_|\__,_|_|  \__,_|_|\__,_|_| |_|", "cyan"))
        print()
        print("Time is", now.strftime("%Y-%m-%d %H:%M:%S"))
        print()
        print("The first ten headlines from Guardian World News website are:\n")
        print(*cleanlist2, sep ='\n*\n')
        print()
        print()
        print("***********")
        #Now the program asks for input on what the user wants to do, i.e. open a website, refresh the headlines, or quit.
        open_site = input("If you want to open YLE, Guardian or both websites, write \"yle\", \"guardian\", or \"both\", respectively. \nTo refresh, write \"refresh\". To quit, press enter: ") 
        if open_site == "yle":
            webbrowser.open('https://www.yle.fi/uutiset/tuoreimmat', new=2)
        elif open_site == "guardian":
            webbrowser.open('https://www.theguardian.com/world', new=2)
        elif open_site == "both":
            webbrowser.open('https://www.yle.fi/uutiset/tuoreimmat', new=2)
            webbrowser.open('https://www.theguardian.com/world', new=2)
main    ()  
