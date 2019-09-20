# Variables that contains the user credentials to access Twitter API from Step 1
# Replace this with your own credentials
consumer_key = ' '
consumer_secret = ' '
access_token = ' '
access_token_secret = ' '

# Hashtag: "#dog" is rare, so I just crawling all tweets with any hashtag.


#Import the necessary methods/packages from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import json
import csv

import os
path = os.path.join(os.path.expanduser('~'), "outputs/Lab2")

class StdOutListenerV2(StreamListener):

    def __init__(self, time_limit=40):
        # start_time: is the start running time of the program
        self.start_time = time.time()
        # limit is the the assigned running time of the program, its default value is 40
        self.limit = time_limit
        # csvfile is the file to store the data
        self.csvfile = open(path + '/Twitter_Data_NY_Hash.csv', 'w')
        #self.csvwriter = csv.writer(csvfile)
        
        super(StdOutListenerV2, self).__init__()
        
    
    # The on_data function will keep crawling the twitter posts one by one, and store them into the data parameter
    # There are only two ways to stop the program inside:
    #                The on_data function returns false
    #                The on_error function catches a error
    def on_data(self, data):
        #  check if the program exceeded the time_limit of running time
        if (time.time() - self.start_time) < self.limit:
            # convert data to json format
            d = json.loads(data)
            
            # check whether the current twitter post has coordinates
            geo_flag = 0
            try:
                lon = d['coordinates']['coordinates'][0]
                lat = d['coordinates']['coordinates'][1]
                geo_flag = 1
            except:
                print('no coordinates')

            # We only want to see the twitter posts with coordinates
            if ( geo_flag == 1 ):
                text = d['text'].rstrip().replace('\n', ' ')
                if '#' in text.lower():
                    creat_time = d['created_at']
                    print( 'catch data with coordinates and hashtag' )
                    # use str() to convert double/float to string
                    #self.csvwriter.writerow( [creat_time, str(lon), str(lat), text] )
                    self.csvfile.write( creat_time + "," + str(lon) + "," + str(lat) + "," + text.replace(',', ';') + '\n')
                    return True
                else:
                    print('no hashtag')
        # If time exceeded, stop the program.
        else: 
            self.csvfile.close()
            return False

    # If an error occured, stop the program
    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    # This handles Twitter authentification and the connection to the Twitter Streaming API
    l = StdOutListenerV2(1000)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # A comma-separated list of longitude,latitude pairs specifying a set of bounding boxes to filter Tweets by
    # e.g. [-122.75,36.8,-121.75,37.8] indicates the area of San Francisco
    stream.filter(locations=[-74, 40, -73, 41])