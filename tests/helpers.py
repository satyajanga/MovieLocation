

import json
import urllib2
from config import config

def get_response(query_param,end_point):
    url = "http://"+config['host'] + "/" + end_point +"?"+ query_param
    return json.loads(urllib2.urlopen(url).read())
