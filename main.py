# -*-coding: utf-8 -*-
import urllib,urllib2,cookielib,re,os,json
import HTMLParser
from progressbar import *
from widgets import *
import progressbar
import socket
h = HTMLParser.HTMLParser()
hash=set()
username=raw_input("Enter username:")
password=raw_input("Enter password:")

try:
	f = open('dl.db', 'r')
	data=json.loads(f.read())
	f.close()
except:
	data={}
widgets = [Percentage(), Bar(marker=RotatingMarker('>-=')),' ', Timer(),
	   '/', ETA(),' ', FileTransferSpeed()  ]
pbar = ProgressBar(widgets=widgets, maxval=10001).start()
def dlProgress(count, blockSize, totalSize):
	global progress
	pbar.maxval = totalSize
	try:
		pbar.update(count*blockSize)
		progress=10000*count*blockSize/totalSize
	except:
		pass
def fetch(packname):
	global username,regex2,regex1,hash
	packid=1
	while(1):
		req='http://osu.ppy.sh/pages/include/packlist-info.php?n='+packname+str(packid)
		print req
		content = urllib2.urlopen(req).read()
		if ('li' in content):
			print "Found"
			pattern = re.compile(r'<a href="/s/(\d+)">(.*?)</a>.*?CLEARED')
			nums = pattern.findall(content)
			for s in nums:
				setid=s[0]
				try:
					data[setid]
				except:
					beatmap=s[1]
					print setid, beatmap
					urllib.urlretrieve('http://bloodcat.com/osu/m/'+setid, "dl/"+setid+" "+beatmap+".osz", reporthook=dlProgress)
					print "dl/"+setid+" "+beatmap+".osz"
					data[setid]=1
					f = open('dl.db', 'w+')
					f.write(json.dumps(data))
					f.close()
			packid+=1
		else:
			break

cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

postdata=urllib.urlencode({
	'username':username,
	'password':password,
	'login':"login",
	'autologin':"on",
})
print 'Logging in...'
req = urllib2.Request(
	url = 'http://osu.ppy.sh/forum/ucp.php',
	data = postdata)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')
result = urllib2.urlopen(req).read()

print 'Logged in... Enter to continue'
raw_input()
fetch('S')
fetch('SA')
fetch('R')