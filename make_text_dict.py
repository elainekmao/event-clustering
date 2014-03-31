import csv, math, string, sys
from gensim import corpora, models, similarities
from nltk.corpus import stopwords

#Increases field size limit
csv.field_size_limit(1000000000)

def main(document):
    with open(document, 'rb') as csvfile:
        docreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        texts = []
        for row in docreader:
            if row[0] != 'id':
                document = []
                clean_row = tokenize_text(row[7])
                for word in clean_row:
                    document.append(word)
                texts.append(document)
        print "Done compiling texts."

    dictionary = corpora.Dictionary(texts)
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
    dictionary.filter_tokens(once_ids)
    dictionary.compactify()
    dictionary.save('cables.dict')
    print dictionary

    dict_list = []
    keys = dictionary.token2id.keys()
    values = dictionary.token2id.values()
    for item in range(0, len(dictionary)):
        dict_list.append([values[item], keys[item]])
    docwriter = csv.writer(open("cablesdictionary.csv", "wb"))
    docwriter.writerows(dict_list)
    print "CSV written."

    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('cables_corpus.mm', corpus)

def tokenize_text (text):
    lowercase_text = text.lower()
    unhyphenated = string.replace(lowercase_text, "-", " ")
    unpunctuated_text = string.translate(unhyphenated, None, string.punctuation)
    split_text = unpunctuated_text.split()
    important_text = filter(lambda x: x not in stopwords.words('english'), split_text)
    return important_text

    #all_tokens = sum(texts, [])
    #tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    #texts = [[word for word in text if word not in tokens_once] for text in texts]
    #dictionary = corpora.Dictionary(texts)
    #dictionary.save('/tmp/cables.dict')
    #print dictionary

if __name__ == "__main__": main(sys.argv[1])