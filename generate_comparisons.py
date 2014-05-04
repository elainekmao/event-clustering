import csv, math, string, random, collections

csv.field_size_limit(1000000000)

comparison = csv.writer(open('lowthreshold_vs_highthreshold.csv', 'w'))
comparison.writerow(['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10'])

for i in range(100):
    set_a = csv.reader(open('vector_clusters_no_expiration.csv', 'rb'))
    set_b = csv.reader(open('vector_clusters_high_threshold.csv', 'rb'))
    document = random.randint(1, 10000)
    cluster_number_a = ''
    cluster_number_b = ''
    for line in set_a:
        if int(line[0]) == document:
            cluster_number_a = int(line[1])
    for line in set_b:
        if int(line[0]) == document:
            cluster_number_b = int(line[1])
    set_a = csv.reader(open('vector_clusters_no_expiration.csv', 'rb'))
    set_b = csv.reader(open('vector_clusters_high_threshold.csv', 'rb'))
    set_a_entries = collections.defaultdict(str)
    set_b_entries = collections.defaultdict(str)
    for line in set_a:
        if int(line[1]) == cluster_number_a:
            entry = line[2]
            entry += '<a href=' + str(line[3]) + '>View full text</a>'
            set_a_entries[line[0]] = entry
    for line in set_b:
        if int(line[1]) == cluster_number_b:
            entry = line[2]
            entry += '<a href=' + str(line[3]) + '>View full text</a>'
            set_b_entries[line[0]] = entry
    ten_entries_a = collections.defaultdict(str)
    ten_entries_b = collections.defaultdict(str)
    a = []
    b = []
    if len(set_a_entries) > 10:
        sample = random.sample(set_a_entries.keys(), 10)
        for num in sample:
            ten_entries_a[num] = set_a_entries[num]
        for key in sorted(ten_entries_a):
            a.append(ten_entries_a[key])
    else:
        for entry in set_a_entries:
            a.append(set_a_entries[entry])
        for i in range(10 - len(set_a_entries)):
            a.append('')
            i += 1
    if len(set_b_entries) > 10:
        sample = random.sample(set_b_entries.keys(), 10)
        for num in sample:
            ten_entries_b[num] = set_b_entries[num]
        for key in sorted(ten_entries_b):
            b.append(ten_entries_b[key])
    else:
        for entry in set_b_entries:
            b.append(set_b_entries[entry])
        for i in range(10 - len(set_b_entries)):
            b.append('')
            i += 1
    comparison.writerow([a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7], b[8], b[9]])
    i += 1
