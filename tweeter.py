from twython import Twython

# reaads a file and returns an array of 4 keys for Twitter. These are:
# [0] = Consumer Key
# [1] = Consumer Secret
# [2] = Access Token
# [3] = Access Secret
# keys are kept in a separate file so we don't have to load onto GitHub, a preceding '#' will act as a comment
def getKeys(keysFilename):
	# make array of all lines in the file - we have plenty of memory for this
	f = open( keysFilename, "r" )
	keys = []
	for line in f:
		if line[0] != '#': 
	    		keys.append( line.rstrip('\n') )
	f.close()
	return keys


# right now, just support for a string, no media
def tweetMessage(keys, tweetStr):
	api = Twython(keys[0],keys[1],keys[2],keys[3]) 
	api.update_status(status=tweetStr)
