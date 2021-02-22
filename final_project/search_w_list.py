from flask import Flask, render_template, request
import re, fileinput, mmap, nltk
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib as mlp
from termcolor import colored
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from nltk.stem.snowball import SnowballStemmer
import os
import ast

documents = []
documents_dict = {}
#found = []
file = open("text_data_list.txt", "r")
contents = file.read()
documents = ast.literal_eval(contents)
file.close()


    
def test_query(query):
    #matches = []

    """Ceates a matric and a term vocabulary"""
    tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2", token_pattern=r"\b\w\w+\-*\'*\.*\"*\w*\b")
    global tf_matrix, terms, t2i
    tf_matrix = tfv.fit_transform(documents).T.todense()
    terms = tfv.get_feature_names()

    if query in terms:      #if query is found in the data
        
        """Creates a term-dictionary index and finds matching documents"""
        t2i = tfv.vocabulary_  # shorter notation: t2i = term-to-index
        hits_list = np.array(tf_matrix[t2i[query]])[0]        
        hits_and_doc_ids = [ (hits, i) for i, hits in enumerate(hits_list) if hits > 0 ]
        ranked_hits_and_doc_ids = sorted(hits_and_doc_ids, reverse=True)

        """Creates a vector from the query, finds matching documents and ranks them"""
        query_vec = tfv.transform([query]).todense()
        scores = np.dot(query_vec, tf_matrix)                
        ranked_scores_and_doc_ids = \
        sorted([ (score, i) for i, score in enumerate(np.array(scores)[0]) if score > 0], reverse=True)

        """Finds the number of matched documents for printing"""
        print("There are " + str(len(ranked_scores_and_doc_ids)) + " documents matching your query:")
#        matches.append(line)

        """Finds information for the printing"""
        for score, i in ranked_scores_and_doc_ids:
            score = "{:.4f}".format(score)
            query_match = re.search(r'\b' + query + r'\b', documents[i].lower())  #Trying to make the find() function to match only exact word like 'cat' and not 'publiCATion'
            snippet_index = query_match.start()                 #Finds an index for a snippet for printing results.
            header = documents[i].split('mv_title')[1]                #Finds the header of an article for printing results.
            body = documents[i].split('mv_title')[2]
            documents_dict[header] = body
            header = str(header)
            snippet = "..."+documents[i][snippet_index:snippet_index+100]+"..."
            snippet = str(snippet)
            print("The score of " + query + " is {:.4} in the document named: {:s}. Here is a snippet: ...{:s}...\n***".format(score, header, documents[i][snippet_index:snippet_index+100]))

    else:       #if query is not found in the data
        print("Search term " + query + " not found.")

def main():
    query = input("Tell me your query: ")
    query = query.lower()
    #if query:
     #   query = query.lower()
   # elif choice == "wildcard":
    #    test_wcquery(query)
        
    #elif choice ==  "exact":
    test_query(query)
     

main()








