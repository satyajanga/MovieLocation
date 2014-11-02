#!/usr/bin/python

from csv_util import parse_csv
import sys
import logging
import urlparse
from optparse import OptionParser

from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import json


html_str ="""<!DOCTYPE html> \n<html>\n <body>\n\n\n<form action="abc" method="GET">
    Movie Name: <input type=\"text\" name=\"movie\"><br>
    <input type="submit" value="Submit">
        </form>
            
                <p><b>Note:</b> The form itself is not visible. Also note that the default width of a text field is 20 characters.</p>
                    
                        </body>
                            </html>
                                """

html_gmaps = """<!DOCTYPE html>
<html>
  <head>
      <style>
            #map_canvas {
                width: 1280px;
                height: 960px;
            }
      </style>
      <script src="https://maps.googleapis.com/maps/api/js"></script>
      <script>
          function initialize() {
              var mapCanvas = document.getElementById('map_canvas');
              var mapOptions = {
                  center: new google.maps.LatLng(44.5403, -78.5463),
                  zoom: 8,
                  mapTypeId: google.maps.MapTypeId.ROADMAP
              }
              var map = new google.maps.Map(mapCanvas, mapOptions)
        }
        google.maps.event.addDomListener(window, 'load', initialize);
      </script>
   </head>
                                                                                                                                                  <body>
                                                                                                                                                      <div id="map_canvas"></div>
                                                                                                                                                        </body>
                                                                                                                                                        </html> """

class MyRequestHandler (BaseHTTPRequestHandler) :

    def do_GET(self) :
        parsed_path = urlparse.urlparse(self.path)
        query_path = parsed_path.path;
        query_params = urlparse.parse_qs(parsed_path.query)
        if query_path == "/movies" :
            self.send_response(200)
            self.send_header("Content-type:", "text/html")
            self.wfile.write("\n")
            self.wfile.write(html_gmaps)
#    def do_POST(self):
        if query_path == "/abc":
            self.send_response(200)
            self.send_header("Content-type:", "text/html")
            self.wfile.write("\n")
            self.wfile.write(movies_index[query_params["movie"][0]])


def init_log(logfile):
    logging.basicConfig(filename=logfile, filemode='a',
                format='%(asctime)-15s %(levelname)s %(message)s',
                level=logging.DEBUG)


def create_dict_for_auto_completion():
    global movies_index;
    movies_index={}
    num_of_movies = len(movies_list);
    count =0; 
#    num_of_movies = 3;
    for i in range(1,num_of_movies):
        movie_len = len(movies_list[i][0])
        count += movie_len-1
 #       print movies_list[i][0]
        for j in range(1,movie_len+1):
            if movies_list[i][0][:j] in movies_index:
                movies_index[movies_list[i][0][:j]].append(i)
            else:
                movies_index[movies_list[i][0][:j]] = [i]
 #       print movies_index;
     
    logging.info("N- gram index with size =" +str(len(movies_index)) );
    print count

def parse_csv(filename):
    global movies_list
    movies_list=[]
    f = open(filename, 'rt')
    try:
        reader = csv.reader(f)
        for row in reader:
            movies_list+=[row];
    finally:
        f.close()
   
    logging.info(" CSV File" + filename + " parsed successfully with num of movies  :: " + str(len(movies_list)));
    

def main():
    parser = OptionParser()
    parser.add_option("-f", "--csv_filename", action="store", default="",
                    help="CSV File Name")
    parser.add_option("-l", "--logfile", action="store", default="server.log",
                help="File Name to save the log")
    
    (options, args) = parser.parse_args()
    init_log(options.logfile)
    if len(options.csv_filename) == 0 :
        logging.error("input data file not specified");
        sys.exit(1);

    parse_csv(options.csv_filename)
    create_dict_for_auto_completion()
    server = HTTPServer(("localhost", 8003), MyRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.exception(e)
        sys.exit(1)
    
