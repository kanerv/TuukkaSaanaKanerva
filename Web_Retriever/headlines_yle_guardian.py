"""This program accesses the YLE and Guardian World News websites, retrieves text from them and
prints the ten top headlines. The user can also visit the websites if there are interesting headlines."""

import nltk, requests, datetime, webbrowser
from bs4 import BeautifulSoup
lista = []
cleanlist = []

def main():
    #The following code retrieves the website, gets its content and analyses it.
    url = "https://yle.fi/uutiset/tuoreimmat"
    html = requests.get(url)
    page = html.content
    soup = BeautifulSoup(page, 'html.parser')
    #This for-loop finds all cases of html class that contains the headlines. These can be found in the source code of the page.
    for i in soup.find_all(class_="Typography__StyledResponsiveTypography-sc-1his0m9-1 dxkrlB link-accent"):
        i = i.get_text() #this cleans the html markup
        i = str(i).strip() #this strips empty rows
        if len(lista) < 10: #This adds the first 10 headlines into a list
            lista.append(i)
    for i in lista:
        i = str(i).replace('  ',' ') #These clean the text strings from white space and hyphenations.
        i = str(i).replace('­','')
        cleanlist.append(i) #appends the cleaned strings into a new list: "cleanlist"
    print()
    print(" __     ___      ______ _____  _____ _____            _____ _____ ____  ")
    print(" \ \   / / |    |  ____|_   _|/ ____|  __ \     /\   |  __ \_   _/ __ \ ")
    print("  \ \_/ /| |    | |__    | | | (___ | |__) |   /  \  | |  | || || |  | |")
    print("   \   / | |    |  __|   | |  \___ \|  _  /   / /\ \ | |  | || || |  | |")
    print("    | |  | |____| |____ _| |_ ____) | | \ \  / ____ \| |__| || || |__| |")
    print("    |_|  |______|______|_____|_____/|_|  \_\/_/    \_\_____/_____\____/ ")
    print()
    now = datetime.datetime.now() #creates a variable with current time and date   
    print("Kello on tällä hetkellä", now.strftime("%Y-%m-%d %H:%M:%S")) # prints time and date
    print()
    print("Tuoreimmat kymmenen uutista ovat:\n")
    print(*cleanlist, sep ='\n') #prints the cleanlist on separate rows

    #This is done exactly the same as the one before
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
    print("   _____                     _ _             ")
    print("  / ____|                   | (_)            ")
    print(" | |  __ _   _  __ _ _ __ __| |_  __ _ _ __  ")
    print(" | | |_ | | | |/ _` | '__/ _` | |/ _` | '_ \ ")
    print(" | |__| | |_| | (_| | | | (_| | | (_| | | | |")
    print("  \_____|\__,_|\__,_|_|  \__,_|_|\__,_|_| |_|")
    print()
    print("Time is", now.strftime("%Y-%m-%d %H:%M:%S"))
    print()
    print("The first ten headlines from Guardian World News website are:\n")
    print(*cleanlist2, sep ='\n')
    print()
    print()
    print("***********")

    #The following lines of code prompts the user with a message that they can open the yle or guardian websites.
    open_site = input("If you want to open YLE, Guardian or both websites, write \"yle\", \"guardian\", or \"both\", respectively: ") 
    if open_site == "yle":
        webbrowser.open('https://www.yle.fi/uutiset/tuoreimmat', new=2)
    elif open_site == "guardian":
        webbrowser.open('https://www.theguardian.com/world', new=2)
    elif open_site == "both":
        webbrowser.open('https://www.yle.fi/uutiset/tuoreimmat', new=2)
        webbrowser.open('https://www.theguardian.com/world', new=2)
    else:
        return
main()
