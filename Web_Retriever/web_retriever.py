"""This program accesses a website, retrieves text from it and
prints (what we choose) results."""

import nltk, re, pprint
from bs4 import BeautifulSoup
from urllib import request
from nltk import word_tokenize
frequency = {} #Dictionary where tokens are given as keys and their frequencies as values
alphabetical = [] #List that can be sorted alphabetically
length = {} #Dictionary that can be sorted by length of tokens

def main():
    url = "https://www.theguardian.com/world"
    html = request.urlopen(url).read().decode('utf8')
    html[:60]
    raw = BeautifulSoup(html, 'html.parser').get_text()
    tokens = word_tokenize(raw)
    tokens = tokens[110:390]
    text = nltk.Text(tokens)
    text.concordance('gene')
    """This for-loop creates dictonary entries
    with tokens as keys and their frequency as values"""
    for token in text:
        if token in frequency:
            frequency[token] = frequency[token] +1
        else:
            frequency[token] = 1
    """This for-loop adds tokens in the "alphabetical" list"""
         
    for token in text:
        if token not in length:
                length[token] = len(token)
    sorted_alphabetical = sorted(alphabetical, key=str.lower) #Sorts the "alphabetical"
    sorted_freq = sorted(frequency.items(), key = lambda word: -word[1]) #Sorts the "frequency" dictionary by frequency
    sorted_len = sorted(length.items(), key = lambda word: -len(word[0])) #Sorts the "length" dictionary by length of keys

    print()
    print("Ordered by frequency:\n==================")
    for i in sorted_freq:
       print(*i, end="\n")
    print()
    print("Ordered by length:\n==================")
    for i in sorted_len:
       print(*i, end="\n")


main()
