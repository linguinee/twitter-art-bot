'''
Gets authentication info.

Expects an authentication.txt file in the same directory.
'''

import sys
import string

def getAuthentication():
    f = open("authentication.txt")
    authFile = f.read()
    authFile = authFile.split("\n")
    f.close()

    auth = {}
    for i in xrange(len(authFile)):
        if (authFile[i] == ""): continue
        keyValue = authFile[i].split("=")
        if (len(keyValue) != 2): continue

        # Get authentication codes
        key = keyValue[0].strip()
        value = keyValue[1].strip()
        auth[key] = value

    return auth
