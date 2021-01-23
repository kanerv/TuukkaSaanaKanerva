"""This program accesses the Guardian World News website, retrieves text from it and
prints the ten top headlines."""

import nltk, requests, datetime, webbrowser
from bs4 import BeautifulSoup
lista = []
cleanlist = []

def main():
    url = "https://yle.fi/uutiset/tuoreimmat"
    html = requests.get(url)
    page = html.content
    soup = BeautifulSoup(page, 'html.parser')
    for i in soup.find_all(class_="Typography__StyledResponsiveTypography-sc-1his0m9-1 dxkrlB link-accent"):
        i = i.get_text()
        i = str(i).strip()
        if len(lista) < 10:
            lista.append(i)
    for i in lista:
        i = str(i).replace('  ',' ')
        i = str(i).replace('­','')
        cleanlist.append(i)
    print()
    print(" __     ___      ______ _____  _____ _____            _____ _____ ____  ")
    print(" \ \   / / |    |  ____|_   _|/ ____|  __ \     /\   |  __ \_   _/ __ \ ")
    print("  \ \_/ /| |    | |__    | | | (___ | |__) |   /  \  | |  | || || |  | |")
    print("   \   / | |    |  __|   | |  \___ \|  _  /   / /\ \ | |  | || || |  | |")
    print("    | |  | |____| |____ _| |_ ____) | | \ \  / ____ \| |__| || || |__| |")
    print("    |_|  |______|______|_____|_____/|_|  \_\/_/    \_\_____/_____\____/ ")
    print()
    now = datetime.datetime.now()    
    print("Kello on tällä hetkellä", now.strftime("%Y-%m-%d %H:%M:%S"))
    print()
    print("Tuoreimmat kymmenen uutista ovat:\n")
    print(*cleanlist, sep ='\n')
    
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
