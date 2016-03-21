from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import ex as s



#consumer key, consumer secret, access token, access secret.
from apidetails import *


class listener(StreamListener):

    def on_data(self, data):
        try:
            all_data = json.loads(data)                             #load twiiter stream data

            tweet = all_data["text"]                                #load all text data from stream
            sentiment_value, confidence = s.sentiment(tweet)        #run sentiment analysis
            print(tweet, sentiment_value, confidence)

            if confidence*100 >= 80:                                #cinfidence filter to ensure no false results
                output = open("twitter-out.txt", "a")               #write sentiment to .txt file
                output.write(sentiment_value)
                output.write('\n')
                output.close()

            return True
        except:
            return True

    def on_error(self, status):
        print(status)


#twitter api settings
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)


#stream init
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["bernie"])                                #haha:D