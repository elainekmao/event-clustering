import csv, math, string, sys

#Increases field size limit
csv.field_size_limit(1000000000)

def main(document):
    with open(document, 'rb') as csvfile:
        docreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        i = 1
        for row in docreader:
            if row[0] != 'id':
                f = open('html/%s.html' % i, 'wb')
                row_id = row[0]
                created_date = row[1]
                reference_id = row[2]
                origin = row[3]
                classification = row[4]
                references = row[5]
                header = row[6]
                text = row[7].split('\n')
                html_string = """
<!DOCTYPE html>
<html>
<head>
    <title>WikiLeaks Cables - """ + row_id + """</title>
    <link rel="stylesheet" href="css/bootstrap.min.css">
</head>
<body>
    <div class="container">
    """
                f.write(html_string)
                f.write("<p>" + row_id + ", " + created_date + ", " + reference_id + ", " + 
                    origin + ", " + classification + ", " + references + ", " + header + "</p>\n")
                for line in text:
                    f.write("<p>" + line + "</p>")
                f.write("</div>\n")
                f.write("</body>\n")
                f.write("</html>")
                f.close()
                i += 1

if __name__ == "__main__": main(sys.argv[1])