###############################################
# This program accesses the YLE and Guardian  #
# news websites, retrieves text from them and #
# prints the top ten headlines.               #
# ––––––––––––––––––––––––––––––––––––––––––– #
# This was made for an assignment at the NLP  #
# course KIK-LG211 at University of Helsinki  #
# "NLTK and "termcolor" need to be installed  #
# in order for this program to work.          #
###############################################

import nltk, requests, datetime, webbrowser
from bs4 import BeautifulSoup
from termcolor import colored
from urllib import request #to make the reuter's retrieval work

"""Defining functions"""

def yle_logo():
    print()
    print (colored(" __     ___      ______ _____  _____ _____            _____ _____ ____  ", "blue"))
    print (colored(" \ \   / / |    |  ____|_   _|/ ____|  __ \     /\   |  __ \_   _/ __ \ ", "blue"))
    print (colored("  \ \_/ /| |    | |__    | | | (___ | |__) |   /  \  | |  | || || |  | |", "blue"))
    print (colored("   \   / | |    |  __|   | |  \___ \|  _  /   / /\ \ | |  | || || |  | |", "blue"))
    print (colored("    | |  | |____| |____ _| |_ ____) | | \ \  / ____ \| |__| || || |__| |", "blue"))
    print (colored("    |_|  |______|______|_____|_____/|_|  \_\/_/    \_\_____/_____\____/ ", "blue"))
    print()

def guardian_logo():
    print()
    print(colored("   _____                     _ _             ", "cyan"))
    print(colored("  / ____|                   | (_)            ", "cyan"))
    print(colored(" | |  __ _   _  __ _ _ __ __| |_  __ _ _ __  ", "cyan"))
    print(colored(" | | |_ | | | |/ _` | '__/ _` | |/ _` | '_ \ ", "cyan"))
    print(colored(" | |__| | |_| | (_| | | | (_| | | (_| | | | |", "cyan"))
    print(colored("  \_____|\__,_|\__,_|_|  \__,_|_|\__,_|_| |_|", "cyan"))
    print()

def reuters_logo():
    print()
    print()(colored("__________               __                      ", "red"))
    print()(colored("\______  \ ____  __ ___/  |_  ___________  ______", "red"))
    print()(colored("|       _// __ \|  |  \   __\/ __ \_  __ \/  ___/", "red"))
    print()(colored("|    |   \  ___/|  |  /|  | \  ___/|  | \/\___ \ ", "red"))
    print()(colored("|____|_  /\___  >____/ |__|  \___  >__|  /____  >", "red"))
    print()(colored("       \/     \/                 \/           \/ ", "red"))
    print()
    


def main():
    open_site = "b"
    while open_site == "b":
        interest = input("Would you like to see news from (1) Yle or (2) Guardian or (3) Reuters? Type 1, 2 or 3: ")
        if interest == "1":
            which_headline = input("Haluaisitko nähdä (1) tuoreimmat vai (2) luetuimmat uutisotsikot? Valitse 1 tai 2: ")
            if which_headline == "1":
                
                lista = []
                cleanlist = []     
                linkit = []            

                url = "https://yle.fi/uutiset/tuoreimmat"

                #next lines of code extract the source code of the website and analyse its contents
                html = requests.get(url)
                page = html.content
                soup = BeautifulSoup(page, 'html.parser')

        	#this for-loop extracts the url links corresponding the headlines
                for link in soup.find_all(class_="GridSystem__GridRow-sc-15162af-1 ljWZzL visitableLink"):
                    link = link.get("href")
                    if len(linkit) < 10: #appends 10 first headlines to a list
                        if link[0] == "/": #checks if the link is missing the beginning and adds it if needed
                            link = "https://yle.fi" + link
                        linkit.append(link)


                #this for-loop finds all cases of the html class that have headlines.
                for i in soup.find_all(class_="Typography__StyledResponsiveTypography-sc-1his0m9-1 dxkrlB link-accent"):
                    i = i.get_text()    #cleans html markup
                    i = str(i).strip()  #cleans extra white rows
                    i = str(i).replace('  ',' ') #cleans extra white space and hyphenation from the headlines
                    i = str(i).replace('­','')
                    if len(lista) < 10: #appends 10 first headlines to a list
                        lista.append(i)
                        
                print("***********")
                
                yle_logo() #Calling for the function yle_logo
                
                now = datetime.datetime.now() #creates a variable that contains current time
                print("Kello on tällä hetkellä", now.strftime("%Y-%m-%d %H:%M:%S")) #print current time
                print()
                print("Tuoreimmat kymmenen uutista ovat:\n")

                for i, (x, y) in enumerate(zip(lista, linkit)):
                    print(x, "\nURL:", y, "\n*")

                #for i in lista:
                 #   for c in linkit:
                  #      print(i)
                   #     print(c)
