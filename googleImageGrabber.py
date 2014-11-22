import urllib2
import simplejson
import cStringIO

fetcher = urllib2.build_opener()
searchTerm = 'parrot'
startIndex = 0
searchUrl = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=" + searchTerm + "&start=" + str(startIndex)
f = fetcher.open(searchUrl)
a =  simplejson.load(f)

imageUrl = a['responseData']['results'][0]['unescapedUrl']
print imageUrl

file = cStringIO.StringIO(urllib.urlopen(imageUrl).read())
img = Image.open(file)
print img
