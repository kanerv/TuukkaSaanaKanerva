from sklearn.feature_extraction.text import CountVectorizer
import re

#########################################
#This program is a search engine        #
#created for Building NLP Apllications  #
#week 2 assignment.                     #
#########################################

def main():
    
    

    try:

        documents = []

        pattern = r'(?u)\b\w+\b'
 
        file = open("enwiki-20181001-corpus.100-articles.txt", "r")
        file_variable = file.read()
        file_variable = file_variable.split("</article>")
        for i in file_variable:
            documents.append(i)
        file.close()

        
        cv = CountVectorizer(lowercase=True, binary=True, token_pattern=pattern)
        sparse_matrix = cv.fit_transform(documents)

        dense_matrix = sparse_matrix.todense()

        global td_matrix, t2i
        td_matrix = dense_matrix.T   # .T transposes the matrix

        terms = cv.get_feature_names()

        t2i = cv.vocabulary_  # shorter notation: t2i = term-to-index

        # Operators and/AND, or/OR, not/NOT become &, |, 1 -
        # Parentheses are left untouched
        # Everything else interpreted as a term and fed through td_matrix[t2i["..."]]

        d = {"and": "&", "AND": "&",
            "or": "|", "OR": "|",
            "not": "1 -", "NOT": "1 -",
            "(": "(", ")": ")"}          # operator replacements
               
        def rewrite_token(t):
            return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t)) # Can you figure out what happens here?

        def rewrite_query(query): # rewrite every token in the query
            return " ".join(rewrite_token(t) for t in query.split())

        def test_query(query):
            print("Query: '" + query + "'")
            print("Rewritten:", rewrite_query(query))

            #print("Matching:", eval(rewrite_query(query))) # Eval runs the string as a Python command

            #Printing the matches instead of ones and zeros
            try:
                hits_matrix = eval(rewrite_query(query))
                hits_list = list(hits_matrix.nonzero()[1])
                for i, doc_idx in enumerate(hits_list):
                    print("Matching doc #{:d}: {:s}".format(i, documents[doc_idx]))
                    print()

            except KeyError:
                print("Search term not found. No Matching doc.")
                
            


        query = "?"
        while query != "":
            print("This is TuukkaSaanaKanerva's search engine.\nYou can use AND, OR, NOT, as parametres.\nHyphenated words are regarded as separate words.\n***\nIf you want to quit press enter.\n")
            query = input("Enter a search term: ")
            if query != "":
                test_query(query)
            else:
                print("You did not enter a query, bye!")

            #test_query("example AND NOT nothing")
            #test_query("NOT example OR great")
            #test_query("( NOT example OR great ) AND nothing") # AND, OR, NOT can be written either in ALLCAPS
            #test_query("( not example or great ) and nothing") # ... or all small letters
            #test_query("not example and not nothing")

            #sparse_td_matrix = sparse_matrix.T.tocsr() --> scaling up osaan

            #def rewrite_token(t):
                #return d.get(t, 'sparse_td_matrix[t2i["{:s}"]].todense()'.format(t)) # Make retrieved rows dense


                #hits_matrix = eval(rewrite_query("NOT example OR great"))

                #hits_list = list(hits_matrix.nonzero()[1])

                #for doc_idx in hits_list:
                    #print("Matching doc:", documents[doc_idx])

                #for i, doc_idx in enumerate(hits_list):
                    #print("Matching doc #{:d}: {:s}".format(i, documents[doc_idx]))


    except OSError:
        print("Could not find the file.")


main()
