#!/usr/bin/python

import csv
def csvcat(argv):
    formatter = "{:<6} {:<67} {:<11} {:<11} {:<21} {:<22} {:<18} {:<18}\n{:<19} {:<10}"
    csvfile = argv
    with open(csvfile, 'r') as csvf:
        csvread = csv.reader(csvf)
        rownum = 0
        for row in csvread:
            if rownum == 1 or row[0]=='None':
                print 182 * "-"
            print formatter.format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9])
            rownum = rownum + 1

if __name__ == "__main__":
    csvcat("requests_stats.csv")