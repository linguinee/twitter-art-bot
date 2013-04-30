'''
Gets the necessary symbols.

Uses the symbols.txt file to get special unicode characters.
'''

import sys
import re, htmlentitydefs
import string

##
# Removes HTML or XML character references and entities from a text string.
# By Fredrik Lundh, from http://effbot.org/zone/re-sub.htm#unescape-html.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # Character reference
            try:
                if text[:3] == "&#x": return unichr(int(text[3:-1], 16))
                else: return unichr(int(text[2:-1]))
            except ValueError: pass
        else:
            # Named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError: pass
        return text
    return re.sub("&#?\w+;", fixup, text)

##
# Parse symbols.txt file.
#   HTML characters are on separate lines.
#   Comments come after the characters and are preceded by "//".
#
# @param filename The symbols.txt file path.
# @return symbols List of Unicode symbols.
# @return descrs List of [descriptors, [symbols,...]].
def getSymbolAndDescrList(filename):
    f = open(filename)
    symbolFile = f.read()
    symbolFile = symbolFile.split("\n")
    f.close()

    symbols = []
    descrs = []
    for i in xrange(len(symbolFile)):
        if (symbolFile[i] == ""): continue
        line = symbolFile[i].split("//")

        # Get symbol
        symbol = unescape(line[0].strip())
        if (symbol == ""): continue
        else: symbols.append(symbol)

        # Get descriptor(s)
        if (len(line) < 2): continue
        descr = line[1].strip()
        descr = descr.split(" ")
        for descriptor in descr:
            d = descriptor.strip()
            if (d == ""): continue

            found = -1
            for i in descrs:
                if (d in i):
                    i[1].append(symbol)
                    found = i
                    break
                else: continue

            if (found == -1): descrs.append([d, [symbol]])

    return symbols, descrs

##
# Search symbols.txt for specific symbols.
#   HTML characters are on separate lines.
#   Comments come after the characters and are preceded by "//".
#
# @param filename The symbols.txt file path.
# @param wanted List of descriptors of the symbol(s) to search for.
# @param unwanted List of descriptors not wanted.
# @return List of Unicode symbol(s) matching descr.
def getSymbols(filename, wanted, unwanted):
    f = open(filename)
    symbolFile = f.read()
    symbolFile = symbolFile.split("\n")
    f.close()

    desired = []
    for i in xrange(len(symbolFile)):
        if (symbolFile[i] == ""): continue
        symbol = symbolFile[i].split("//")
        if (len(symbol) < 2): continue

        giveBack = True
        for yes in wanted:
            if (yes not in symbol[1]):  # symbol doesn't have descr
                giveBack = False
                break
            else:
                for no in unwanted:     # symbol has unwanted descr
                    if (no in symbol[1]): giveBack = False

        symbol = symbol[0].strip()
        if (giveBack and (symbol != "")): desired.append(unescape(symbol))

    return desired

##
# Get box drawing symbols.
#
# @return List of Unicode box drawing symbols.
def getBoxDrawings():
    first = 9472  # box drawings light horizontal
    last = 9599   # box drawings heavy up and light down
    symbols = []

    for i in xrange(last - first):
        symbol = "&#" + str(first + i) + ";"
        print unescape(symbol),
        symbols.append(unescape(symbol))

    return symbols

##
# Creates a dictionary of fullwidth alphabet characters.
#
# @return Dictionary of alphabet -> fullwidth alphabet.
def getFullwidthAlphabet():
    alphabet = '!"#$%&'
    alphabet += "'()*+,-./0123456789:;<=>?@"
    alphabet += "ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_"
    alphabet += "abcdefghijklmnopqrstuvwxyz{|}~"

    alphabetDict = {}
    for letter in alphabet:
        alphabetDict[letter] = unichr(0xFEE0 + ord(letter))

    return alphabetDict

##
# Creates a dictionary of circled alphabet characters.
#
# @return Dictionary of alphabet -> circled alphabet.
def getCircledAlphabet():
    alphabet =  "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphabet += "abcdefghijklmnopqrstuvwxyz"
    alphabet += "0"

    alphabetDict = {}
    firstLet = 9398  # circled capital letter A
    last = 9450      # circled number zero

    for i in xrange(last - firstLet):
        symbol = "&#" + str(firstLet + i) + ";"
        alphabetDict[alphabet[i]] = unescape(symbol)

    alphabet = "123456789"
    firstNum = 9312  # circled number one
    lastNum = 9320   # circled number nine

    for i in xrange(lastNum - firstNum):
        symbol = "&#" + str(firstNum + i) + ";"
        alphabetDict[alphabet[i]] = unescape(symbol)

    return alphabetDict
