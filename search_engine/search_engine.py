from sklearn.feature_extraction.text
import CountVectorizer

def main():

    try:
         
    file = open("enwiki-20181001-corpus.1000-articles.txt", "r")
    
    file = file.read()

    cv = CountVectorizer(lowercase=True, binary=True)
    sparse_matrix = cv.fit_transform(documents)
    
    file_variable.close()

    except OSError:
        print("Could not find the file.")
