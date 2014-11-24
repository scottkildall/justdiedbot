# JustDiedBot
# by Scott Kildall
# to be added: some way to check for when names get misspelled
# maybe if there is a match in the age + any part of the name (first, middle, last)

from bs4 import BeautifulSoup
import urllib2
import datetime
import time

import tweeter as Tweeter

def Activate():
	# limit the max num of tweets each day
	maxDailyTweets = 10

	print "Activate called" 

	# generate the appropriate URL that has all the wikipeda 
	wikipediaURL =  generateURL()
	print wikipediaURL

	rawText = getRawURLText(wikipediaURL)
	tweetTodaysDeaths(rawText, maxDailyTweets)
	

# URL is something like:
# "http://en.wikipedia.org/wiki/Deaths_in_2014"
def generateURL():
        baseURL = "http://en.wikipedia.org/wiki/Deaths_in_"
	return baseURL + get_year()

def getRawURLText(wikipediaURL):
	# all of this will get the raw text for the wikipedia deaths page
        header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
        req = urllib2.Request(wikipediaURL,headers=header)
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page)

        # get raw text of page 
        return soup.get_text()

# the current year as a string, e.g. "2014"
def get_year():
        return datetime.datetime.today().strftime("%Y")

# e.g. "April 2014"
def get_monthyear():
	todayStr = datetime.datetime.today() 
 	return todayStr.strftime("%B %Y")

# e.g. if date is March 20th, 2010, this will return 20, strip leading zeros
def get_daydate():
	todayStr = datetime.datetime.today() 
 	todayStr = todayStr.strftime("%d")
 	return todayStr.lstrip("0")
    #date = datetime.now().strftime('%b %d %y')
    # In date string we store the date in format Month-Day-Year
    #return date

# returns our custom timestamp for tweet-logging
def get_timestamp():
	return datetime.datetime.today().strftime("%B %d %Y %H:%M")

def get_lastdied():
	# grab the last quote
	f = open("lastdied.txt", "r")
	lastdied = f.read()
	f.close
	return lastdied.rstrip('\n')

def tweet_death(diedStr):
	print "TWEETING: " + diedStr
	tweetStr = "RIP " + diedStr
	Tweeter.tweetMessage(Tweeter.getKeys("keys.txt"), tweetStr)
	log_tweet(tweetStr)

# writes all the dead people to a list, this is just for one day
def write_deathlist(lastDiedStr):
	f = open("deathlist.txt", "a")
	f.write(extractName(lastDiedStr))
	f.write("\n")
	f.close()

# writes all the dead people to a list, this is just for one day
def read_deathlist():
	f = open("deathlist.txt", "r")
	dList = []
	for line in f:
		dList.append( line.rstrip('\n') )
	f.close()
	return dList

# creates an empty file
def clear_deathlist():
	f = open("deathlist.txt", "w")
	f.close()

# removes the Wikipedia annotation
def clean_obituary(diedStr):
	# there is no annotation
	if diedStr.find('[') == -1:
		return diedStr
	else:
		return  diedStr[0:diedStr.index('[')]

def log_tweet(tweetStr):
	f = open("senttweets.txt", "a")
	f.write(tweetStr)
	f.write(" | ")
	f.write(get_timestamp())
	f.write("\n")
	f.close()

# short name
def extractName(line):
	return line[0:line.index(',')]


def tweetTodaysDeaths(rawText, maxDailyTweets):
	# look for the month, in format such as "February 2014"
	matchString = get_monthyear()

	# get the start line that contains the number
	startIndex = 0
	rawLines = rawText.split('\n')
	for line in rawLines:
		if line == matchString:
			break
		startIndex = startIndex + 1

	#now look for the current date, i.e. 20 for March 20th, 2014
	matchDateString = get_daydate()	
	foundEntries = False

	print matchDateString 

	# find the index for this date, just the day part of the date, e.g. "20
	for i in range(startIndex, len(rawLines)-1):
		if rawLines[i] == matchDateString:
			startIndex = startIndex + 1
			foundEntries = True
			break
		
		startIndex = startIndex + 1

	wikiDeathList = []

	# skip past leading blank lines
	if foundEntries == True:
		foundEntries = False
		for i in range(startIndex, len(rawLines)-1):
			if not rawLines[i]:
				# we have all the entries need
				if foundEntries == True:
					break
				else:
					foundEntries = True
			else:
				# add to array
				wikiDeathList.append(rawLines[i])
				#print extractName(rawLines[i])
				#print clean_obituary(rawLines[i])


	if len(wikiDeathList) == 0:
		# no entries, clear file, we are done
		clear_deathlist()

	# get today's list of the dead
	dList = read_deathlist()
		# make sure we haven't exceeded max number of daily tweets
	if len(dList) < maxDailyTweets:
	
		for line in wikiDeathList:
			encodeLine = line.encode('utf-8')
			if not extractName(encodeLine) in dList:
			
				# not in our list already
				tweet_death(clean_obituary(encodeLine))
				write_deathlist(encodeLine)

				# only tweet once/scrape in case of wiki-vandalism
				break

		


if __name__ == "__main__":
	Tweeter.tweetMessage(Tweeter.getKeys("keys.txt"), "Viktor Tikhonov, 84, Soviet ice hockey coach.")
	#Activate()
		
