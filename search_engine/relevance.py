import re, fileinput, mmap
from tqdm import tqdm
from termcolor import colored
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

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
        documents = text_string.split("</article>") #splits the file into a list at </article>
        
        tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
        global tf_matrix, t2i
        tf_matrix = tfv.fit_transform(documents).T.todense()

        terms = tfv.get_feature_names()
        t2i = tfv.vocabulary_  # shorter notation: t2i = term-to-index

        def rewrite_query(query): # rewrite every token in the query
            return " ".join(rewrite_token(t) for t in query.split())

        def test_query(query):
            print("Query: '" + query + "'")

            try:
                hits_list = np.array(tf_matrix[t2i[query]])[0]
                hits_and_doc_ids = [ (hits, i) for i, hits in enumerate(hits_list) if hits > 0 ]
                print("List of tuples (hits, doc_idx) where hits > 0:", hits_and_doc_ids)

                ranked_hits_and_doc_ids = sorted(hits_and_doc_ids, reverse=True)
                print("Ranked (hits, doc_idx) tuples:", ranked_hits_and_doc_ids)

                print("\nMatched the following documents, ranked highest relevance first:")
                for hits, i in ranked_hits_and_doc_ids:
                    print("Score of " + query + " is {:.4f} in document: {:.50s}".format(hits, documents[i]))

                print("Hits:", hits_list)

               
                
                
            except KeyError:
                print("Search term not found. No Matching doc.")         

        query = "?"
        while query != "":
            print(colored("We are ready to search!", "green"))
            print("You can use AND, OR, NOT, as parametres.\nHyphenated words are regarded as separate words.\n***\nIf you want to quit press enter.\n")
            query = input("Enter a search term: ")
            query = query.lower()
            if re.match(r'\w+\s(NOT|not)\s\w+', query):  # Prints an error message if the user enters a search like 'word NOT word'
                print(colored("Parameter not used correctly, try using 'AND NOT' instead of 'NOT'", "red"))
            elif query != "":
                test_query(query)
            else:
                print("You did not enter a query, bye!")

    except OSError:
        print("Could not find the file. Good bye!")


main()
