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
import pke
import spacy


mlp.use('Agg')

#Initialize Flask instance
app = Flask(__name__)

"""Retrieves data and stores it in a list called documents"""
documents = []
documents_dict = {} #just in case we want to use dictionary
file = open("scraped_data.txt", "r") #file where data is stored
contents = file.read()
documents = ast.literal_eval(contents)
file.close()

"""Ceates a matrix and a term vocabulary"""
global tfv, tf_matrix, terms
tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2", token_pattern=r"\b\w+\-*\'*\.*\"*\w*\b")
tf_matrix = tfv.fit_transform(documents).T.todense()
terms = tfv.get_feature_names()

"""Initializes spacy"""
global nlp, doc
nlp = spacy.load('en_core_web_sm') #loads a small english module


@app.route('/search')
def search():
    os.system('rm -f static/*.png')
    global matches
    matches = []
    
    #Get query from URL variable
    query = request.args.get('query')
    
    #Get choice of search engine from URL variable
    global choice
    choice = request.args.get('choice')
    
    #If query exists (i.e. is not None)
    if query:                               
        query = query.lower()
        matches = test_query(query)

        #generate_query_plot(query, graph_matches)
        generate_adj_plot(query, graph_matches)
        generate_verb_plot(query, graph_matches)
        return render_template('index.html', matches=matches, query=query)
    
    #Returns an empty template for empty searches
    else:
        return render_template('indexempty.html', matches=[])


def test_query(query):
    matches = []
    global graph_matches
    graph_matches = []
    
    if choice:
        if choice == "exact":
            if query in terms:      #if query is found in the data
                matches = relevance_search(query, query)            #searches for query
                
            else:                   #if query is not found in the data
                line = "Search term " + query + " not found."
                matches.append(line)

        elif choice == "wildcard":
            wc_query = query+".*"   #adds the wildcard notation and finds matching words from the data
            wc_words = [w for w in terms if re.fullmatch(wc_query, w)]      #this line is copied from the group "wewhoshallnotbenamed"
            new_query_string = " ".join(wc_words)   #creates a new query from the matching words
            
            if wc_words:            #if words matching the query exist
                matches = relevance_search(query, new_query_string) #searches for the query
                   
            else:                   #if query is not found in the data
                line = "Search term " + query + " not found."
                matches.append(line)
                
    return matches


def relevance_search(orig_query, query):
    snippets = []
            
    """Creates a vector from the query, finds matching documents and ranks them"""
    query_vec = tfv.transform([query]).todense()
    scores = np.dot(query_vec, tf_matrix)                
    ranked_scores_and_doc_ids = \
    sorted([ (score, i) for i, score in enumerate(np.array(scores)[0]) if score > 0], reverse=True)

    """Finds the number of matched documents for printing"""
    line = "There are " + str(len(ranked_scores_and_doc_ids)) + " documents matching your query:"
    matches.append(line)

    """Finds information for printing results"""
    for score, i in ranked_scores_and_doc_ids:
        score = "{:.4f}".format(score)
        header = documents[i].split('mv_title')[1]                              #Finds the header of an article for printing results.
        body = documents[i].split('mv_title')[2]                                #Finds the body of the texct
        documents_dict[header] = body                                           #We might not need this                                                                                          
        line = "The score of " + orig_query + " is "+ score + " in the document named: " + header + "\n\n" + "Here is the review:\n" + body + "\n"
        matches.append(line)
        graph_matches.append({'name':header,'content':documents[i],'pltpath':header+'_plt.png'})

    """Finds themes"""
    f = open("document.txt", "a") #document from which extractor will create themes
    f.write(str(snippets))
    f.close()
    keyphrases = extractor() #retrieves the themes and weights from extractor
    keyphrases_str = '\n'.join(str(v) for v in keyphrases)
            
    """I'm sure this can be done better but just wanted to clean up the display in webGUI"""
    matches.append("Themes:\n")
    for i in keyphrases:
        i = str(i)
        i = re.sub("\(\'", "", i)
        i = re.sub("\)", "", i)
        i = re.sub("\'", "", i)
        matches.append(i)
    return matches        

