import nltk, requests, datetime, webbrowser
from bs4 import BeautifulSoup
from termcolor import colored

def main():
	linkit = []

	url = "https://yle.fi/uutiset/tuoreimmat"

	#next lines of code extract the source code of the website and analyse its contents
	html = requests.get(url)
	page = html.content
	soup = BeautifulSoup(page, 'html.parser')
    
	#this for-loop extracts the url links corresponding the headlines
	for link in soup.find_all(class_="Typography__StyledResponsiveTypography-sc-1his0m9-1 dxkrlB link-accent"):
		link = link.get("href")
		if len(linkit) < 10: #appends 10 first headlines to a list
			linkit.append(link)
                   
	print(linkit)

main()
