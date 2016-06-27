import urllib2
import json
import threading
import time

api_key = 'Get one from api.nasa.org'



with open('apikeys.json', 'r') as f:
    
    api_key = json.load(f)['NASA']
               

url = 'https://api.nasa.gov/neo/rest/v1/feed?' + 'api_key=' + api_key
asteroiddata = ''

class datagrabber(object):
    
    def __init__(self):
        self.data = ''

    def getdata(self):
        while True:
        
            asteroiddata = json.load(urllib2.urlopen(url))
            print 'ASTEROID DATA UPDATED'
            self.data = asteroiddata
            time.sleep(600)
    
    def returndata(self):
        
        if self.data != '':
            
            return self.data
        
        else:
            
            while self.data == '':
                
                pass
            
            return self.data
        
def checkifsafe():
    
    asteroiddata = newdatagrabber.returndata()
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

newdatagrabber = datagrabber()
getdatathread = threading.Thread(target=newdatagrabber.getdata)
#getdatathread.setDaemon(True)
getdatathread.start()