"""def generate_query_plot(query, graph_matches):

    # create dictionary
    dist_dict={}
    for match in graph_matches:
        dist_dict[match['name']] = len(match['content'])
        
    #scatterplot
    #fig = plt.figure()
    #plt.title("Word distribution per document \n query: "+query)
    #var_1 = list(dist_dict.values())
    #var_2 = list(dist_dict.keys())
    #plt.scatter(var_1,var_2,color='C2')
    #plt.savefig(f'static/query_{query}_plot.png')

    #bar plot
    #fig2 = plt.figure()
    #plt.bar(range(len(dist_dict)), list(dist_dict.values()), align='center', color='g')
    #plt.xticks(range(len(dist_dict)), list(dist_dict.keys()),rotation=80)   # labels are rotated
    #plt.gcf().subplots_adjust(bottom=0.30)                                  # if you comment this line, your labels in the x-axis will be cutted
    #plt.savefig(f'static/query_{query}_plot_bar.png')"""

def generate_adj_plot(query, graph_matches):
    # create dictionary
    dist_dict={}
    adjectives = []
    for match in graph_matches:
        doc = nlp(match['content'])
        adjectives = [token.lemma_ for token in doc if token.pos_ == "ADJ"]
        #print(adjectives)
        for adj in adjectives:
            if adj in dist_dict.keys():
                dist_dict[adj] = dist_dict[adj] + 1
            else:
                dist_dict[adj] = 1
    
    #bar plot
    fig2 = plt.figure()
    plt.bar(range(len(dist_dict)), list(dist_dict.values()), align='center', color='g')
    plt.xticks(range(len(dist_dict)), list(dist_dict.keys()),rotation=80)   # labels are rotated
    plt.gcf().subplots_adjust(bottom=0.30)                                  # if you comment this line, your labels in the x-axis will be cutted
    plt.savefig(f'static/adj_{query}_plot_bar.png')

    
def generate_verb_plot(query, graph_matches):
    #create dictionary
    dist_dict={}
    verbs = []
    for match in graph_matches:
        doc = nlp(match['content'])
        verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
        #print(verbs)
        for verb in verbs:
            if verb in dist_dict.keys():
                dist_dict[verb] = dist_dict[verb] + 1
            else:
                dist_dict[verb] = 1

    #bar plot
    fig2 = plt.figure()
    plt.bar(range(len(dist_dict)), list(dist_dict.values()), align='center', color='g')
    plt.xticks(range(len(dist_dict)), list(dist_dict.keys()),rotation=80)   # labels are rotated
    plt.gcf().subplots_adjust(bottom=0.30)                                  # if you comment this line, your labels in the x-axis will be cutted
    plt.savefig(f'static/verb_{query}_plot_bar.png')


def generate_theme_plot(keyphrases): #creates a scatterplot by theme and weight
    fig = plt.figure()
    plt.title("Themes weighted: ")
    plt.bar(range(len(keyphrases.keys())), list(keyphrases.values()), align='center', color='g')
    plt.xticks(range(len(keyphrases)), list(keyphrases.keys()), rotation=60)   # labels are rotated
    plt.gcf().subplots_adjust(bottom=0.50)                                  # if you comment this line, your labels in the x-axis will be cutted
    

    #var_1 = list(keyphrases.values())
    #var_2 = list(keyphrases.keys())
    #plt.scatter(var_1,var_2,color='C2')
    plt.savefig(f'static/theme_plot.png')
    

def extractor(): #extracts important words from the search results
    keyphrases = []
    extractor = pke.unsupervised.TopicRank()
    extractor.load_document("document.txt", language='en')
    extractor.candidate_selection()
    extractor.candidate_weighting()
    keyphrases = extractor.get_n_best(n=10)
    theme_dict = {k:v for k, v in keyphrases}
    generate_theme_plot(theme_dict)
    
    return keyphrases
