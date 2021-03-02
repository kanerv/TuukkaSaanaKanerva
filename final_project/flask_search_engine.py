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

"""Initialize Flask instance"""
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
global nlp
nlp = spacy.load('en_core_web_sm') #loads a small english module

@app.route('/search')
def search():
    os.system('rm -f static/*.png')
    global matches, graph_matches
    matches = []
    graph_matches = []
    
    #Get query from URL variable
    query = request.args.get('query')
    query = str(query)
    query = query.lower()
    
    #Get choice of search engine from URL variable
    global choice
    choice = request.args.get('choice')

    #Defining variables for wildcard search
    wc_query = query+".*"                                       #adds the wildcard notation and finds matching words from the data
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
                matches, graph_matches = relevance_search(query, query) #searches for exact query

                generate_distribution_plot(query, graph_matches) #generates distribution plot
                generate_adj_plot(query, graph_matches)     #generates an adjective plot
                extractor(query, graph_matches)             #extracts themes and generates a theme plot
                generate_verb_plot(query, graph_matches)    #generates a verb plot
                generate_pos_plot(query, graph_matches)     #generates a PoS plot
                return render_template('index.html', matches=matches, query=query)
                
            if choice == "wildcard":
                new_query_string = " ".join(wc_words)   #creates a new query from the matching words
                print("doing a wildcard search for: ", query)
                matches, graph_matches = relevance_search(query, new_query_string) #searches for wildcard query

                generate_distribution_plot("wildcard_"+query, graph_matches) #generates distribution plot
                generate_adj_plot("wildcard_"+query, graph_matches)     #generates an adjective plot
                extractor("wildcard_"+query, graph_matches)             #extracts themes and generates a theme plot
                generate_verb_plot("wildcard_"+query, graph_matches)    #generates a verb plot
                generate_pos_plot("wildcard_"+query, graph_matches)     #generates a PoS plot
                return render_template('index.html', matches=matches, query="wildcard_"+query)            

        #Show empty template in the beginning
        else:
            return render_template('indexempty.html', matches=[])
    
    #Returns an empty template for empty searches
    else:
        return render_template('indexempty.html', matches=[])


def relevance_search(orig_query, query):
    snippets = []
    matches = []
    graph_matches = []
            
    """Creates a vector from the query, finds matching documents and ranks them"""
    query_vec = tfv.transform([query]).todense()
    scores = np.dot(query_vec, tf_matrix)                
    ranked_scores_and_doc_ids = \
    sorted([ (score, i) for i, score in enumerate(np.array(scores)[0]) if score > 0], reverse=True)

    """Finds the number of matched documents for printing"""
    line = "<h4 style=font-family:'Courier New';>There are " + str(len(ranked_scores_and_doc_ids)) + " documents matching your query <i>" + query +"</i>:</h4><br>"
    matches.append(line)

    """Finds information for printing results"""
    try:
        for score, i in ranked_scores_and_doc_ids:
            score = "{:.4f}".format(score)
            header = documents[i].split('mv_title')[1]              #Finds the header of an article for printing results.
            body = documents[i].split('mv_title')[2]                #Finds the body of the texct                          
            doc_html = nlp(body)                                    #Creates an object for ner recognition
            html = displacy.render(doc_html, style="ent", minify=True)  #Creates ner highlights
                                                                 
            line = "<h4 style=font-family:'Courier New';>&#127813; The score of <i> " + orig_query + "</i> is "+ score + " in the document named: <em>" + header + "</em></b></h4>\n\n" + "<h4 style=font-family:'Courier New';>Here is the review:</h4>" + html

            matches.append(line)
            graph_matches.append({'name':header,'content':body,'pltpath':header+'_plt.png'})
            
    except IndexError:
        line = "There was a problem with the search"
        matches.append(line)    
               
    return matches, graph_matches

def generate_distribution_plot(query, graph_matches):
    """Generates a barplot of the distribution of the query word in the movie reviews"""
    fig1 = plt.figure()
    plt.title("Distribution of your query per review")
    dist_dict1={}
    for match in graph_matches:
        dist_dict1[match['name']] = len(match['content']) 
    plt.bar(range(len(dist_dict1)), list(dist_dict1.values()), align='center', color="r")
    plt.xticks(range(len(dist_dict1)), list(dist_dict1.keys()),rotation=60) # labels are rotated
    # make room for the labels
    plt.gcf().subplots_adjust(bottom=0.50) # if you comment this line, your labels in the x-axis will be cutted
    plt.savefig(f'static/distribution_{query}_plot.png')

