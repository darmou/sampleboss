'''
Origonal script at http://blog.prashanthellina.com/2008/04/22/alexa-rank-a-script-to-get-the-rank-for-any-site/
class allows one to find the popularity and reach rank
'''

import sys
import re
import urllib2
from xml.dom.minidom import parseString

class AlexaRank():
    
    def get_alexa_rank(self, url):
        try:
            data = urllib2.urlopen('http://data.alexa.com/data?cli=10&dat=snbamz&url=%s' % (url)).read()
            dom = parseString(data.strip())
            
            #f = open('/tmp/alexa', 'w')
            #f.write("Data: " + str(data)+"/n")
            #f.write(str(self._googlerank)  + "\n")
            #f.close()
            
            reach_rank = re.findall("REACH[^\d]*(\d+)", data)
            if reach_rank: reach_rank = reach_rank[0]
            else: reach_rank = -1

            popularity_rank = re.findall("POPULARITY[^\d]*(\d+)", data)
            if popularity_rank: popularity_rank = popularity_rank[0]
            else: popularity_rank = -1

            return int(popularity_rank), int(reach_rank)

        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            return None

    def get_poplarity_rank(self, url):
        popularity_rank, reach_rank = -1, -1
        data = self.get_alexa_rank(url)
        if data:
            popularity_rank, reach_rank = data
        
        return popularity_rank
