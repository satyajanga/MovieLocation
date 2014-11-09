#!/usr/bin/python
from process_movie_data import ProcessMovies
import logging
from optparse import OptionParser
from bottle import route, run, request, static_file,debug
import bottle

@route('/movies')
def movies():
    movie_name = request.GET.get('movie',default = None).lower()
    return movies_db.search_with_prefix(movie_name);

@route('/get_locations')
def get_locations(): 
    movie_name = request.GET.get('movie',default = None).lower()
    return movies_db.get_locations_by_name(movie_name);

@route('/index.html')
@route('/')
def site(): 
    return static_file("index.html", root = ".")

@route('/map.js')
def site(): 
    return static_file("map.js", root =".")

def init_log(logfile):
    logging.basicConfig(filename=logfile, filemode='a',
                format='%(asctime)-15s %(levelname)s %(message)s',
                level=logging.DEBUG)


parser = OptionParser()
parser.add_option("-f", "--csv_filename", action="store", default="",
                    help="CSV File Name")
parser.add_option("-l", "--logfile", action="store", default="server.log",
                help="File Name to save the log")

#(options, args) = parser.parse_args()
log_file = "server.log"
csv_file = "output.csv"
init_log(log_file)
if len(csv_file) == 0 :
    logging.error("input data file not specified");
    sys.exit(1);


movies_db = ProcessMovies(csv_file,log_file)
debug(True) # display traceback 
application = bottle.default_app()

    