def generate_adj_plot(query, graph_matches):
    """Generates a pieplot of the most frequent adjectives from the search results"""
    
    #Creates a dictionary and uses it to track adjective frequency
    dist_dict={}
    adjectives = []
    for match in graph_matches:
        doc = nlp(match['content'])
        adjectives = [token.lemma_ for token in doc if token.pos_ == "ADJ"]
        for adj in adjectives:
            if len(adj)>1:      #skipping punctuation marks that spacy incorrectly classifies as adjectives
                if adj in dist_dict.keys():
                    dist_dict[adj] = dist_dict[adj] + 1
                else:
                    dist_dict[adj] = 1
            else:
                continue
                
    #Ranks the adjectives in a list according to frequency
    ranked_adjectives = []
    highest_adj_count = 0
    for adj in dist_dict.keys():
        if dist_dict[adj] >= highest_adj_count:
            ranked_adjectives.insert(0, adj)
            highest_adj_count = dist_dict[adj]
        else:
            ranked_adjectives.append(adj)

    #Creates pie charts for top10 or all adjectives
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

    print("adjectives for ", query, " are: ", labels)
    plt.savefig(f'static/adj_{query}_plot_pie.png')

    
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
    plt.title("Your query has the following verb distribution")
    plt.bar(range(len(dist_dict)), list(dist_dict.values()), align='center', color='g')
    plt.xticks(range(len(dist_dict)), list(dist_dict.keys()),rotation=80)   # labels are rotated
    plt.gcf().subplots_adjust(bottom=0.30)                                  # if you comment this line, your labels in the x-axis will be cutted
    plt.savefig(f'static/verb_{query}_plot_bar.png')

    #Ranks the verbs in a list according to frequency
    ranked_verbs = []
    highest_verb_count = 0
    for verb in dist_dict.keys():
        if dist_dict[verb] >= highest_verb_count:
            ranked_verbs.insert(0, verb)
            highest_verb_count = dist_dict[verb]
        else:
            ranked_verbs.append(verb)

    #Creates pie charts for top10 or all verbs
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


def generate_theme_plot(query, keyphrases):
    """Creates a scatterplot by theme and weight"""
    fig = plt.figure()
    plt.title("Theme distribution of your query")
    plt.bar(range(len(keyphrases.keys())), list(keyphrases.values()), align='center', color='r')
    plt.xticks(range(len(keyphrases)), list(keyphrases.keys()), rotation=60)   # labels are rotated
    plt.gcf().subplots_adjust(bottom=0.50)              # if you comment this line, your labels in the x-axis will be cutted
    
    #var_1 = list(keyphrases.values())
    #var_2 = list(keyphrases.keys())
    #plt.scatter(var_1,var_2,color='C2')
    plt.savefig(f'static/theme_{query}_plot.png')
    

def extractor(query, graph_matches):
    """Finds themes and calls the theme plot generator"""
    
    snippets = []
    for match in graph_matches:
        snippets = match['content']
        
    f = open("document.txt", "w") #document from which extractor will create themes
    f.write(str(snippets))
    f.close()
     
    """Extracts important words from the search results"""
    keyphrases = []
    extractor = pke.unsupervised.TopicRank()
    extractor.load_document("document.txt", language='en')
    extractor.candidate_selection()
    extractor.candidate_weighting()
    keyphrases = extractor.get_n_best(n=10)
    theme_dict = {k:v for k, v in keyphrases}
    generate_theme_plot(query, theme_dict)  #calls for theme plot generator
    #keyphrases_str = '\n'.join(str(v) for v in keyphrases)

def generate_pos_plot(query, graph_matches):
    """Generates a pie plot of the distribution of PoS tagged content"""
    
    #Creates a dictionary and uses it to track PoS frequency
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

    #Creates a bar plot for all tags
    bar_fig = plt.figure()
    plt.title("Part-of-speech tag distribution")
    plt.bar(range(len(dist_dict)), list(dist_dict.values()), align='center', color='r')
    plt.xticks(range(len(dist_dict)), list(dist_dict.keys()),rotation=80)   # labels are rotated
    plt.gcf().subplots_adjust(bottom=0.30)                                  # if you comment this line, your labels in the x-axis will be cutted
    plt.savefig(f'static/pos_{query}_plot_bar.png')

