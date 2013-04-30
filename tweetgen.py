'''
Generates tweets.
'''

import getsymbols as get
import random
import string

em = u"\u2003"

##
# Generate a random tweet.
#
# @param symbols List of Unicode symbols.
# @return Tweet.
def genRandomTweet(symbols):
    numSymbols = len(symbols)
    if (numSymbols == 0): return ""

    # As of March 13, 2013, Twitter has newlines!
    # This makes twitterart a lot easier, since we don't have to insert spaces
    # to force a break, and standardizes formatting across web and mobile.

    charPerLine = 15
    numLines = 8
    tweet = ""

    # Randomize the hashtag
    x = random.randint(1,10)
    if (x < 9): hashtag = ""
    elif (x == 9): hashtag = "#140art"
    else: hashtag = "#twitterart"

    # If only one symbol, populate the tweet
    if (numSymbols == 1):
        for i in xrange(numLines):
            tweet += symbols[0]*charPerLine
            tweet += '\n'
        tweet = tweet[:-1] + " " + hashtag
        print tweet
        return tweet

    # Tweets are randomly decided
    # e.g. numLines = 7
    #      chars = [[1,2],[3,4,5]]
    #      shift = [0,2]
    #
    #   121212121212121212
    #   345345345345345345
    #   121212121212121212
    #   534534534534534534
    #   121212121212121212
    #   453453453453453453
    #   121212121212121212

    # Determining different lines, and lines in total
    diffLines = random.randint(1,3)
    print "diffLines = " + str(diffLines)

    # Doubling up on symbols
    x = random.randint(0,4)
    for i in xrange(x):
        pick = random.randint(0, len(symbols)-1)
        symbols.append(symbols[pick])
    print "random add = " + str(x)

    # Determining different characters per line
    shiftLine = []
    chars = []
    for i in xrange(diffLines):
        if (numSymbols == 2): diffCharPerLine = random.randint(1,2)
        else: diffCharPerLine = random.randint(1,3)
        print "diffCharPerLine = " + str(diffCharPerLine)
        shiftLine.append(random.randint(0,diffCharPerLine-1))
        chars.append(random.sample(symbols, diffCharPerLine))

    print "shiftLine = ",
    print shiftLine
    print "chars = ",
    print chars

    shift = [0 for i in xrange(numLines)]
    for i in xrange(numLines):
        diffLineIndex = i % diffLines
        s = shiftLine[diffLineIndex]
        if (s == 0):
            shift[i] = 0
        else:
            l = (i/diffLines) + 1
            shift[i] = (s*l) % diffLines

    print "shift = ",
    print shift

    # Assembling the tweet
    for i in xrange(numLines):
        line = chars[i % diffLines]
        start = shift[i]
        for j in xrange(charPerLine):
            c = j % len(line)
            tweet += line[(start + c) % len(line)]
        tweet += '\n'
    tweet = tweet[:-1] + " " + hashtag

    print tweet
    return tweet

##
# Generate a text tweet with symbols.
#
# @param message Text to turn circular or full-width.
# @param replyHandle (optional) Twitter handle to reply to.
# @return Their tweet, circular-ified or full-widthified.
def genTextTweet(message, replyHandle=""):
    handle = "@tartbot"

    # Determine type of symbols
    if ("-c" in message):
        alphabet = get.getCircledAlphabet()
        message = string.replace(message, "-c", "").strip()
    elif ("-w" in message):
        alphabet = get.getFullwidthAlphabet()
        message = string.replace(message, "-w", "").strip()
    else:
        coin = random.randint(0, 1)
        if (coin == 0): alphabet = get.getCircledAlphabet()
        else: alphabet = get.getFullwidthAlphabet()

    # Converts a message with the exception of Twitter handles
    def convertTweet(message):
        conversion = ""
        convert = True
        for i in xrange(len(message)):
            if (convert):
                if (message[i] == "@"):
                    convert = False
                    char = message[i]
                else:
                    char = alphabet.get(message[i], message[i])
            else:
                if (message[i] == " "):
                    convert = True
                char = message[i]
            conversion += char
        return conversion

    tweet = ""

    # Replace occurrences of @tartbot with replyHandle
    if (not replyHandle == ""):
        replyHandle = "@" + replyHandle + " "
        numMentions = string.count(message, handle)

        if (numMentions < 1):
            tweet = convertTweet(message)

        elif (numMentions == 1):
            index = string.find(message, handle)
            first = convertTweet(message[:index])
            last = convertTweet(message[index + len(handle):])
            tweet = first + replyHandle + last

        else:
            for i in xrange(numMentions):
                index = string.find(message, handle)
                first = convertTweet(message[:index])
                last = convertTweet(message[index + len(handle):])
                tweet += first + replyHandle + last
    else:
        tweet = convertTweet(message)

    if (len(tweet) > 140): tweet = tweet[:140]

    print tweet
    return tweet

##
# Generate a tweet from a photo.
#
# @param
# @return
def genPhotoTweet(photo, replyHandle):
    gradient = []

    replyHandle = em + "@" + replyHandle
    numRows = 7
    numCols = 11
    numShadedCols = 0

    # Get dimensions
    height = photo
    width = photo
    ratio = (height/numRows) / (width/11)

    if (ratio <= .5): numRows = 3
    elif (.500 < ratio and ratio <= .643): numRows = 4
    elif (.643 < ratio and ratio <= .786): numRows = 5
    elif (.786 < ratio and ratio <= .929): numRows = 6
    # .929 < ratio <= 1.12 is the default 7 x 11 tweet
    elif (1.12 < ratio and ratio <= 1.40): numShadedCols = 1
    elif (1.40 < ratio and ratio <= 1.89): numShadedCols = 2
    elif (1.89 < ratio and ratio <= 2.94): numShadedCols = 3
    else: numShadedCols = 4  # ratio > 2.94

    # Analyze photo

    tweet = ""
    tweet += replyHandle

    print tweet
    return tweet