#                print(*lista, sep ='\n*\n') #prints headlines on separate rows
                print("***********")
                print()

            elif which_headline == "2":
                lista3 = []
                cleanlist3 = []
                linkit3 = []
            
                url = "https://yle.fi/uutiset/"

                #next lines of code extract the source code of the website and analyse its contents
                html = requests.get(url)
                page = html.content
                soup = BeautifulSoup(page, 'html.parser')

                #this for-loop finds all cases of the html class that have headlines.
                for i in soup.find_all("h6", class_="Typography__StyledResponsiveTypography-sc-1his0m9-1 dpfFnA link-accent"):
                    i = i.get_text()    #cleans html markup
                    i = str(i).strip()  #cleans extra white rows
                    if len(lista3) < 10: #appends 10 first headlines to a list
                        i = str(i).replace('  ',' ') #cleans extra white space and hyphenation from the headlines
                        i = str(i).replace('­','')
                        lista3.append(i)

                #this for-loop extracts the url links corresponding the headlines
                for link in soup.find_all(class_="Headline__Direction-sc-5nx0d9-0 fAhMa visitableLink"):
                    link = link.get("href")
                    if len(linkit3) < 10: #appends 10 first headlines to a list
                        if link[0] == "/": #checks if the link is missing the beginning and adds it if needed
                            link = "https://yle.fi" + link
                        linkit3.append(link)

                print("***********")
                
                yle_logo()
                
                now = datetime.datetime.now() #creates a variable that contains current time
    
                print("Kello on tällä hetkellä", now.strftime("%Y-%m-%d %H:%M:%S")) #print current time
                print()
                print("Luetuimmat kymmenen uutista ovat:\n")

                for i, (x, y) in enumerate(zip(lista3, linkit3)):
                    print(x, "\nURL:", y, "\n*")
                #print(*lista3, sep ='\n*\n') #prints headlines on separate rows
                print("***********")
                print()
            
            """The following code until "open_site" is exactly the same as the first half"""
            
            
        if interest == "2":
            lista2 = []
            cleanlist2 = []
            linkit2 = []

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
                    
            now = datetime.datetime.now() #creates a variable that contains current time
            
            print("***********")
            guardian_logo()
            print("Time is", now.strftime("%Y-%m-%d %H:%M:%S"))
            print()
            print("The first ten headlines from Guardian World News website are:\n")
            for i, (x, y) in enumerate(zip(lista2, linkit2)):
                print(x, "\nURL:", y, "\n*")
            #print(*lista2, sep ='\n*\n')
            print("***********")
            print()
                    

        if interest == "3":
            lista4 = []
            cleanlist4 = []
            linkit4 = []
            
            """Tried another way of retrieving the website"""
            url = "https://www.reuters.com/world"
            html = request.urlopen(url).read().decode('utf8')
            
            #url = "https://www.reuters.com/world"
            #html = requests.get(url)
            #page = html.content

            soup = BeautifulSoup(html, 'html.parser')
    
            for i in soup.find_all(class_="story-title"):
                i = i.get_text()
                i = str(i).strip()
                i = str(i).replace('  ',' ')
                if len(lista4) < 10:
                    lista4.append(i)
                        
            #this for-loop extracts the url links corresponding the headlines
            #for link in soup.find_all(class_="story-content"):                  #THIS ONE DOESN'T WORK YET, NEED TO FIND THE RIGHT CLASS?
            #    link = link.get("href")
            #    if len(linkit4) < 10: #appends 10 first headlines to a list
            #        linkit4.append(link)
                    
            now = datetime.datetime.now() #creates a variable that contains current time
            
            print("***********")
            reuters_logo()
            print("Time is", now.strftime("%Y-%m-%d %H:%M:%S"))
            print()
            print("The first ten headlines from Reuters World News website are:\n")
            for i, (x, y) in enumerate(zip(lista4)):           #when links work, add linkit4
                print(x, "\nURL:", y, "\n*")
            #print(*lista2, sep ='\n*\n')
            print("***********")
            print()
                    

            """Next, the program asks for input on what the user wants to do, i.e. open a website, refresh the headlines, or quit."""
        
        open_site = input("If you want to open (1) YLE, (2) Guardian or (3) both websites, enter 1, 2 or 3. \nTo go back to choosing your news, enter \"b\". To quit, press enter: ") 
        if open_site == "1":
            webbrowser.open('https://www.yle.fi/uutiset/tuoreimmat', new=2)
            print("Thank you. Goodbye!")
        elif open_site == "2":
            webbrowser.open('https://www.theguardian.com/world', new=2)
            print("Thank you. Goodbye!")
        elif open_site == "3":
            webbrowser.open('https://www.yle.fi/uutiset/tuoreimmat', new=2)
            webbrowser.open('https://www.theguardian.com/world', new=2)
            print("Thank you. Goodbye!")
        if open_site == "":
            print("Thank you. Goodbye!")
main()
