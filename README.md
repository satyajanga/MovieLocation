SF Movie set locations
=============

<b>Problem </b>

1) User should be able to search the movie based on autocompletion search 
2) Showing the locations of the selected movie on Google Maps API

<b> Solution </b>

1) Download the data from the https://data.sfgov.org/Culture-and-Recreation/Film-Locations-in-San-Francisco/yitu-d5am?

2) To mark a location on Google Maps it must be in Longitude, Latitude coordinates. So convert the locations in the data file to Lat Long coordinates using Google MAPS Geocode API and add to the file.

3) Create a HTTP server and load this data during the application startup.
 
4) Preprocessing :While loading the data create a index on all the prefixes of all the movie names, which helps in fast processing of each single request. 

5) Host it on AWS.

<b>Technical Choices</b>

The solution focuses mainly backend and a bit of frontend. 
The stack I choose
1) Python (Beginner) 
    Python has always been simple to develop and easy to learn language. 
2) Javascript & JQuery(Completely new)
    There is vast support and documentation for Google Maps API in Javascript and For autocompletion search I chose JQuery. 
3) Google MAPS API(Completely new).

4) Bottle for light weight WSGI supported python application server(Completely new).
    Thanks to its light weight, we can deploy bottle.py  along with our source code

5) AWS 
<b> URL </b>
http://movielocationtmp-env.elasticbeanstalk.com/

<b> If I had more time</b>

I will make the front end more user friendly and I will also add a help section.
Processing and keeping all movies data in memomry in not scalable approach So I will add a mysql database which helps in scaling the applciation in the presence of huge data.
