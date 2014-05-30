import csv, math, string, sys

def process_results(inputfile, outputfile):
    infile = csv.reader(open(inputfile, 'r'))
    outfile = csv.writer(open(outputfile, 'w'))
    i = 0
    total = 0
    for row in infile:
        if i == 4:
            outfile.writerow([total])
            i = 0
            total = 0
        choice = row[47]
        if choice == 'Choice1':
            total += -1
            i += 1
        elif choice == 'Choice2':
            total += 1
            i += 1
        elif choice == 'Choice3':
            total += 0
            i += 1
    outfile.writerow([total])

if __name__ == "__main__": process_results(sys.argv[1], sys.argv[2])