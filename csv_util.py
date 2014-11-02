#!/usr/bin/python
import csv

@staticmethod
def parse_csv(filename,row_list):
    f = open(filename, 'rt')
    try:
        reader = csv.reader(f)
        for row in reader:
            movies_list+=[row];
    finally:
        f.close()

