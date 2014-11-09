import logging
from csv_util import parse_csv
import json
class ProcessMovies:
    def __init__(self,csv_file,log_file):
        self.csv_file = csv_file
        self.log_file = log_file
        self.movies_data = []
        self.movies_prefix_index ={}
        self.load_and_process_data()
    
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
            location['content'] = "Movie Name : " + self.movies_data[i][0]+"\nLocation :: "+ self.movies_data[i][2]   
            locations['location'].append(location)
                                                                             
        return json.dumps(locations);

