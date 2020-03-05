import tweepy
import random
from credentials import *
from textblob import TextBlob

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status, count=1):
        print (status.text)
        print (status.user.screen_name)
        analysis = TextBlob(str(status.text))
        goodreply = ["Thanks for the nice tweet!", "Good Tweet!","Thanks!","I appreciate it!", "Great Tweet!","Great, thanks!"]
        badreply = ["Thanks.... :/","凸(¬д¬)凸","ಠ_ಠ","Thanks, but no thanks.","No, thank you.","Not good."]
        neutralreply = ["I see what you did there.","I can't complain.","Seems normal to me.","Thanks! I'll check it out."]

        try:
            if analysis.sentiment.polarity > 0.2:
                api.update_status("@"+status.user.screen_name+" "+random.choice(goodreply),  in_reply_to_status_id = status.id)
                print(status.text)
                print(analysis.sentiment.polarity)
            elif analysis.sentiment.polarity < -0.2:
                api.update_status("@"+status.user.screen_name+" "+random.choice(badreply),  in_reply_to_status_id = status.id)
                print(status.text)
                print(analysis.sentiment.polarity)
            else:
                api.update_status("@"+status.user.screen_name+" "+random.choice(neutralreply),  in_reply_to_status_id = status.id)
                print(status.text)
                print(analysis.sentiment.polarity)

        except tweepy.TweepError as e:
            print(e.reason)


    def on_error(self, status_code):
        print (sys.stderr + ' Encountered error with status code: ' + status_code)
        return True # Don't kill the stream

    def on_timeout(self):
        print (sys.stderr + 'Timeout...')
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
sapi.filter(track=['@panekstations'])
