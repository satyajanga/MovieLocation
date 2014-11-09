import helpers
from urllib import urlencode
import unittest

SEARCH_ENDPOINT = "movies"
LOCATION_ENDPOINT = "get_locations"
class Test_Movies(unittest.TestCase):
    def test_search_by_empty(self):
        query_params = "movie= "
        response = helpers.get_response(query_params, SEARCH_ENDPOINT)
        self.assertEqual(len(response['movies']),0)

    def test_search_by_valid_keyword(self):
        query_params = "movie=al"
        response = helpers.get_response(query_params, SEARCH_ENDPOINT)
        self.assertEqual(len(response['movies']),3)
          
    def test_search_by_non_existent_keyword(self):
        query_params = "movie=notexists"
        response = helpers.get_response(query_params, SEARCH_ENDPOINT)
        self.assertEqual(len(response['movies']),0)
    
    def test_search_by_complete_movie_name(self):
        query_params = urlencode({"movie":"Around the Fire"})
        response = helpers.get_response(query_params, SEARCH_ENDPOINT)
        self.assertEqual(len(response['movies']),1)

    def test_get_locations_by_empty_movie_name(self):
        query_params = "movie= "
        response = helpers.get_response(query_params, LOCATION_ENDPOINT)
        self.assertEqual(len(response['location']),0)
        
    def test_get_locations_by_valid_movie_name(self):
        query_params = urlencode({"movie":"Around the Fire"})
        response = helpers.get_response(query_params, LOCATION_ENDPOINT)
        self.assertEqual(response['location'][0]['lat'],"37.7593749")
        self.assertEqual(response['location'][0]['lng'],"-122.5108057")
        
    def test_get_locations_by_non_existent_movie_name(self):
        query_params = "movie=nonexistentmovie"
        response = helpers.get_response(query_params, LOCATION_ENDPOINT)
        self.assertEqual(len(response['location']),0)



