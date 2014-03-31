import csv, math, string, sys
from gensim import corpora, models, similarities
from nltk.corpus import stopwords

#Increases field size limit
csv.field_size_limit(1000000000)

def main (document):
    with open(document, 'rb') as csvfile:
        docreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        with open('temp.csv', 'wb') as f:
            tempwriter = csv.writer(f, delimiter=',')
            for row in docreader:
                row[7] = tokenize_text(row[7])
                tempwriter.writerow(row)
            print "Done"

def tokenize_text (text):
    lowercase_text = text.lower()
    unhyphenated = string.replace(lowercase_text, "-", " ")
    unpunctuated_text = string.translate(unhyphenated, None, string.punctuation)
    split_text = unpunctuated_text.split()
    important_text = filter(lambda x: x not in stopwords.words('english'), split_text)
    return important_text

if __name__ == "__main__": main(sys.argv[1])