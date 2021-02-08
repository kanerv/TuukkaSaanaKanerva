import re, fileinput, mmap, nltk
from tqdm import tqdm
from termcolor import colored
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from nltk.stem.snowball import SnowballStemmer

#########################################
#This program is a search engine        #
#created for Building NLP Apllications  #
#week 3 assignment.                     #
#########################################

def main():
    
    

    try:
        teksti = []
        documents = []

        pattern = r'(?u)\b\w+\b' #a new regex that takes into account tokens comprised of a singe alphanumerical character
        print(colored("This is TuukkaSaanaKanerva's search engine.", "green"))
        path = input("Please input file path: ")
        
        def get_num_lines(path): #function to find out file size for progress bar
            fp = open(path, "r+")
            buf = mmap.mmap(fp.fileno(), 0)
            lines = 0
            while buf.readline():
                lines += 1
            return lines
        

        with open(path) as file: #opens the file
            for line in tqdm(file, total=get_num_lines(path)): #adds a progress bar
                if len(teksti) < 100000:
                    teksti.append(line)

        text_string = "".join(teksti)
        
        # TRIED TO ADD A STEMMER BUT NOT REALLY WORKING YET, DELETE THE FOLLOWING PARTS IF NOT NEEDED
        #stemmer = SnowballStemmer("english")
        #stemmed_text = stemmer.stem(text_string)
        #documents = stemmed_text.split("</article>") #splits the file into a list at </article>
        #print(documents[1])

        documents_pre = text_string.split("</article>") #splits the file into a list at </article>
        for i in documents_pre:
            i = re.sub("<article name=", "", i)
            i = re.sub(">", "", i)
            documents.append(i)
    
        tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
        global tf_matrix, terms, t2i
        tf_matrix = tfv.fit_transform(documents).T.todense()

        terms = tfv.get_feature_names()
        t2i = tfv.vocabulary_  # shorter notation: t2i = term-to-index

        #def rewrite_query(query): # rewrite every token in the query
        #    print(" ".join(rewrite_token(t) for t in query.split()))
        #    return " ".join(rewrite_token(t) for t in query.split())

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
                    header = snip.split('"')[1]
                    print("The score of " + query + " is {:.4f} in document named: {:s}. Here is a snippet: {:s}\n***".format(score, header, snip[find_first:find_first+50]))
                
            except KeyError:
                print("Search term not found. No Matching doc.")
                

        def test_multiword_query(query):

            #TRYING TO ENABLE MULTI-WORD SEARCHES HERE, IF YOU FIGURE OUT A WAY FEEL FREE TO CHANGE OR DELETE THIS FUNCTION
            #I basically just copied the function from test_query but added ngram_range as a parametre, it doesn't really seem to be working tho
            print("Query: '" + query + "'")
            tfv_ngram = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2", ngram_range=(2,3))
            tf_matrix_ngram = tfv_ngram.fit_transform(documents).T.todense()

            try:
                hits_list = np.array(tf_matrix_ngram[t2i[query]])[0]
                hits_and_doc_ids = [ (hits, i) for i, hits in enumerate(hits_list) if hits > 0 ]
                ranked_hits_and_doc_ids = sorted(hits_and_doc_ids, reverse=True)

                #cosine similarity:
                query_vec = tfv_ngram.transform([query]).todense()
                scores = np.dot(query_vec, tf_matrix_ngram)
                print("The documents have the following cosine similarities to the query:")
                ranked_scores_and_doc_ids = \
                    sorted([ (score, i) for i, score in enumerate(np.array(scores)[0]) if score > 0], reverse=True)

                for score, i in ranked_scores_and_doc_ids:
                    print("The score of " + query + " is {:.4f} in document: {:.100s}".format(score, documents[i]))
                
            except KeyError:
                print("Search term not found. No Matching doc.")

        query = "?"
        while query != "":
            print(colored("We are ready to search!", "green"))
            query = input("Enter a search term: ")
            query = query.lower()
            if re.match(r'\w+ \w+ ?(\w+)?', query):    #Recognizes multi-word queries of two or three words
                test_multiword_query(query)
            elif query != "":
                test_query(query)
            else:
                print("You did not enter a query, bye!")

    except OSError:
        print("Could not find the file. Good bye!")


main()
