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

print("Term-document matrix: (?)\n")
print(sparse_matrix)

dense_matrix = sparse_matrix.todense()

print("Term-document matrix: (?)\n")
print(dense_matrix)

td_matrix = dense_matrix.T   # .T transposes the matrix

print("Term-document matrix:\n")
print(td_matrix)

print("\nIDX -> terms mapping:\n")
print(cv.get_feature_names())

terms = cv.get_feature_names()

print("First term (with row index 0):", terms[0])
print("Third term (with row index 2):", terms[2])

print("\nterm -> IDX mapping:\n")
print(cv.vocabulary_) # note the _ at the end

print("Row index of 'example':", cv.vocabulary_["example"])
print("Row index of 'silly':", cv.vocabulary_["silly"])
<<<<<<< HEAD
=======

>>>>>>> df81a73d0091341a6b7530ee4186573a8bde65cf
