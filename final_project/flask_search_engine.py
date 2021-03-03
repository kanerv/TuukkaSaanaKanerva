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
from spacy import displacy


mlp.use('Agg')

"""Initializes a Flask instance"""
app = Flask(__name__)

"""Retrieves data and stores it in a list called documents"""
documents = []
file = open("scraped_data.txt", "r") #file where data is stored
contents = file.read()
documents = ast.literal_eval(contents)
file.close()

"""Ceate matrix and a term vocabulary"""
global tfv, tf_matrix, terms
tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2", token_pattern=r"\b\w+\-*\'*\.*\"*\w*\b")
tf_matrix = tfv.fit_transform(documents).T.todense()
terms = tfv.get_feature_names()

"""Initialize SpaCy"""
global nlp
nlp = spacy.load('en_core_web_sm') #loads the small english module


"""Define a search function that is associated with the address base URL + '/search'"""
@app.route('/search')
def search():
    
    #delete previous plots and rewrites variables
    os.system('rm -f static/*.png')
    global matches, graph_matches
    matches = []
    graph_matches = []
    
    #Get query from URL variable
    query = request.args.get('query')
    query = str(query)
    query = query.lower()
    
    #Get the choice of search engine from URL variable
    global choice
    choice = request.args.get('choice')

    #Define variables for wildcard search
    wc_query = query+".*"                                       #add the wildcard notation and finds matching words from the data
    global wc_words
    wc_words = [w for w in terms if re.fullmatch(wc_query, w)]  #this line is copied from the group "wewhoshallnotbenamed"

    """If query exists (i.e. is not None)"""
    if query:
        
        #If query is not found in the data, return a template for no results
        if query not in terms and choice == "exact" or not wc_words and choice == "wildcard":
            return render_template('indexnoresults.html', matches=[], query=query)

        #If query is found, search and return a template for results
        elif query in terms or wc_words:
            
            if choice == "exact":
                print("doing an exact search for: ", query)
                matches, graph_matches = relevance_search(query, query) #search for exact query

                extractor(query, graph_matches)             #extract themes and generate a theme plot
                generate_pos_plot(query, graph_matches)     #generate a PoS plot
                generate_adj_plot(query, graph_matches)     #generate an adjective plot
                generate_verb_plot(query, graph_matches)    #generate a verb plot
                return render_template('index.html', matches=matches, query=query)  #Render index.html with matches variable and choice-specific query
                
            if choice == "wildcard":
                new_query_string = " ".join(wc_words)   #create new query from the matching words
                print("doing a wildcard search for: ", query)
                matches, graph_matches = relevance_search(query, new_query_string) #search for wildcard query

                extractor("wildcard_"+query, graph_matches)             #extract themes and generate a theme plot
                generate_pos_plot("wildcard_"+query, graph_matches)     #generate a PoS plot
                generate_adj_plot("wildcard_"+query, graph_matches)     #generate an adjective plot
                generate_verb_plot("wildcard_"+query, graph_matches)    #generate a verb plot
                return render_template('index.html', matches=matches, query="wildcard_"+query)  #Render index.html with matches variable and choice-specific query
            
        #Show an empty template before any searches
        else:
            return render_template('indexempty.html', matches=[])
    
    #Return an empty template for empty searches
    else:
        return render_template('indexempty.html', matches=[])

"""Search for most relevant documents for query and return matches for printing and generating plots"""
def relevance_search(orig_query, query):
    snippets = []
    matches = []
    graph_matches = []
            
    """Create a vector from the query, find matching documents and rank them"""
    query_vec = tfv.transform([query]).todense()
    scores = np.dot(query_vec, tf_matrix)                
    ranked_scores_and_doc_ids = \
    sorted([ (score, i) for i, score in enumerate(np.array(scores)[0]) if score > 0], reverse=True)

    """Find the number of matched documents for printing and save the line in matches"""
    line = "<h4 style=font-family:'Courier New';>There are " + str(len(ranked_scores_and_doc_ids)) + " movies matching your query <i>" + orig_query +"</i>:</h4><br>"
    matches.append(line)

    """Find information for printing results and generating plots"""
    try:
        for score, i in ranked_scores_and_doc_ids:
            score = "{:.4f}".format(score)
            header = documents[i].split('mv_title')[1]              #Find the header of each matching article.
            body = documents[i].split('mv_title')[2]                #Find the body of the texct                          
            doc_html = nlp(body)                                    #Create an object for ner recognition
            html = displacy.render(doc_html, style="ent", minify=True)  #Create ner highlights                                                           
            line = "<h4 style=font-family:'Courier New';>&#127813; The score of <i> " + orig_query + "</i> is "+ score + " in the movie named: <em>" + header + "</em></b></h4>\n\n" + "<h4 style=font-family:'Courier New';>Here is the review:</h4>" + html
            matches.append(line)
            graph_matches.append({'name':header,'content':body,'pltpath':header+'_plt.png'})
            
    except IndexError:
        line = "There was a problem with the search"
        matches.append(line)    
               
    return matches, graph_matches


def generate_theme_plot(query, keyphrases):
    """Generage a bar plot by theme and weight"""
    fig = plt.figure()
    plt.title("Theme distribution")
    plt.bar(range(len(keyphrases.keys())), list(keyphrases.values()), align='center', color='r')
    plt.xticks(range(len(keyphrases)), list(keyphrases.keys()), rotation=60)   #rotate labels
    plt.gcf().subplots_adjust(bottom=0.50)              #make room for labels
    
    #var_1 = list(keyphrases.values())
    #var_2 = list(keyphrases.keys())
    #plt.scatter(var_1,var_2,color='C2')
    plt.savefig(f'static/theme_{query}_plot.png')
    

