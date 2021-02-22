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


mlp.use('Agg')

#Initialize Flask instance
app = Flask(__name__)


documents = []
documents_dict = {}
#found = []
file = open("text_data_list.txt", "r")
contents = file.read()
documents = ast.literal_eval(contents)
file.close()

@app.route('/search')
def search():
    os.system('rm -f static/*.png')
    matches = []
    
    #Get query from URL variable
    query = request.args.get('query')
    
    #Get choice of search engine from URL variable
    choice = request.args.get('choice')
    
    #If query exists (i.e. is not None)
    if query:                               
        query = query.lower()
        
        if choice == "stem":     
            query = query + "_s"
            matches = test_query(query)

        elif choice == "wildcard":                      
            matches = test_wcquery(query)
            
        elif choice ==  "exact":    
            matches = test_query(query)

        generate_query_plot(query, graph_matches)
    return render_template('index.html', matches=matches)


def test_query(query):
    matches = []
    global graph_matches
    graph_matches = []
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
        line = "There are " + str(len(ranked_scores_and_doc_ids)) + " documents matching your query:"
        matches.append(line)

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
            line = "The score of " + query + " is "+ score + " in the document named: " + header + "\n" + "Here is a snippet: " + snippet
            matches.append(line)
            graph_matches.append({'name':header,'content':documents[i],'pltpath':header+'_plt.png'})

    else:       #if query is not found in the data
        line = "Search term " + query + " not found."
        matches.append(line)
    return matches

def test_wcquery(query):
    matches = []
    global graph_matches
    graph_matches = []
    """Ceates a matric, a term vocabulary and a list of words matching the wildcard query"""
    tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2", token_pattern=r"\b\w\w+\-*\'*\w*\b")
    global tf_matrix, terms, t2i
    tf_matrix = tfv.fit_transform(documents).T.todense()
    terms = tfv.get_feature_names()
    wc_query = query+".+"
    wc_words = [w for w in terms if re.fullmatch(wc_query, w)]      #this line is copied from the group "wewhoshallnotbenamed"
    
    if wc_words:        #if words matching the query exist

        """Creates a vector from the words matching the wildcard query, finds matching documents and ranks them"""
        new_query_string = " ".join(wc_words)
        query_vec = tfv.transform([new_query_string]).todense()
        scores = np.dot(query_vec, tf_matrix)                
        ranked_scores_and_doc_ids = \
        sorted([ (score, i) for i, score in enumerate(np.array(scores)[0]) if score > 0], reverse=True)

        """Finds the number of matched documents for printing"""
        line = "There are " + str(len(ranked_scores_and_doc_ids)) + " documents matching your query:"
        matches.append(line)

        """Finds information for the printing"""
        for score, i in ranked_scores_and_doc_ids:
            score = "{:.4f}".format(score)
            snippet_index = documents[i].lower().find(query)    #Finds an index for a snippet for printing results.
            header = documents[i].split('mv_title')[1]                #Finds the header of an article for printing results.
            header = str(header)
            snippet = "..."+documents[i][snippet_index:snippet_index+100]+"..."
            snippet = str(snippet)
            line = "The score of " + query + " is "+ score + " in the document named: " + header + "\n" + "Here is a snippet: " + snippet
            matches.append(line)
            graph_matches.append({'name':header,'content':documents[i],'pltpath':header+'_plt.png'})
            
    else:       #if there are no words matching the query
        line = "No matches for wildcard search " + query
        matches.append(line)
        print()
        
    return matches



def generate_query_plot(query, graph_matches):
    # create a figure
    fig = plt.figure()
    plt.title("Word distribution per document \n query: "+query)
    # some values we will use to generate a plot
    dist_dict={}
    for match in graph_matches:
        dist_dict[match['name']] = len(match['content']) 
    # from a dictionary we can create a plot in two steps:
    #  1) plotting the bar chart 
    #  2) setting the appropriate ticks in the x axis
    plt.bar(range(len(dist_dict)), list(dist_dict.values()), align='center', color='g')
    plt.xticks(range(len(dist_dict)), list(dist_dict.keys()),rotation=80) # labels are rotated
    # make room for the labels
    plt.gcf().subplots_adjust(bottom=0.30) # if you comment this line, your labels in the x-axis will be cutted
    plt.savefig('static/query_plot.png')
