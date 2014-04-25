import csv, math, string, sys
from gensim import corpora, models, similarities

corpus = corpora.MmCorpus('sample3/cables_corpus.mm')
dictionary = corpora.Dictionary.load('sample3/cables.dict')
print "Corpus loaded."

tfidf = models.TfidfModel(corpus, normalize=True)
tfidf_corpus = tfidf[corpus]
tfidf_index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=58672)

tfidf.save('sample3/tfidf_model.tfidf')
tfidf_index.save('sample3/tfidf.index')
print "TF-IDF model saved."

#for document in tfidf_corpus:
#    total_writer = csv.writer(open('tfidf.csv', 'a'))
#    total_writer.writerow(document)
#print "TF-IDF done."

#lsi = models.LsiModel(tfidf_corpus, id2word=dictionary, num_topics=300)
#lsi_corpus = lsi[tfidf_corpus]
#lsi_index = similarities.Similarity(lsi_corpus)

#lsi.save('lsi_model.lsi')
#lsi_index.save('lsi.index')

#for document in lsi_corpus:
#    total_writer = csv.writer(open('lsi.csv', 'a'))
#    total_writer.writerow(document)
#print "LSI done."