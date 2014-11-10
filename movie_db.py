import logging
from csv_util import parse_csv
import json
class MovieDB:
    """ 
    Initializes the class and calls the preprocessing fuction 
    Args:
    csv_file :: Name of the CSV File that contains the data
    """
    def __init__(self,csv_file):
        self.csv_file = csv_file
        self.movies_data = []
        self.movies_prefix_index ={}
        self.load_and_process_data()
    
    """
    Creates indexing on all the prefixes of movie names, 
    which helps in faster search for autocompletion queries
    """
    def load_and_process_data(self):
        parse_csv(self.csv_file,self.movies_data);
        logging.info(" CSV File" + self.csv_file + " parsed successfully with num of movies  :: " + str(len(self.movies_data)));
        num_of_movies = len(self.movies_data);
        count =0; 
        for i in range(1,num_of_movies):
            movie_len = len(self.movies_data[i][0])
            count += movie_len-1
            for j in range(1,movie_len+1):
                temp_str = self.movies_data[i][0][:j].lower()
                if temp_str in self.movies_prefix_index:
                    self.movies_prefix_index[temp_str].append(i)
                else:
                    self.movies_prefix_index[temp_str] = [i]
    
    """
    Searches the prefix index and return all the matching movie names
    Args:
    movie_prefix : input from user during search
    """
    def search_with_prefix(self,movie_prefix):
        try:
            movie_name_idx = self.movies_prefix_index[movie_prefix]
        except:
            movie_name_idx=[]
        movies=[]
        for i in movie_name_idx:
            movies.append(self.movies_data[i][0])
        
        movies_names={'movies' : list(set(movies))};
        return json.dumps(movies_names)

    """
    Returns all the necessary movie information for the selected movie
    Args:
    movie_name:: User selected movie name

    """
    def get_locations_by_name(self,movie_name):
        try:
            movie_name_idx = self.movies_prefix_index[movie_name]
        except:
            movie_name_idx=[]
        cols = len(self.movies_data[0])
        locations={'location' : []};
        for i in movie_name_idx:
            location = {}
            location['lat'] = self.movies_data[i][cols-2];
            location['lng'] = self.movies_data[i][cols-1];
            location['content'] = "Movie Name : " + self.movies_data[i][0]+"\nYear :: "+ self.movies_data[i][1] + "\nCast ::" + self.movies_data[i][8]+"," + self.movies_data[i][9] + "," + self.movies_data[i][10] + "\nTrivia :: " + self.movies_data[i][3]   
            locations['location'].append(location)
                                                                             
        return json.dumps(locations);


