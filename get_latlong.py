#!/usr/bin/python

import logging

from csv_util import *
from optparse import OptionParser
import json
import urllib2
import urllib
import sys
import time

def init_log(logfile):
    logging.basicConfig(filename=logfile, filemode='a',
        format='%(asctime)-15s %(levelname)s %(message)s',level=logging.DEBUG)


def get_lat_lng_from_url(url):
    try:
        response = urllib2.urlopen(url)
    except Exception as e:
        logging.exception(e)
        logging.info("Malformed URL ::" + url)
        sys.exit(1)

    if response.code!=200:
        logging.info("Http Error Code " +response.code+" For URL ::" + url)
        sys.exit(1)

    decoder = json.JSONDecoder();
#    json_response = json.dumps(response.read())
    try:
        decoded_json = decoder.decode(response.read())
    except Exception as e:
        logging.exception(e)
        logging.info("Malformed JSON ::"+json_response + "for the url ::" + url)
        sys.exit(1)
    
    try:
        #lat_lng = decoded_json['results'][0]['geometry']['location'];
        lat_lng = decoded_json['results'][0]['geometry']['location']

    except Exception as e:
        logging.exception(e)
        logging.info("Lat Long not found in JSON ::"+str(decoded_json) + "for the url ::" + url)
        sys.exit(1)
        
    return  lat_lng;


def get_lat_long_info():
    num_of_movies = len(movie_list);
    movie_list[0].append("latitude")
    movie_list[0].append("longitude")
    API_KEY = "&key=AIzaSyC929XwB6__sRxCPKRY6jscx6IOuLRX02M"
    API_URL = "https://maps.googleapis.com/maps/api/geocode/json?"
    EXTRA_LOC = " San Fransciso, CA, USA"
    for i in range(1,num_of_movies):
        location = {"address" : movie_list[i][2] + EXTRA_LOC};
        lat_lng = get_lat_lng_from_url(API_URL+urllib.urlencode(location)+API_KEY)
        movie_list[i].append(lat_lng['lat'])
        movie_list[i].append(lat_lng['lng'])
        time.sleep(0.25)
        



def main():
    parser = OptionParser()
    parser.add_option("-f", "--csv_filename", action="store", default="",
                help="CSV File Name")
    parser.add_option("-o", "--output_csv_filename", action="store", default="",
                help="Output CSV File Name")
    parser.add_option("-l", "--logfile", action="store", default="server.log",
                help="File Name to save the log")

    (options, args) = parser.parse_args()
    init_log(options.logfile)
    if len(options.csv_filename) == 0 :
        logging.error("input data file not specified");
        sys.exit(1);
    
    if len(options.output_csv_filename) == 0 :
        logging.error("output data file not specified");
        sys.exit(1);

    global movie_list
    movie_list=[]
    parse_csv(options.csv_filename,movie_list)
    global temp_movie_list
    temp_movie_list=movie_list[:10]
    get_lat_long_info()
    write_csv(options.output_csv_filename,movie_list)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.exception(e)
        sys.exit(1)


