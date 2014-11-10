#!/usr/bin/python
import csv
import logging

"""
Parse the csv file and return all the rows in a list
"""
def parse_csv(filename,row_list):
    f = open(filename, 'rt')
    try:
        reader = csv.reader(f)
        for row in reader:
            row_list+=[row];
    except:
       logging.info("Failed To parse CSV File:" + filename)
    finally:
        f.close()

def write_csv(filename,row_list):
    f = open(filename, 'wt')
    try:
        writer = csv.writer(f)
        writer.writerows(row_list);
    except:
       logging.info("Failed To write into CSV File:" + filename)
    finally:
        f.close()

