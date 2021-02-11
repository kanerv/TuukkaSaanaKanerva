from flask import Flask, render_template, request
import re, fileinput, mmap, nltk
from tqdm import tqdm
from termcolor import colored
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from nltk.stem.snowball import SnowballStemmer

#Initialize Flask instance
app = Flask(__name__)

documents = []
file_variable = open("enwiki-20181001-corpus.100-articles.txt", "r+")
text_string = file_variable.read()


#Function search() is associated with the address base URL + "/search"
@app.route('/search')
def search():
    matches = []
    #Get query from URL variable
    query = request.args.get('query')

    #Initialize list of matches
    #matches = []
    
    #If query exists (i.e. is not None)
    if query:
        query = query.lower()
        if re.match(r'\w+_s\b', query):             #Recognizes stem searches
            print("Searching a stem...")
            documents = stem(text_string)
            matches = test_query(query)

        elif re.match(r'\w+\*', query):             #Recognizes wildcard queries that end with a wildcard
            documents = relevance(text_string)
            queries = []
            for article in documents:               #Iterates through the articles
                words = article.split()
                for word in words:
                    word = word.lower()
                    if re.match(query[:-1]+".+", word):    #Finds all possible queries matching the initial query
                        while re.match(r'\W', word[-1]):     #gets rid of punctuation at the end of word    
                            word = word[:-1]
                        while re.match(r'\W', word[0]):      #gets rid of punctuation in the beginning of word
                            word = word[1:]
                        if word not in queries:             #saves all matching queries
                            queries.append(word)
            for query in queries:
                #print(query)
                matches = test_query(query)                   #Searches with all queries separately

        elif query != "":
            documents = relevance(text_string)
            matches = test_query(query)
        
        #Look at each entry in the example data
        #for entry in example_data:
            #If an entry name contains the query, add the entry to matches
            #if query.lower() in entry['name'].lower():
                #matches.append(entry)

    #Render index.html with matches variable
    return render_template('index.html', matches=matches)

def relevance(documents_in):
            
    documents_pre = documents_in.split("</article>") #splits the file into a list at </article>
    for i in documents_pre:
        i = re.sub("<article name=", "", i)
        i = re.sub(">", "", i)
        documents.append(i)

    return documents
            

def stem(documents_in):
    stem_words = []
    documents_pre = []
    documents_out = []
    tokenized = []
        
    tokens = [w for w in nltk.word_tokenize(documents_in)] #tokenises the text

    """this stems the tokens and creates a list of stemmed words"""
    snowball = SnowballStemmer("english")
    for w in tokens:
            x = snowball.stem(w)
            x = x + "_s"
            stem_words.append(x)
    stemmed_text = " ".join(stem_words)
    documents_pre = stemmed_text.split("<_s /articl_s >_s")

    """This cleans the list from xml code in headers and appends stemmed tokens to documents"""
    for i in documents_pre:
        i = re.sub("<_s articl_s name=_s ''_s", "\"", i)
        i = re.sub("''_s >", "\"", i)
        documents_out.append(i)

    return documents_out

def test_query(query):
    matches = []
    """Ceates a matric and term-dictionary index"""
    tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
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

    print("There are ", len(ranked_scores_and_doc_ids), " documents matching your query:")

    for score, i in ranked_scores_and_doc_ids:
        snippet_index = documents[i].lower().find(query)    #Finds an index for a snippet for printing results.
        header = documents[i].split('"')[1]                 #Finds the header of an article for printing results.
        matches.append(header)
        #print("The score of " + query + " is {:.4f} in the document named: {:s}. Here is a snippet: ...{:s}...\n***".format(score, header, documents[i][snippet_index:snippet_index+100]))
    
    return matches


