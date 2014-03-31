import csv, math, numpy, string, sys, collections, time, calendar
from gensim import corpora, models, similarities

clusters = collections.defaultdict(list) #identify vectors by ids?
cluster_means = collections.defaultdict(list)
vectors = collections.defaultdict(list) #{vector_id:vector} pairs
vector_dates = collections.defaultdict(int)

index = similarities.SparseMatrixSimilarity.load('sample/sample_tfidf.index')
corpus = corpora.MmCorpus.load('sample/sample_tfidf_model.tfidf')

def main():
    with open('sample/sample.csv', 'rb') as csvfile:
        f = csv.reader(csvfile, delimiter=',')
        i = 0
        for row in f:
            if row[0] != 'id':
                i+=1
                vector_dates[i] = get_epoch(row[1])
    with open('sample/sample_tfidf.csv', 'rb') as csvfile:
        vectorfile = csv.reader(csvfile, delimiter=',')
        i = 0
        for vector in vectorfile:
            i += 1
            vectors[i] = vector
    for vector in vectors:
        if clusters:
            distance_dict = {}
            for cluster in clusters: 
                distance_dict[cluster] = cosine_distance(vectors[vector],cluster)
            closest_cluster = min(distance_dict.iterkeys(), key=lambda k: distance_dict[k])
            closest_distance = distance_dict[closest_cluster]
            if closest_distance < 0.8: #DEFINE THIS between 0.6 and 0.8
                update_cluster(vector,closest_cluster)
            else:
                new_cluster(vector)
        else:
            clusters[1] = [vector]
            cluster_means[1] = vectors[vector]
    print clusters, cluster_means
    return clusters

def get_epoch(time_string):
    return calendar.timegm(time.strptime(time_string, "%m/%d/%Y %H:%M"))

def vector_distance(i,j): #by IDs
    sim = list(enumerate(index))
    return sim[i][1][j]

#def cosine_distance(vector,cluster_id):
#    cluster_mean = cluster_means[cluster_id]
#    for element in vector:
#        pass
#    return numpy.dot(vector,cluster_mean)/math.sqrt((numpy.dot(vector,vector)*numpy.dot(cluster_mean,cluster_mean)))

def update_cluster(vector,cluster_id):
    cluster_size = len(clusters[cluster_id])
    mean = cluster_means[cluster_id]
    updated_mean = (mean*cluster_size + vector)/(cluster_size + 1)
    cluster_means[cluster_id] = updated_mean
    clusters[cluster_id] += vector
    print "Cluster " + cluster_id + " updated with new vector."

def new_cluster(vector):
    last_cluster = clusters.keys()[-1]
    clusters[last_cluster + 1] += vector
    cluster_means[last_cluster + 1] = vectors[vector]

def select_clusters():
    for cluster in clusters:
        pass
        #if age of cluster less than A, include

def age(cluster):
    vector_list = clusters[cluster]
    last_vector = vector_list[-1]
    last_updated = vector_dates[last_vector]

if __name__ == "__main__": main()