def extractor(query, graph_matches):
    """Find themes and call the theme plot generator"""
    
    snippets = []
    for match in graph_matches:
        snippets = match['content']
        
    f = open("document.txt", "w") #document from which extractor will create themes
    f.write(str(snippets))
    f.close()
     
    """Extract important words from the search results"""
    keyphrases = []
    extractor = pke.unsupervised.TopicRank()
    extractor.load_document("document.txt", language='en')
    extractor.candidate_selection()
    extractor.candidate_weighting()
    keyphrases = extractor.get_n_best(n=10)
    theme_dict = {k:v for k, v in keyphrases}
    generate_theme_plot(query, theme_dict)  #call theme plot generator
    #keyphrases_str = '\n'.join(str(v) for v in keyphrases)

def generate_pos_plot(query, graph_matches):
    """Generate a bar plot by PoS tagged content"""
    
    #Create a dictionary to track PoS frequency
    dist_dict={}
    pos_tags = []
    for match in graph_matches:
        doc = nlp(match['content'])
        pos_tags = [token.pos_ for token in doc]
        for tag in pos_tags:
            if tag in dist_dict.keys():
                dist_dict[tag] = dist_dict[tag] + 1
            else:
                dist_dict[tag] = 1

    #Create a bar plot for all tags
    bar_fig = plt.figure()
    plt.title("Part-of-speech tag distribution")
    plt.bar(range(len(dist_dict)), list(dist_dict.values()), align='center', color='r')
    plt.xticks(range(len(dist_dict)), list(dist_dict.keys()),rotation=80)   # labels are rotated
    plt.gcf().subplots_adjust(bottom=0.30)                                  # if you comment this line, your labels in the x-axis will be cutted
    plt.savefig(f'static/pos_{query}_plot_bar.png')


def generate_adj_plot(query, graph_matches):
    """Generate a pieplot of the most frequent adjectives from the search results"""   
    #Create a dictionary to track adjective frequency
    dist_dict={}
    adjectives = []
    for match in graph_matches:
        doc = nlp(match['content'])
        adjectives = [token.lemma_ for token in doc if token.pos_ == "ADJ"]
        for adj in adjectives:
            if len(adj)>1:      #skip punctuation marks that spacy incorrectly classifies as adjectives
                if adj in dist_dict.keys():
                    dist_dict[adj] = dist_dict[adj] + 1
                else:
                    dist_dict[adj] = 1
            else:
                continue
                
    #Rank the adjectives in a list according to frequency
    ranked_adjectives = []
    highest_adj_count = 0
    for adj in dist_dict.keys():
        if dist_dict[adj] >= highest_adj_count:
            ranked_adjectives.insert(0, adj)
            highest_adj_count = dist_dict[adj]
        else:
            ranked_adjectives.append(adj)

    #Create a pie chart for top10 or all adjectives
    if len(ranked_adjectives) >= 10:
        top_10_adjectives = []
        remaining_adj_count = 0
        top_10_adjectives = ranked_adjectives[0:9]
        for adj in ranked_adjectives[10:]:
            remaining_adj_count =+ dist_dict[adj]
        dist_dict['Other'] = remaining_adj_count
        top_10_adjectives.append('Other')
        #Pie chart for top 10 adjectives
        pie_fig = plt.figure()
        labels = top_10_adjectives
        sizes = [dist_dict[adj] for adj in top_10_adjectives]
        pie_fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
        ax.set_title("Most frequent adjectives")
    else:
        #Pie chart for all
        pie_fig = plt.figure()
        labels = dist_dict.keys()
        sizes = dist_dict.values()
        pie_fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
        ax.set_title("Most frequent adjectives")

    plt.savefig(f'static/adj_{query}_plot_pie.png')
    
  
def generate_verb_plot(query, graph_matches):
    """Generate a pieplot of the most frequent verbs from the search results""" 
    #create a dictionary to track verb frequency
    dist_dict={}
    verbs = []
    for match in graph_matches:
        doc = nlp(match['content'])
        verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
        for verb in verbs:
            if verb in dist_dict.keys():
                dist_dict[verb] = dist_dict[verb] + 1
            else:
                dist_dict[verb] = 1

    #Rank the verbs in a list according to frequency
    ranked_verbs = []
    highest_verb_count = 0
    for verb in dist_dict.keys():
        if dist_dict[verb] >= highest_verb_count:
            ranked_verbs.insert(0, verb)
            highest_verb_count = dist_dict[verb]
        else:
            ranked_verbs.append(verb)

    #Create pie charts for top10 or all verbs
    if len(ranked_verbs) >= 10:
        top_10_verbs = []
        remaining_verb_count = 0
        top_10_verbs = ranked_verbs[0:9]
        for verb in ranked_verbs[10:]:
            remaining_verb_count =+ dist_dict[verb]
        dist_dict['Other'] = remaining_verb_count
        top_10_verbs.append('Other')
        #Pie chart for top 10 adjectives
        pie_fig = plt.figure()
        labels = top_10_verbs
        sizes = [dist_dict[verb] for verb in top_10_verbs]
        pie_fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
        ax.set_title("Most frequent verbs")
    else:
        #Pie chart for all
        pie_fig = plt.figure()
        labels = dist_dict.keys()
        sizes = dist_dict.values()
        pie_fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
        ax.set_title("Most frequent verbs")
        
    plt.savefig(f'static/verb_{query}_plot_pie.png')
