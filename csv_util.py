#!/usr/bin/python
import csv

def parse_csv(filename,row_list):
    f = open(filename, 'rt')
    try:
        reader = csv.reader(f)
        for row in reader:
            row_list+=[row];
    finally:
        f.close()

def write_csv(filename,row_list):
    f = open(filename, 'wt')
    try:
        writer = csv.writer(f)
        writer.writerows(row_list);
    finally:
        f.close()

