import csv, math, string, random

csv.field_size_limit(1000000000)

comparison = csv.writer(open('a_vs_b.csv', 'w'))
comparison.writerow(['Cluster A Number', 'Cluster A Entries', 'Cluster B Number', 'Cluster B Entries'])

for i in range(100):
    set_a = csv.reader(open('vector_clusters_time.csv', 'rb'))
    set_b = csv.reader(open('vector_clusters_no_expiration.csv', 'rb'))
    document = random.randint(1, 10000)
    set_a_entry = []
    set_b_entry = []
    cluster_number_a = ''
    cluster_number_b = ''
    for line in set_a:
        if int(line[0]) == document:
            cluster_number_a = int(line[1])
    for line in set_b:
        if int(line[0]) == document:
            cluster_number_b = int(line[1])
    set_a = csv.reader(open('vector_clusters_time.csv', 'rb'))
    set_b = csv.reader(open('vector_clusters_no_expiration.csv', 'rb'))
    for line in set_a:
        if int(line[1]) == cluster_number_a:
            entry = line[2]
            entry += '<a href=' + str(line[3]) + '>View full text</a>'
            set_a_entry.append(entry)
    for line in set_b:
        if int(line[1]) == cluster_number_b:
            set_b_entry.append(line[2:])
    comparison.writerow([cluster_number_a, set_a_entry, cluster_number_b, set_b_entry])
    i += 1
