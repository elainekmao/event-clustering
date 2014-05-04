import csv, math, numpy, string, sys, collections, time, calendar, re
from gensim import corpora, models, similarities

csv.field_size_limit(1000000000)

clusters = collections.defaultdict(list) #identify vectors by ids
vector_dates = collections.defaultdict(list) #(vector id, date) pairs
vector_subjects = collections.defaultdict(str) #(vector id, subject) pairs
vector_snippets = collections.defaultdict(str) #(vector id, snippet) pairs

index = similarities.SparseMatrixSimilarity.load('sample3/tfidf.index')
corpus = corpora.MmCorpus.load('sample3/tfidf_model.tfidf')
sim = list(enumerate(index))
print "Index loaded."

#matrix = []
#for row in sim:
#    matrix.append(row[1])

#value_list = []
#for i in range(0,500):
#    for j in range(i,500):
#        if i!= j:
#            value = float(matrix[i][j])
#            value_list.append(value)

#mean = numpy.average(value_list)
#median = numpy.median(value_list)
#std = numpy.std(value_list)

#print "Mean: " + str(mean)
#print "Median: " + str(median)
#print "Standard Deviation: " + str(std)

def main():
    with open('sample3/sample.csv', 'rb') as csvfile:
        f = csv.reader(csvfile, delimiter=',')
        i = 0
        for row in f:
            if row[0] != 'id':
                i+=1
                vector_dates[i] = get_date(row[1])
                vector_subjects[i] = get_subject(row[7])
                vector_snippets[i] = get_preview(row[7])
    print "vector_dates, vector_subjects dictionaries populated."
    outputcsv = csv.writer(open('vector_clusters_high_threshold.csv', 'w'))
    for vector in vector_dates:
        print "Processing vector " + str(vector)
        if clusters:
            distance_dict = {}
            for cluster in clusters: 
                distance_dict[cluster] = cluster_similarity(vector,cluster)
            most_similar = max(distance_dict.iterkeys(), key=lambda k: distance_dict[k])
            highest_similarity = distance_dict[most_similar]
            if highest_similarity > 0.1: #mean + std
                update_cluster(vector,most_similar)
                outputcsv.writerow([vector, most_similar, vector_snippets[vector], 'https://rawgit.com/elainekmao/event-clustering/master/html/' + str(vector) + '.html'])
            else:
                new_cluster(vector)
                cluster_id = clusters.keys()[-1] + 1
                outputcsv.writerow([vector, cluster_id, vector_snippets[vector], 'https://rawgit.com/elainekmao/event-clustering/master/html/' + str(vector) + '.html'])
        else:
            clusters[1] = [vector]
            outputcsv.writerow([vector, 1, vector_snippets[vector], 'https://rawgit.com/elainekmao/event-clustering/master/html/' + str(vector) + '.html'])
            print "Cluster 1 created."
    with open('html/index_high_threshold.html', 'w') as output:
        output.write("""
<!DOCTYPE html>
<html>
    <head>
      <title>WikiLeaks Event Detection</title>
        <script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
        <script src="js/highcharts.js"></script>
        <link rel="stylesheet" href="css/bootstrap.min.css">

        <body>
        <div id="graph"></div>
        <script>
            var chart = null;
            var autoTickInterval = null;
            $(function () {
              $('#graph').highcharts({
                  chart: {
                    height: 700,
                    backgroundColor: "#FFF",
                    spacingTop: 24,
                    zoomType: "xy",
                    style: {
                      fontSize: 12,
                      fontFamily: 'sans-serif',
                      fontWeight: 300,
                    }
                  },
                  yAxis: {
                    min: 0,
                    max: """ + str(len(clusters)) + """,
                    title: {
                      text: "Clusters",
                      style: {
                        color: "#AAA",
                        fontWeight: 300,
                      }
                    },
                    labels: {
                      style: {
                        color: "#999",
                      }
                    },
                    gridLineColor: 'rgba(255, 255, 255, .1)'
                  },
                  xAxis: {
                    type: "datetime",
                    title: {
                      text: "Time",
                      style: {
                        color: "#AAA",
                        fontWeight: 300,
                      }
                    },
                    labels: {
                      style: {
                        color: "#999",
                      }
                    },
                    max: 10
                  },
                  title: {
                    text: $('<div/>').html('WikiLeaks Cables').text(),
                    style: {
                      color: "#333",
                      font: 'sans-serif',
                      fontWeight: 300,
                    }
                  },
                  scrollbar: {
                    enabled: true
                  },
                  legend: {
                    enabled: false
                  },
                  credits: {
                    href: "http://www.elainekmao.com",
                    text: "http://www.elainekmao.com"
                  },
                  tooltip: {
                    useHTML: true,
                    formatter: function() {
                        return [
                                "<b>", this.point.id, "</b>", "<br>",
                                this.point.title, "<br>", 
                                "Cluster: ", this.point.y, "<br>", 
                                "Date: ", Highcharts.dateFormat("%B %e %Y", this.point.x)
                               ].join("");
                    }
                  },
                  plotOptions: {
                  turboThreshold: 10000,
                    scatter: {
                      cursor: 'pointer',
                      point: {
                        events: {
                          click: function() {
                            window.open(
                              [this.options.id, ".html"].join(""),
                            '_blank');
                          }
                        }
                      }
                    }
                  },
                  series: [
        """)
        i = 1
        for cluster in clusters:
            output.write("""
                {
                    type: "scatter",
                    data: [
                """)
            for document in clusters[cluster]:
                output.write('\t\t\t{\n')
                output.write('\t\t\t"x": Date.UTC' + str(vector_dates[document]) + ',\n')
                output.write('\t\t\t"y": ' + str(cluster) + ',\n')
                output.write('\t\t\t"id": ' + str(document) + ',\n')
                output.write('\t\t\t"title": $("<div/>").html("' + str(vector_subjects[document]) + '").text(),\n')
                output.write('\t\t\t},\n') 
            output.write('\t\t],')
            if i != len(clusters):
                output.write("""
                    lineWidth: 1,
                    marker: {
                        radius: 4,
                        symbol: "circle"
                        }
                },
                    """)
            else:
                output.write("""
                    lineWidth: 1,
                    marker: {
                        radius: 4,
                        symbol: "circle"
                },
                    """)
            i += 1
        output.write("""},
            ]
            }
            );
            });
            </script>""")
    return clusters

