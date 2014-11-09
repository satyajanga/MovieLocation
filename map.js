
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
    var bounds = new google.maps.LatLngBounds ();
    for (var i = 0; i < jsonData.location.length; i++) {
    var location = new google.maps.LatLng(jsonData.location[i].lat,jsonData.location[i].lng);
    var infoWindow = new google.maps.InfoWindow({
              content: jsonData.location[i].content
                });
    bounds.extend(location);
    addMarker(location,jsonData.location[i].content);
    }
    map.fitBounds(bounds);
}
google.maps.event.addDomListener(window, 'load', initialize);
