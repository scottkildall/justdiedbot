import urllib2
import simplejson
#import cStringIO
from PIL import Image
import requests
from io import BytesIO


fetcher = urllib2.build_opener()
searchTerm = 'parrot'
startIndex = 0
searchUrl = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=" + searchTerm + "&start=" + str(startIndex)
f = fetcher.open(searchUrl)
a =  simplejson.load(f)

print a
imageUrl = a['responseData']['results'][0]['unescapedUrl']
#print imageUrl
imageUrl = "http://pngimg.com/upload/parrot_PNG713.png"

response = requests.get(imageUrl)
img = Image.open(BytesIO(response.content))
img.save('tweetImage.png')

#imageFile = cStringIO.StringIO(urllib2.urlopen(imageUrl).read())
#print imageFile

#img = Image.open(file)
#print img
