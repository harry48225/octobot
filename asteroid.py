import urllib2
import json


api_key = 'Get one from api.nasa.org'



with open('apikeys.json', 'r') as f:
    
    api_key = json.load(f)['asteroid']
               

url = 'https://api.nasa.gov/neo/rest/v1/feed?' + 'api_key=' + api_key
def getdata():
    
    asteroiddata = json.load(urllib2.urlopen(url))
    return asteroiddata

def checkifsafe():
    
    asteroiddata = getdata()
    asteroiddatekeys = asteroiddata['near_earth_objects'].keys()
    dangerousasteroids = 0
    safeasteroids = 0
    
    for key in asteroiddatekeys:
        
        asteroids = asteroiddata['near_earth_objects'][key]
        
        for asteroid in asteroids:
            
            if asteroid['is_potentially_hazardous_asteroid']:
                
                
                dangerousasteroids += 1
                
            else:
                
                safeasteroids += 1
                
    return 'There are: {0} asteroids that will not hit us, and {1} that will.'.format(safeasteroids, dangerousasteroids)

