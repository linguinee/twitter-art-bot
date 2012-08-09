'''
Twitter bot that generates twitter/symbol art.
By Ling-Yi Kung (https://github.com/linguinee).

Uses Twython (https://github.com/ryanmcgrath/twython).
'''

from twython import Twython
import getsymbols as get
import tweetgen as tweet
import getauthentication as authenticate
import random
import sys
import time

##
# Get pending mentions.
#
# @return Number of tweets replied to.
def checkMentions():
    replied = 0

    # Get ID of last replied tweet
    f = open("lastReply.txt")
    lastId = f.read()
    f.close()
    mentions = api.getUserMentions(since_id=lastId, include_entities=True)
    if (len(mentions) == 0): return 0
    
    i = 0
    for mention in mentions:
        userName = mention['user']['screen_name']
        text = mention['text']
        tweetId = str(mention['id'])
        print "tweetId = " + tweetId
        print "userName = " + userName
        print "text = " + text

        # Check for commented RT
        if (("via" in text) or ("RT" in text)):
            continue

        # Check for photo media
        try:
            photo = mention['entities']['media'][0]['media_url']
            continue
            #t = tweet.genPhotoTweet(photo, userName)
        except KeyError:
            print "No media found."
            t = tweet.genTextTweet(text, userName)

        # Tweet!
        api.updateStatus(status=t, in_reply_to_status_id=tweetId)
        replied += 1

        # First ID is the most current one
        if (i == 0): lastId = tweetId
        i += 1

    # Save last replied tweet ID
    f = open("lastReply.txt", "w")
    f.write(lastId)
    f.close()
    
    return replied

##
# Tweet some Twitter art.
#
# 18 characters + em space (&emsp;) per line.
def tweetArt():
    r = random.randint(0, 9)
    
    if (r < 7):
        # Picking symbols based on descriptors
        picked = descrs[random.randint(0,len(descrs)-1)][1]
        for p in picked: print p,
    else:
        # Picking symbols randomly
        picked = random.sample(symbols, random.randint(2,9))
        for p in picked: print p,

    print "\n"
    t = tweet.genRandomTweet(picked)
    if (t == ""): print "Tweet failed."
    else: api.updateStatus(status=t)

##
# Get #140art and #twitterart tweets. Retweet those with +100 RTs.
#
# @return Number of tweets retweeted.
def retweetPopularArt():
    retweeted = 0

    # Make sure nothing gets retweeted twice
    lastId = api.retweetedByMe(count=1)
    if (len(lastId) == 0): lastId = 0
    else: lastId = lastId[0]['id']

    # If the tweet has +100 RTs, retweet
    def RT(t):
        tweetId = str(t['id'])
        count = api.showStatus(id=tweetId)['retweet_count']
        if (count < 100): return False
        else:
            print t['text']
            api.reTweet(id=tweetId)
            return True
    
    twitterArt = api.search(q="#twitterart", since_id=lastId)['results']
    if (len(twitterArt) > 0):
        for t in twitterArt:
            if (RT(t)): retweeted += 1

    art = api.search(q="#140art", since_id=lastId)['results']
    if (len(art) > 0):
        for t in art:
            if (RT(t)): retweeted += 1

    print str(retweeted) + " retweeted."
    return retweeted

##
# Init.
print "Starting Twitter art bot..."

# Get authentication info
authInfo = authenticate.getAuthentication();
try:
    consumer_key = authInfo["CONSUMER_KEY"]
    consumer_secret = authInfo["CONSUMER_SECRET"]
    access_token = authInfo["ACCESS_TOKEN"]
    access_token_secret = authInfo["ACCESS_TOKEN_SECRET"]
except KeyError:
    print "Key does not exist. Check authentication.txt."
    raise

# Access Twitter through Twython
print "Accessing Twitter..."
api = Twython(app_key=consumer_key,
              app_secret=consumer_secret,
              oauth_token=access_token,
              oauth_token_secret=access_token_secret)

# Get symbols for use
print "Loading symbols..."
symbols, descrs = get.getSymbolAndDescrList("symbols.txt")

##
# Main loop that runs.
#
# Checks mentions every two minutes.
# Tweets something random every sixteen minutes.
# Looks for something to retweet every hour.
print "Bot initialized.\n"
replyInterval = 120

tweetTime = 8
retweetTime = 30
tw = tweetTime
rt = retweetTime

while(1):
    
    # Check mentions
    print "\nChecking mentions..."
    numReplies = checkMentions()
    print "Replied to " + str(numReplies) + " mentions."

    # Tweet something
    if (tw == tweetTime):
        print "\nGenerating art..."
        tweetArt()
        tw = 0
    else:
        tw += 1

    # Retweet something
    if (rt == retweetTime):
        print "\nSearching for art to retweet..."
        retweetPopularArt()
        rt = 0
    else:
        rt += 1

    time.sleep(replyInterval)