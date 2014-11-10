#!/usr/bin/python
from movie_db import MovieDB
import logging
from bottle import route, run, request, static_file,debug
import bottle

"""
Route to handle auto complete search
Example Query: /movies?movie=ae
"""
@route('/movies')
def movies():
    movie_name = request.GET.get('movie',default = None).lower()
    return movies_db.search_with_prefix(movie_name);

"""
Route to return (lat,long) coordinates and other movie information
Example Query: /get_locations=alcatraz
"""
@route('/get_locations')
def get_locations(): 
    movie_name = request.GET.get('movie',default = None).lower()
    return movies_db.get_locations_by_name(movie_name);

"""
To return static content
"""
@route('/index.html')
@route('/')
def site(): 
    return static_file("index.html", root = ".")


"""
To return static content
"""
@route('/map.js')
def site(): 
    return static_file("map.js", root =".")

"""
This function initializes the logger

"""
def init_log(logfile):
    logging.basicConfig(filename=logfile, filemode='a',
                format='%(asctime)-15s %(levelname)s %(message)s',
                level=logging.DEBUG)

log_file = "server.log"
csv_file = "output.csv"
init_log(log_file)
if len(csv_file) == 0 :
    logging.error("input data file not specified");
    sys.exit(1);


movies_db = MovieDB(csv_file)
debug(True) # display traceback 
application = bottle.default_app()

    
