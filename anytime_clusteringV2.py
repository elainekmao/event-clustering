import csv, math, numpy, string, sys, collections, time, calendar, re
from gensim import corpora, models, similarities

clusters = collections.defaultdict(list) #identify vectors by ids
vector_dates = collections.defaultdict(int) #(vector id, date) pairs
vector_subjects = collections.defaultdict(str) #(vector id, subject) pairs

index = similarities.SparseMatrixSimilarity.load('sample2/tfidf.index')
corpus = corpora.MmCorpus.load('sample2/tfidf_model.tfidf')
sim = list(enumerate(index))
print "Index loaded."

matrix = []
for row in sim:
    matrix.append(row[1])

value_list = []
for i in range(0,500):
    for j in range(i,500):
        if i!= j:
            value = float(matrix[i][j])
            value_list.append(value)

mean = numpy.average(value_list)
median = numpy.median(value_list)
std = numpy.std(value_list)

print "Mean: " + str(mean)
print "Median: " + str(median)
print "Standard Deviation: " + str(std)

def main():
    with open('sample2/sample.csv', 'rb') as csvfile:
        f = csv.reader(csvfile, delimiter=',')
        i = 0
        for row in f:
            if row[0] != 'id':
                i+=1
                vector_dates[i] = get_date(row[1])
                vector_subjects[i] = get_subject(row[7])
    print "vector_dates, vector_subjects dictionaries populated."
    for vector in vector_dates:
        print "Processing vector " + str(vector)
        if clusters:
            distance_dict = {}
            for cluster in clusters: 
                distance_dict[cluster] = cluster_similarity(vector,cluster)
            most_similar = max(distance_dict.iterkeys(), key=lambda k: distance_dict[k])
            highest_similarity = distance_dict[most_similar]
            if highest_similarity > 0.11282315154: #DEFINE THIS between 0.6 and 0.8
                update_cluster(vector,most_similar)
            else:
                new_cluster(vector)
        else:
            clusters[1] = [vector]
    with open('html/index.html', 'w') as output:
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
                    backgroundColor: "#FFF",
                    spacingTop: 24,
                    zoomType: "x",
                    style: {
                      fontSize: 12,
                      fontFamily: 'sans-serif',
                      fontWeight: 300,
                    }
                  },
                  navigation: {
                    buttonOptions: {
                      theme: {
                        fill: '#333333',
                        stroke: '#000',
                        states: {
                          hover: {
                              fill: '#474747',
                              stroke: '#333',
                          },
                          select: {
                              fill: '#474747',
                              stroke: '#333',
                          }
                        }
                      }
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
                    }
                  },
                  title: {
                    text: $('<div/>').html('WikiLeaks Cables').text(),
                    style: {
                      color: "#333",
                      font: 'sans-serif',
                      fontWeight: 300,
                    }
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
                output.write('{\n')
                output.write('"x": Date.UTC' + str(vector_dates[document]) + ',\n')
                output.write('"y": ' + str(cluster) + ',\n')
                output.write('"id": ' + str(document) + ',\n')
                output.write('"title": $("<div/>").html("' + str(vector_subjects[document]) + '").text(),\n')
                output.write('},\n') 
            output.write('],')
            if i != len(clusters):
                output.write("""
                    marker: {
                        radius: 4,
                        symbol: "circle"
                        }
                },
                    """)
            else:
                output.write("""
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
    print clusters
    return clusters

def get_epoch(time_string):
    return calendar.timegm(time.strptime(time_string, "%m/%d/%Y %H:%M"))

def get_date(time_string):
    t = time.strptime(time_string, "%m/%d/%Y %H:%M")
    return (t[0], t[1], t[2])

def get_subject(text):
    lines = text.split('\n')
    for line in lines:
        matchObj = re.match( r'SUBJECT: (.*) .*|SUBJ: (.*) .*', line, re.M|re.I)
        if matchObj:
            return string.replace(matchObj.group(), '"', '')

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

def select_clusters():
    for cluster in clusters:
        pass
        #if age of cluster less than A, include

def age(cluster):
    vector_list = clusters[cluster]
    last_vector = vector_list[-1]
    last_updated = vector_dates[last_vector]

if __name__ == "__main__": main()
