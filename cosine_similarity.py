import csv, math, string, sys
from gensim import corpora, models, similarities

index = similarities.SparseMatrixSimilarity.load('tfidf.index')

similarity_matrix = csv.writer(open("tfidf_matrix.csv", 'a'))

for similarities in index:
    similarity_matrix.writerow(list(enumerate(similarities)))