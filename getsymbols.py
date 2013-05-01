'''
Gets the necessary symbols.

Uses the symbols.txt file to get special unicode characters. Each character
should be on its own line, represented in the &#xxxx; format. The file can be
annotated using comments preceded by '//'.
'''

import sys
import string
import re, htmlentitydefs

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
def symbolAndDescrList(filename):
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
# Creates a dictionary of fullwidth alphabet characters.
#
# @return Dictionary of alphabet -> fullwidth alphabet.
def fullwidthAlphabet():
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
def circledAlphabet():
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

##
# Get gradient symbols.
#
# @return List of gradient lists.
def gradients():
    fullwidth = [u"\u3000", u"\uFF0E", u"\uFF0C", u"\uFF0A", u"\uFF1A",
                 u"\uFF1B", u"\uFF0B", u"\uFF1D", u"\uFF4F", u"\uFF41",
                 u"\uFF18", u"\uFF06", u"\uFF03", u"\uFF20"]
    cjk1 = [u"\u3000", u"\u4E36", u"\u51AB", u"\u2EA6", u"\u4EBB", u"\u5165",
            u"\u516C", u"\u519C", u"\u517F", u"\u5164", u"\u4B1F", u"\u4A3A"]
    cjk2 = [u"\u3000", u"\u4E37", u"\u5196", u"\u5182", u"\u518B", u"\u5183",
            u"\u5184", u"\u518A", u"\u2EB4", u"\u5193", u"\u418F", u"\u4C13"]
    cjk3 = [u"\u3000", u"\u2E80", u"\u52F9", u"\u52FA", u"\u52FB", u"\u52FF",
            u"\u5306", u"\u530A", u"\u530D", u"\u5314", u"\u41AF", u"\u4868"]
    cjk4 = [u"\u3000", u"\u4E37", u"\u4EBA", u"\u53EA", u"\u56DA", u"\u56E0",
            u"\u56EA", u"\u56EB", u"\u5703", u"\u571E", u"\u4279", u"\u9F98"]
    rect = [u"\u3000", u"\u2591", u"\u2592", u"\u2593"]

    gradients = [fullwidth, cjk1, cjk2, cjk3, cjk4, rect]
    return gradients
