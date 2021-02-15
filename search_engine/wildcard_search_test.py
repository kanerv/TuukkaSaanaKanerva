#from flask import Flask, render_template, request
import re, fileinput, mmap, nltk
from tqdm import tqdm
from termcolor import colored
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from nltk.stem.snowball import SnowballStemmer

#splits the articles
def relevance(documents_in):
            
    documents_pre = documents_in.split("</article>") #splits the file into a list at </article>
    for i in documents_pre:
        i = re.sub("<article name=", "", i)
        i = re.sub(">", "", i)
        documents.append(i)

    return documents

#changes all words matching the query into wildcards in the data.
def modify_wildcards_in_doc(query, documents_in):
    print(type(documents_in))
    documents_out = []
    wc_word = query+"_wc"
    for article in documents_in:
        words = article.split()
        for word in words:
            word = word.lower()
            if re.match(query+".+", word):
                print("Found a match: " + word)
                words = re.sub(word, wc_word, str(words))
        if wc_word in words:
            print("previous wildcards added to documents!")
        documents_out.append(words)
    return documents_out

#searches for query            
def test_query(query):
    matches = []
    
    """Ceates a matric and term-dictionary index"""
    
    tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2", token_pattern=r"\b\w\w+\-*\'*\w*\b")
    global tf_matrix, terms, t2i
    tf_matrix = tfv.fit_transform(documents).T.todense()
    terms = tfv.get_feature_names()
    t2i = tfv.vocabulary_  # shorter notation: t2i = term-to-index
    hits_list = np.array(tf_matrix[t2i[query]])[0]
    hits_and_doc_ids = [ (hits, i) for i, hits in enumerate(hits_list) if hits > 0 ]

    ranked_hits_and_doc_ids = sorted(hits_and_doc_ids, reverse=True)

    #cosine similarity:
    query_vec = tfv.transform([query]).todense()
    scores = np.dot(query_vec, tf_matrix)                
    ranked_scores_and_doc_ids = \
    sorted([ (score, i) for i, score in enumerate(np.array(scores)[0]) if score > 0], reverse=True)
    #print("There are ", len(ranked_scores_and_doc_ids), " documents matching your query:")

    # Trying to output something if the search doesn't match anything, NOT WORKING YET
    if len(ranked_scores_and_doc_ids) == 0:
        line = "No matches found"
        matches.append(line)
    else:
        for score, i in ranked_scores_and_doc_ids:
            score = "{:.4f}".format(score)
            snippet_index = documents[i].lower().find(query)    #Finds an index for a snippet for printing results.
            header = documents[i].split('"')[1]                #Finds the header of an article for printing results.
            header = str(header)
            snippet = "..."+documents[i][snippet_index:snippet_index+100]+"..."
            snippet = str(snippet)
            line = "The score of " + query + " is "+ score + " in the document named: " + header + "\n" + "Here is a snippet: " + snippet
            matches.append(line)
    print("query: " + query + "\n document: " + header + "\n snippet: " + snippet + "\n ***")
    #print("The score of " + query + " is {:.4f} in the document named: {:s}. Here is a snippet: ...{:s}...\n***".format(score, header, documents[i][snippet_index:snippet_index+100]))
    return matches


#running the program
documents = []
file_variable = open("enwiki-20181001-corpus.100-articles.txt", encoding="utf8")
text_string = file_variable.read()
print("This is a test seach engine for wildcards")
query = input("input query:")

query = query.lower()
documents = relevance(text_string)
documents = modify_wildcards_in_doc(query, documents)

matches = test_query(query+"_wc")               

