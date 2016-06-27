import urllib2
import json

with open('apikeys.json', 'r') as f:
    api_key = json.load(f)['NASA']

url = 'https://api.nasa.gov/planetary/earth/imagery?'

def check(lat, longi):
    
    
    longstring = 'lon=' + str(longi)
    latstring = 'lat=' + str(lat)
    
    newurl = url + longstring + '&' + latstring + '&cloud_score=True&api_key=' + api_key
    print newurl
    
    imagedata = json.load(urllib2.urlopen(newurl))
    try:
        
        return 'You were last observed at {0}, the cloud cover was approximately {2}%, and here is the image {1}'.format(imagedata['date'], imagedata['url'], imagedata['cloud_score'])
    except:
        
        return 'Invaild Lat or long!'