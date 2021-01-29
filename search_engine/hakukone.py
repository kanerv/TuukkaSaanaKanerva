from sklearn.feature_extraction.text import CountVectorizer
import re, fileinput

#########################################
#This program is a search engine        #
#created for Building NLP Apllications  #
#week 2 assignment.                     #
#########################################

def main():
    
    

    try:
        teksti = []
        documents = []

        pattern = r'(?u)\b\w+\b' #a new regex that takes into account tokens comprised of a singe alphanumerical character
        print("This is TuukkaSaanaKanerva's search engine.")
        path = input("Please input file path: ")
        file = open(path, "r") #Opens the file

        for line in file:           #because the file is massive,
                                    #this is better than read(),
                                    #as it doesn't store the whole
                                    #thing into memory
            if len(teksti) < 1000:
                teksti.append(line)

        #file_variable = file.read() #Reads the contents(dead code)

        text_string = "".join(teksti)
        documents = text_string.split("</article>") #splits the file into a list at </article>
        file.close()

        
        cv = CountVectorizer(lowercase=True, binary=True, token_pattern=pattern)
        global dense_matrix, sparse_td_matrix,td_matrix, t2i
        sparse_matrix = cv.fit_transform(documents)
        dense_matrix = sparse_matrix.todense()
        sparse_td_matrix = sparse_matrix.T.tocsr()
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
            return d.get(t, 'sparse_td_matrix[t2i["{:s}"]].todense()'.format(t)) # Make retrieved rows dense


        def rewrite_query(query): # rewrite every token in the query
            return " ".join(rewrite_token(t) for t in query.split())

        def test_query(query):
            print("Query: '" + query + "'")
            print("Rewritten:", rewrite_query(query))

            try:
                hits_matrix = eval(rewrite_query(query))
                hits_list = list(hits_matrix.nonzero()[1])
                for i, doc_idx in enumerate(hits_list[0:9]):
                    print("Matching doc #{:d}: {:s}".format(i, documents[doc_idx]))
                    print()

            except KeyError:
                print("Search term not found. No Matching doc.")         

        query = "?"
        while query != "":
            print("You can use AND, OR, NOT, as parametres.\nHyphenated words are regarded as separate words.\n***\nIf you want to quit press enter.\n")
            query = input("Enter a search term: ")
            if query != "":
                test_query(query)
            else:
                print("You did not enter a query, bye!")

    except OSError:
        print("Could not find the file.")


main()
