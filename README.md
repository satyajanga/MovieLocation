SF In Movies
=============
Shows where movies have been filmed in San Fransico 

<b> URL </b>

http://movielocationtmp-env.elasticbeanstalk.com/

<b>Problem </b>

1) User should be able to search the movie based on autocompletion search 
2) Showing the locations of the selected movie on Google Maps API

<b> Steps in Solution </b>

These are the steps I sketched down after understanding the coding chanllenge.

1) Download the data from the https://data.sfgov.org/Culture-and-Recreation/Film-Locations-in-San-Francisco/yitu-d5am

2) To mark a location on Google Maps it must be in Longitude, Latitude coordinates. So convert the locations in the data file to Lat Long coordinates using Google MAPS Geocode API and add to the file.

3) Create a HTTP server and load this data during the application startup.
 
4) Preprocessing :While loading the data create a index on all the prefixes of all the movie names, which helps in fast processing of each single request. 

5) Need to have JQuery for querying the server during auto-completion search.
 
6) Host it on AWS.

<b>Technical Choices</b>

The solution focuses mainly backend and a bit of frontend. I chose following tech stack.

1) Python (Beginner) 
    I used python for some school assignment but Python has always been simple to develop and easy to learn language. So it didn't take much time to gather enough knowledge for this project. 

2) Javascript & JQuery(Completely new)
    Google MAPS has very good API in AJAX and For autocompletion search I found out that I should use JQuery. 

3) Google MAPS API(Completely new).
    Examples provided by Google MAPS are easy understand and also sufficient for this project. 

4) Bottle for light weight WSGI supported python application server(Completely new).
    Thanks to its light weight, we can deploy bottle.py  along with our source code. So I chose bottle compared to others. 

5) AWS 
    I haven't used AWS before but I was able to figure it out by spending some time on it.
     
<b> If I had more time</b>

I will make the frontend more user friendly and I will also add a help section.

Processing and keeping all movies data in memory in not scalable approach So I will add a mysql database which helps in scaling the applciation in the presence of huge data.
