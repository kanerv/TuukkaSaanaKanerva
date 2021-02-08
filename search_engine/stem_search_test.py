import re, fileinput, mmap, nltk
from tqdm import tqdm
from termcolor import colored
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from nltk.stem.snowball import SnowballStemmer
from nltk import word_tokenize

#########################################
#This program is a search engine        #
#created for Building NLP Apllications  #
#week 3 assignment.                     #
#########################################

def main():
    
    

    try:
        stem_words = []
        documents_pre = []
        documents = []
        tokenized = []

        print(colored("This is TuukkaSaanaKanerva's search engine.", "green"))
        path = input("Please input file path: ")
        file_variable = open(path, "r")
        text_string = file_variable.read()

        tokens = [w for w in nltk.word_tokenize(text_string)] #tokenises the text

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
            i = re.sub("<_s articl_s name=_s ''_s", "", i)
            i = re.sub("''_s >", "", i)
            documents.append(i)
            

        """Ceates a matric and term-dictionary index"""
        tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
        global tf_matrix, t2i, stems_matrix
        tf_matrix = tfv.fit_transform(documents).T.todense()
        terms = tfv.get_feature_names()
        t2i = tfv.vocabulary_  # shorter notation: t2i = term-to-index

        

        def test_query(query):
            print("Query: '" + query + "'")

            try:
                hits_list = np.array(tf_matrix[t2i[query]])[0]
                hits_and_doc_ids = [ (hits, i) for i, hits in enumerate(hits_list) if hits > 0 ]
                #print("List of tuples (hits, doc_idx) where hits > 0:", hits_and_doc_ids)

                ranked_hits_and_doc_ids = sorted(hits_and_doc_ids, reverse=True)
                #print("Ranked (hits, doc_idx) tuples:", ranked_hits_and_doc_ids)

                #print("\nMatched the following documents, ranked highest relevance first:")
                #for hits, i in ranked_hits_and_doc_ids:
                    #print("Score of " + query + " is {:.4f} in document: {:.50s}".format(hits, documents[i]))

                #cosine similarity:
                query_vec = tfv.transform([query]).todense()
                
                scores = np.dot(query_vec, tf_matrix)
                print("The documents have the following cosine similarities to the query:")
                ranked_scores_and_doc_ids = \
                sorted([ (score, i) for i, score in enumerate(np.array(scores)[0]) if score > 0], reverse=True)

                for score, i in ranked_scores_and_doc_ids:
                    snip = documents[i]
                    find_first = documents[i].find(query)
                    print("The score of " + query + " is {:.4f} in document: {:.15s}. Here is a snippet: {:s}\n***".format(score, documents[i], snip[find_first:find_first+50]))

            except KeyError:
                print("Search term not found. No Matching doc.")         

        query = "?"
        while query != "":
            print(colored("We are ready to search!", "green"))
            #print("You can use AND, OR, NOT, as parametres.\nHyphenated words are regarded as separate words.\n***\nIf you want to quit press enter.\n")
            query = input("Enter a search term. Please use \"_s\" at the end of the stem: ")
            query = query.lower()
            if query != "":
                test_query(query)
            else:
                print("You did not enter a query, bye!")

    except OSError:
        print("Could not find the file. Good bye!")


main()
