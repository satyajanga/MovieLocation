#!/usr/bin/python

from csv_util import parse_csv
import sys
import logging
import urlparse
from optparse import OptionParser

from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import json
# <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAzj8PHYdRbMgP1datcx7Z_suSS_s1DYqY"></script>

html_gmaps = """<!DOCTYPE html>
<html>
  <head>
      <style type="text/css">
      html {height : 100%}
      body {height : 100%; margin : 0; padding: 0}
      #map_canvas {
                width : 100%;
                height: 100%;
            }
      </style>
        <link href="//ajax.googleapis.com/ajax/libs/jqueryui/1.11.1/themes/ui-darkness/jquery-ui.min.css" rel="stylesheet">
            <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
                <script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.11.1/jquery-ui.min.js"></script>
     <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?sensor=false"></script>
     <script>
        var map;
        var markers = [];
        function addMarker(location, content) {
              var marker = new google.maps.Marker({
                      position: location,
                      map: map, 
                      title : content
                });
              markers.push(marker);
        }

        function deleteMarkers() {
              for (var i = 0; i < markers.length; i++) {
                   markers[i].setMap(null);
              }
              markers = [];
        }
        
        function initialize(){
              var mapCanvas = document.getElementById('map_canvas');
              var mapOptions = {
                  center: new google.maps.LatLng(37.7833, -122.4167),
                  zoom: 10,
                  mapTypeId: google.maps.MapTypeId.ROADMAP
              }
     map = new google.maps.Map(mapCanvas, mapOptions);
     map.controls[google.maps.ControlPosition.TOP_LEFT].push($("#movies").get(0));
    }

$(function() {

            $("#movies").autocomplete({
                        source : function(request, response){
                            var data = getMovies();
                            response(data);
                            },
                        select : function(event,ui){
                            httpGet(ui.item.label);
                        }
                            });
});

      function getMovies()
      {
          var xmlHttp = null;
          xmlHttp = new XMLHttpRequest();
          xmlHttp.open( "GET", "/movies?movie="+$("#movies").val(), false );
          xmlHttp.send( null );
          var jsonData = JSON.parse(xmlHttp.responseText);
          return jsonData.movies;
      }

      function httpGet(movie_name)
      {
          deleteMarkers();
          var xmlHttp = null;
          xmlHttp = new XMLHttpRequest();
          xmlHttp.open( "GET", "/get_locations?movie="+movie_name , false );
          xmlHttp.send( null );
          var jsonData = JSON.parse(xmlHttp.responseText);
          var avg_lat=0
          var avg_lng=0;
          for (var i = 0; i < jsonData.location.length; i++) {
            var location = new google.maps.LatLng(jsonData.location[i].lat,jsonData.location[i].lng);
            var infoWindow = new google.maps.InfoWindow({
                      content: jsonData.location[i].content
                        });

            avg_lat += jsonData.location[i].lat;
            avg_lng += jsonData.location[i].lng;
            addMarker(location,jsonData.location[i].content);
          }

          if(jsonData.location.length !=0)
          {
            avg_lat = avg_lat/jsonData.location.length;
            avg_lng = avg_lng/jsonData.location.length;
          }

      }
      google.maps.event.addDomListener(window, 'load', initialize);
      </script>

   </head>
                                                                                                                                                  <body>
            <div id="map_canvas"></div>
           
    <div class="ui-widget">
      Moives: <input id="movies">
        </div>                                                                                                                                                    </html> """

class MyRequestHandler (BaseHTTPRequestHandler) :
    def do_GET(self) :
        parsed_path = urlparse.urlparse(self.path)
        query_path = parsed_path.path;
        query_params = urlparse.parse_qs(parsed_path.query)
        if query_path == "/":
            self.send_response(200)
            self.send_header("Content-type:", "text/html")
            self.wfile.write("\n")
            self.wfile.write(html_gmaps)

        if query_path == "/movies" :
            self.send_response(200)
            self.send_header("Content-type:", "text/html")
            self.wfile.write("\n")
            try:
                movie_name_idx = movies_index[query_params["movie"][0].lower()]
            except:
               movie_name_idx=[]
            movies=[]
            for i in movie_name_idx:
                movies.append(movies_list[i][0])
            
            movies_names={'movies' : list(set(movies))};
            self.wfile.write(json.dumps(movies_names))
        
        if query_path == "/get_locations":
            self.send_response(200)
            self.send_header("Content-type:", "text/html")
            self.wfile.write("\n")

            try:
                movie_locations = movies_index[query_params["movie"][0].lower()]
            except:
                movie_locations =[]

            cols = len(movies_list[0])
            locations={'location' : []};
            for i in movie_locations:
                location = {}
                location['lat'] = movies_list[i][cols-2];
                location['lng'] = movies_list[i][cols-1];
                location['content'] = "Movie Name : " + movies_list[i][0]+"\nLocation :: "+ movies_list[i][2]   
                locations['location'].append(location)
                
            self.wfile.write(json.dumps(locations))


def init_log(logfile):
    logging.basicConfig(filename=logfile, filemode='a',
                format='%(asctime)-15s %(levelname)s %(message)s',
                level=logging.DEBUG)


def create_dict_for_auto_completion():
    global movies_index;
    movies_index={}
    num_of_movies = len(movies_list);
    count =0; 
    for i in range(1,num_of_movies):
        movie_len = len(movies_list[i][0])
        count += movie_len-1
        for j in range(1,movie_len+1):
            temp_str = movies_list[i][0][:j].lower()
            if temp_str in movies_index:
                movies_index[temp_str].append(i)
            else:
                movies_index[temp_str] = [i]
     
    logging.info("N- gram index with size =" +str(len(movies_index)) );
    print count

   
    

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

    global movies_list
    movies_list = []
    parse_csv(options.csv_filename,movies_list)
    logging.info(" CSV File" + options.csv_filename + " parsed successfully with num of movies  :: " + str(len(movies_list)));
    create_dict_for_auto_completion()
    server = HTTPServer(("localhost", 8003), MyRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.exception(e)
        sys.exit(1)
    