def get_date(time_string):
    t = time.strptime(time_string, "%m/%d/%Y %H:%M")
    return (t[0], t[1], t[2])

def get_subject(text):
    lines = text.split('\n')
    for line in lines:
        matchObj = re.match( r'SUBJECT: (.*) .*|SUBJ: (.*) .*', line, re.M|re.I)
        if matchObj:
            return string.replace(matchObj.group(), '"', '')

def get_preview(text):
    lines = text.split('\n')
    i = 0
    for line in lines:
        i += 1
        matchObj = re.match( r'SUBJECT: (.*) .*|SUBJ: (.*) .*', line, re.M|re.I)
        if matchObj:
            snippet = ''
            snippet += '<p>' + string.replace(matchObj.group(), '"', '') + '</p>'
            for line in lines[i:i+5]:
                matchObj = re.match( r'REF: (.*) .*|1\. (.*) .*|REFS: (.*) .*', line, re.M|re.I)
                if matchObj:
                    break
                elif line.strip():
                    snippet += '<p>' + line + '</p>'
            return snippet

def vector_similarity(i,j): #by IDs
    return sim[i-1][1][j-1]

def cluster_similarity(i,cluster_id):
    cluster = clusters[cluster_id]
    total = 0
    for j in cluster:
        total += vector_similarity(i,j)
    return total/len(cluster)

def update_cluster(vector,cluster_id):
    clusters[cluster_id] += [vector]
    print "Cluster " + str(cluster_id) + " updated with new vector."

def new_cluster(vector):
    last_cluster = clusters.keys()[-1]
    clusters[last_cluster + 1] += [vector]
    print "Cluster " + str(last_cluster +1) + " created."

if __name__ == "__main__": main()

