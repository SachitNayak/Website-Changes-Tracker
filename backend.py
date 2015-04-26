from __future__ import print_function
from bs4 import BeautifulSoup
from urllib2 import *
import urllib2
import re
import os 




def make_list( filename ):
	f = open( filename ,'r')
	res = []                                                  #Stores each of the changes found
	z = 0
	for l in f:
		ln = l[0:5]
		sp = (ln[0].isdigit() and ln[1]=="_" and ln[2].isalpha() and ln[3]==".") 
		dp = (ln[0].isdigit()and ln[1].isdigit()and ln[2]=="_"and ln[3].isalpha()and ln[4]==".")
		pattern = (sp or dp)
		if(pattern and z==1):
			if( not( (s[8]=="\n") and ((s[7]=="\n") or (s[9]=="\n")) ) ):
				res.append(s)
			s = ""
		elif(pattern and z==0):
			s = ""
			z = 1
		s += l
	if( not( (s[8]=="\n") and ((s[7]=="\n") or (s[9]=="\n")) ) ): 
		res.append(s)                               #For excluding files which didnt have diff
	f.close()

	#print(res)                              #Gives \n version of o/p

	final=[]                     #Stores each of the changes as a list containing lineno,old,new.
	for i in range(0,len(res)):
		l=[]
		m = re.search("\n\d", res[i][11:])
		x = ((m != None) and (len( res[i][:m.start()].split("\n<",1) ) != 1))
		if( x or ((m == None) and (len( res[i].split("\n<",1) ) != 1)) ):
			l.append(res[i].split("\n<",1)[0].split("\n")[0])
			l.append(res[i].split("\n<",1)[0].split("\n")[1])
			m = re.search("\n\d", res[i].split("\n<",1)[1])
			y = ((m != None) and (len( res[i].split("\n<",1)[1][:m.start()].split("\n---\n>",1) ) != 1))
			if( y or ((m==None) and (len( res[i].split("\n<",1)[1].split("\n---\n>",1) ) != 1)) ):
				l.append(res[i].split("\n<",1)[1].split("\n---\n>",1)[0].strip())
				l.append(res[i].split("\n<",1)[1].split("\n---\n>",1)[1].strip())
			else:
				l.append("del")
				l.append(res[i].split("\n<",1)[1].strip())		
		else:
			l.append(res[i].split("\n>",1)[0].split("\n")[0])
			l.append(res[i].split("\n>",1)[0].split("\n")[1])
			l.append("add")
			l.append(res[i].split("\n>",1)[1].strip())
		while( len( l[ (len(l) - 1) ].split("\n", 1) ) != 1 ):
			if( l[ (len(l) - 1) ].split("\n", 1)[1][0].isdigit() ):
				s = l[ (len(l) - 1) ]
				l[ (len(l) - 1) ] = s.split("\n",1)[0]
				s = s.split("\n",1)[1]
				m = re.search("\n\d", s[2:])
				x = ((m!=None) and (len( s[:m.start()].split("\n<",1) ) != 1))
				if( x or ((m==None) and (len( s.split("\n<",1) ) != 1)) ):
					l.append(s.split("\n<",1)[0])
					m = re.search("\n\d", s.split("\n<",1)[1])
					y = ((m != None) and (len( s.split("\n<",1)[1][:m.start()].split("\n---\n>",1) ) != 1))
					if( y or ((m == None) and (len( s.split("\n<",1)[1].split("\n---\n>",1) ) != 1)) ):
						l.append(s.split("\n<",1)[1].split("\n---\n>",1)[0].strip())
						l.append(s.split("\n<",1)[1].split("\n---\n>",1)[1].strip())
					else:
						l.append("del")
						l.append(s.split("\n<",1)[1].strip())
				else:
					l.append(s.split("\n>",1)[0])
					l.append("add")
					l.append(s.split("\n>",1)[1].strip())
			elif( not ( l[ (len(l) - 1) ].split("\n", 1)[1][0].isdigit() ) ):
				s = l[ (len(l) - 1) ].split("\n", 1)[0] + "\n"
				r = l[ (len(l) - 1) ].split("\n", 1)[1]
				while( len( r.split("\n", 1) ) != 1 ):
					s = s + r.split("\n", 1)[0] + "\n"
					r = r.split("\n", 1)[1]
					if( r[0].isdigit() ):
						l[ (len(l) - 1) ] = s[:-1]
						m = re.search("\n\d", r[2:])
						x = ((m!=None) and (len( r[:m.start()].split("\n<",1) ) != 1))
						if( x or ((m==None) and (len( r.split("\n<",1) ) != 1)) ):
							l.append(r.split("\n<",1)[0])
							m = re.search("\n\d", r.split("\n<",1)[1])
							y = ((m != None) and (len( r.split("\n<",1)[1][:m.start()].split("\n---\n>",1) ) != 1))
							if( y or ((m == None) and (len( r.split("\n<",1)[1].split("\n---\n>",1) ) != 1))  ):
								l.append(r.split("\n<",1)[1].split("\n---\n>",1)[0].strip())
								l.append(r.split("\n<",1)[1].split("\n---\n>",1)[1].strip())
							else:
								l.append("del")
								l.append(r.split("\n<",1)[1].strip())
						else:
							l.append(r.split("\n>",1)[0])
							l.append("add")
							l.append(r.split("\n>",1)[1].strip())
						break
					elif( not ( r[0].isdigit() ) ):
						continue 			
				else:
					break			
		final.append(l)

	return final




def dynchange( final ):

	tlist = []
	for i in final:
		l = []
		l.append( i[0] )
		j = 1
		while(j < len( i ) ):
			r = []
			for k in range(0,3):
				r.append( i[ j ] )
				j += 1
			l.append( r )
		tlist.append( l )
	
	slist = []
	for i in tlist:
		z = []
		for j in i[ 1: ]:
			f = 0
			if(len( j[2] ) <= 25):
				f = 1
			elif( re.search( r"\.jpg" ,j[2]) != None ):
				f = 1
			elif( re.search( r"script" ,j[2]) != None ):
				f = 1
			elif( re.search( r"type=wav" ,j[2]) != None ):
				f = 1
			elif(re.search( r"\.setConfig\(" ,j[2]) != None):
				f = 1
			elif( re.search( r"\.setSpan\(" ,j[2]) != None ):
				f = 1
			elif( re.search( r"&quot;id_" ,j[2]) != None ):
				f = 1
			elif( re.search( r"widget" ,j[2]) != None ):
				f = 1
			elif( re.search( r"data-objectid=" ,j[2]) != None ):
				f = 1
			elif( re.search( r"data-sessionlink=" ,j[2]) != None ):
				f = 1
			elif( re.search( r"data-id=" ,j[2]) != None ):
				f = 1
			elif( re.search( r"googletag" ,j[2]) != None ):
				f = 1
			elif( re.search( r"_add_placement" ,j[2]) != None ):
				f = 1
			elif( re.search( r"_setKeywords" ,j[2]) != None ):
				f = 1
			elif( re.search( r"xsrft" ,j[2]) != None ):
				f = 1
			elif( re.search( r"style" ,j[2]) != None ):
				f = 1
			elif( re.search( r"addComponentMetadata" ,j[2]) != None ):
				f = 1
			elif( re.search( r"sessionId=" ,j[2]) != None ):
				f = 1
			elif( re.search( r"EventID:" ,j[2]) != None ):
				f = 1
			elif( re.search( r"\.$" ,j[2]) != None ):
				f = 1
			elif( re.search( r"\.\.\." ,j[2]) != None ):
				f = 1
			elif( re.search( r"n   a   v" ,j[2]) != None ):
				f = 1
			elif( re.search( r"   f   o   n   t   " ,j[2]) != None ):
				f = 1
			elif( re.search( r"i   m   a   g   e" ,j[2]) != None ):
				f = 1
		 	elif( re.search( r"c   o   l   o   r" ,j[2]) != None ):
				f = 1
			elif( re.search( r"f   u   n   c   t   i   o   n" ,j[2]) != None ):
				f = 1
			elif( re.search( r"w   i   d   g   e   t" ,j[2]) != None ):
				f = 1
			elif( re.search( r"s   t   y   l   e   =" ,j[2]) != None ):
				f = 1
			elif(re.search(r't   y   p   e   =   "   h   i   d   d   e   n   "',j[2])!=None):
				f = 1
			elif( re.search(r"<!--" ,j[2]) != None ):
				f = 1
			elif( re.search(r"activityId" ,j[2]) != None ):
				f = 1
			elif( re.search(r"/questions/" ,j[2]) != None ):
				f = 1
			elif( re.search(r"/posts/" ,j[2]) != None ):
				f = 1
			elif( re.search( r"#" ,j[2]) != None ):
				f = 1
			elif( re.search( r"data-count=" ,j[2]) != None ):
				f = 1
			elif( re.search( r"ct=" ,j[2]) != None ):
				f = 1
			elif( re.search( r"data-anon=" ,j[2]) != None ):
				f = 1
			elif( re.search( r"initPostLogin" ,j[2]) != None ):
				f = 1
			elif( re.search( r'class="relativetime" title=' ,j[2]) != None ):
				f = 1
			elif( re.search( r'class="comment " id=' ,j[2]) != None ):
				f = 1
			elif( re.search( r'class=" comment-score"' ,j[2]) != None ):
				f = 1
			elif( re.search( r"\.realtime\.subscribeTo" ,j[2]) != None ):
				f = 1
			elif( re.search( r"\.server=" ,j[2]) != None ):
				f = 1
			elif( re.search( r"serverTime" ,j[2]) != None ):
				f = 1
			elif( re.search( r'<a data-sc="' ,j[2]) != None ):
				f = 1
			elif( re.search( r"meta-info" ,j[2]) != None ):
				f = 1
			elif( re.search( r'class="favicon"' ,j[2]) != None ):
				f = 1
			elif( re.search( r"/users/login\?returnurl=" ,j[2]) != None ):
				f = 1
			elif( re.search( r"experimentContextString:" ,j[2]) != None ):
				f = 1
			elif( re.search( r"<tr><td></td><td></td></tr>" ,j[2]) != None ):
				f = 1
			elif((re.search(r'class="label-key',j[2])!=None)and(re.search(r"title=",j[2])!=None)):
				f = 1
			elif((re.search("input",j[2])!=None)and(re.search(r'type="hidden"',j[2])!=None)):
				f = 1
			elif( re.match( r">" ,j[2]) != None ):
				f = 1
			elif( re.match( r"<div" ,j[2]) != None ):
				f = 1
			elif( re.match( r"<td>" ,j[2]) != None ):
				f = 1
			elif( re.match( r"ga" ,j[2]) != None ):
				f = 1
			elif( re.match( r"Currently online:" ,j[2]) != None ):
				f = 1
			elif( re.match( r"new Image\(\)\.src =" ,j[2]) != None ):
				f = 1
			elif( re.match( r"LITHIUM" ,j[2]) != None ):
				f = 1
			elif( re.match( r"<thead id=" ,j[2]) != None ):
				f = 1
			elif( re.match( r";\.v=" ,j[2]) != None ):
				f = 1
			elif( re.match( r"ProfileTweet" ,j[2]) != None ):
				f = 1
			elif(re.match( r"document\.write\('&lt;img src=" ,j[2]) != None):
				f = 1
			elif( re.match( r"document\.bg = new" ,j[2]) != None ):
				f = 1
			elif( re.match( r"window\.optimizely_tm =" ,j[2]) != None ):
				f = 1
			elif(re.match(r"utilityNavController\.account\.set",j[2]) !=None):
				f = 1
			elif(re.match(r'<meta content="',j[2]) !=None):
				f = 1
			elif(re.match(r"PubSub\.publish\(",j[2]) !=None):
				f = 1
			elif(re.match(r"s\.eVar7=",j[2]) !=None):
				f = 1
			elif(re.match(r"HelpCenter\.internal =",j[2]) !=None):
				f = 1
			elif(re.match(r"<video",j[2]) !=None):
				f = 1
			elif( re.match( r"&lt;" ,j[2]) != None ):
				f = 1
			elif( re.match( r"&amp;" ,j[2]) != None ):
				f = 1
			elif( re.match( r"var" ,j[2]) != None ):
				f = 1
			elif( re.match( r"</ul>" ,j[2]) != None ):
				f = 1
			elif( (re.match( r"</li>" ,j[2]) != None) and (j[1] != "add") ):
				f = 1
			elif( re.match( r"</section>" ,j[2]) != None ):
				f = 1
			elif( re.match( r"</footer>" ,j[2]) != None ):
				f = 1
			elif( re.match( r"<blockquote>" ,j[2]) != None ):
				f = 1
			elif( re.match( r"<header" ,j[2]) != None ):
				f = 1
			elif( re.match( r"function" ,j[2]) != None ):
				f = 1
			elif( re.match( r"<img " ,j[2]) != None ):
				f = 1
			elif( re.match( r"<label" ,j[2]) != None ):
				f = 1
			elif( re.match( r"<span class=" ,j[2]) != None ):
				f = 1
			elif( re.match( r"<a " ,j[2]) != None ):
				f = 1
			elif( re.match( r"window\.NREUM" ,j[2]) != None ):
				f = 1
			elif( re.match( r"window\.open" ,j[2]) != None ):
				f = 1
			elif( re.match( r"<span aria" ,j[2]) != None ):
				f = 1
			elif( re.match( r"'/popup\.aspx\?src='" ,j[2]) != None ):
				f = 1
			elif( re.match( r"'BG_P':" ,j[2]) != None ):
				f = 1
			elif( re.match( r"'WATCH_LEGAL_TEXT" ,j[2]) != None ):
				f = 1
			elif( re.match( r"'NAVIGATION_TRACKING" ,j[2]) != None ):
				f = 1
			elif( re.match( r"'TTS_URL':" ,j[2]) != None ):
				f = 1
			elif( re.match( r"'CONVERSION_CONFIG" ,j[2]) != None ):
				f = 1
			elif( re.match( r"'ADS_DATA':" ,j[2]) != None ):
				f = 1
			elif( re.match( r"<li class=" ,j[2]) != None ):
				f = 1
			elif( re.match( r"<ol class=" ,j[2]) != None ):
				f = 1
	 		elif( re.match( r"</li><li> <a" ,j[2]) != None ):
				f = 1
			elif( re.match( r"/   s   c   r   i   p   t" ,j[2]) != None ):
				f = 1
			elif( re.match( r"r   e   p   o   s   i   t" ,j[2]) != None ):
				f = 1
			elif( re.match( r"e   n   c   o   d   e" ,j[2]) != None ):
				f = 1
			elif( re.match( r"l   i   n   k" ,j[2]) != None ):
				f = 1
			elif( re.match(r"!   -   -",j[2]) != None ):
				f = 1
			elif( re.match(r'\{   "',j[2]) != None ):
				f = 1
			elif( re.match( r"\}" ,j[2]) != None ):
				f = 1
			elif( re.match( r"\]" ,j[2]) != None ):
				f = 1
			elif( re.match( r"y   ;" ,j[2]) != None ):
				f = 1
			elif( re.match( r"'XSRF_TOKEN':" ,j[2]) != None ):
				f = 1
			elif( re.match( r"</div>" ,j[2]) != None ):
				f = 1
			elif( re.match( r"data-screen-name=" ,j[2]) != None ):
				f = 1
			elif( re.match( r"background-image: url\(" ,j[2]) != None ):
				f = 1
			elif( re.match( r"background: url\(" ,j[2]) != None ):
				f = 1
			elif( re.match( r"<button" ,j[2]) != None ):
				f = 1
			elif( re.match( r"fb page: &lt;a href=" ,j[2]) != None ):
				f = 1
			elif( re.match( r"</a></span></div></div>" ,j[2]) != None ):
				f = 1
			elif( re.match( r"<code class" ,j[2]) != None ):
				f = 1
	 		elif( re.match( r"loadTimestamp:" ,j[2]) != None ):
				f = 1
			elif( re.match( r"Served from:" ,j[2]) != None ):
				f = 1
			elif( re.match( r"'https:" ,j[2]) != None ):
				f = 1
			elif( re.match( r"<link" ,j[2]) != None ):
				f = 1
			elif( re.match( r"<form" ,j[2]) != None ):
				f = 1
			elif( re.match( r"jQuery" ,j[2]) != None ):
				f = 1
			elif( re.match( r"@font-face" ,j[2]) != None ):
				f = 1
			elif( re.match( r"@import url" ,j[2]) != None ):
				f = 1
			elif( re.match( r"DWREngine" ,j[2]) != None ):
				f = 1
			elif( re.match( r"timeStamp:" ,j[2]) != None ):
				f = 1
			elif( re.match( r"return false;" ,j[2]) != None ):
				f = 1
			elif( re.match( r"preloadData:" ,j[2]) != None ):
				f = 1
			elif( re.match( r"\," ,j[2]) != None ):
				f = 1
			elif( re.match( r"onloadRegister_DEPRECATED" ,j[2]) != None ):
				f = 1
			elif( re.match( r"Analytics\." ,j[2]) != None ):
				f = 1
			elif( re.match( r"revision:" ,j[2]) != None ):
				f = 1
 			elif( re.match( r"return " ,j[2]) != None ):
				f = 1
			elif( re.match( r"formkey:" ,j[2]) != None ):
				f = 1
			elif( re.match( r"bingoId:" ,j[2]) != None ):
				f = 1
			elif( re.match( r"commitSHA:" ,j[2]) != None ):
				f = 1
			elif( re.match( r"EUREKA_VIDEO" ,j[2]) != None ):
				f = 1
			elif( re.match( r"requestLogId:" ,j[2]) != None ):
				f = 1
			elif( re.match( r"_kiq\.push" ,j[2]) != None ):
				f = 1
			elif( re.match( r"'variation' :" ,j[2]) != None ):
				f = 1
			elif( re.match( r'dir="ltr"' ,j[2]) != None ):
				f = 1
			elif( re.match( r"dap" ,j[2]) != None ):
				f = 1
			elif( re.match( r"signInUrl:" ,j[2]) != None ):
				f = 1
			elif( re.match( r"DM_Context" ,j[2]) != None ):
				f = 1
			elif( re.match( r"WpsTracking" ,j[2]) != None ):
				f = 1
			elif( re.match( r"window\.serverStart" ,j[2]) != None ):
				f = 1
			elif( re.match( r"masscast_async_call=" ,j[2]) != None ):
				f = 1
			elif( re.match( r"served from batcache" ,j[2]) != None ):
				f = 1
			elif( re.match( r"<pubdate>" ,j[2]) != None ):
				f = 1
			elif( re.match( r"<media:" ,j[2]) != None ):
				f = 1
			elif( re.match( r"<authordetails>" ,j[2]) != None ):
				f = 1
			elif( re.match( r"<slideshare:" ,j[2]) != None ):
				f = 1
			elif( re.match( r"EUREKA_" ,j[2]) != None ):
				f = 1
			elif( re.match( r"_stq\.push\(" ,j[2]) != None ):
				f = 1
			elif( re.match( r"user:" ,j[2]) != None ):
				f = 1
			elif( re.match( r"'state': " ,j[2]) != None ):
				f = 1
			elif( re.match( r'"html" : "&lt;div' ,j[2]) != None ):
				f = 1
			elif( re.match( r'<html itemscope=""' ,j[2]) != None ):
				f = 1
			elif( re.match( r"'YPC_SIGNIN_URL':" ,j[2]) != None ):
				f = 1
			elif( re.match( r"'YPC_SWITCH_URL':" ,j[2]) != None ):
				f = 1
			elif( re.match( r"'YPC_OFFER_OVERLAY':" ,j[2]) != None ):
				f = 1
			elif( re.match( r"'RELATED_PLAYER_ARGS':" ,j[2]) != None ):
				f = 1
			elif( re.match( r'<input class="uvField' ,j[2]) != None ):
				f = 1
			elif((re.match(r"<script src=",j[2])!=None)and(re.search(r"/\?_=",j[2])!=None)):
				f = 1
			elif((re.match(r"{ txt: ",j[2])!=None)and(re.search(r"  var ",j[2])!=None)):
				f = 1
			elif((re.match(r"<",j[2])!=None)and(j[1]=="del")):
				f = 1
			'''elif((re.match(r"<!--" ,j[2]) != None)and(re.search("-->",j[2])!=None)):
				f = 1
			elif( re.match( r"</style><link href=" ,j[2]) != None ):
				f = 1  '''			

			if(f == 0):
				if( i[0] not in z ): 
					z.append( i[0] )
				z.append( j[0] )
				z.append( j[1] )
				z.append( j[2] )
	
		if( (len( z ) != 0) ):
			slist.append( z )	
	
	return slist




#print("Round 1:")

'''  
	WORKS FOR:
webnm = "http://news.bbc.co.uk/2/hi/health/2284783.stm" 
webnm = "http://www.google.com" 
webnm = "http://www.facebook.com"
webnm = "https://www.hackerrank.com"
webnm = "http://www.youtube.com"
webnm = "http://www.pingdom.com"
webnm = "http://www.w3schools.com"
webnm = "http://www.pes.edu"
webnm = "http://www.twitter.com" 
webnm = "http://www.linkedin.com"
webnm = "http://www.blogspot.com" 
webnm = "http://www.bing.com"
webnm = "http://www.wordpress.com"
webnm = "http://www.instagram.com"
webnm = "http://www.msn.com" 
webnm = "http://www.apple.com"  
webnm = "http://www.cnn.com"      
webnm = "http://www.goodreads.com"
webnm = "http://www.mint.com" 
webnm = "http://www.khanacademy.com"
webnm = "http://www.slideshare.net" 
webnm = "http://www.skype.com"
webnm = "http://www.spotify.com"
webnm = "http://www.weather.com" 
webnm = "http://www.onion.com" 

	PROBLEMS:
www.myntra.com - has >300 links in main page only
www.nytimes.com - has >135 links in main page only
www.ndtv.com - has >120 links in main page only
www.espn.com - has >76 links in main page only 
www.techcrunch.com - has >76 links in main page only 
en.wikipedia.org/wiki/Star - core dumped
www.bbc.com - runtimeerror recursion exceeded
www.allmusic.com - runtimeerror recursion exceeded
www.github.com - gets stuck after 5_a.txt
www.yahoo.com - gets stuck after 0_a.txt

www.amazon.com - crazy dynamic content
www.stackoverflow.com - also
www.dailymotion.com - also
'''

webnm = "http://news.bbc.co.uk/2/hi/health/2284783.stm"         
page1 = urllib2.urlopen( webnm )
soup1 = BeautifulSoup(page1)
i=0
f=open(str(i)+"_a.txt", "w")
f.write( str(soup1) )                
f.close()
i+=1
t=[]

for link in soup1.find_all('a'):
    l=link.get('href')
    l=str(l)
    if(re.match("^#",l)):
            continue    
    if(re.match("^http",l)!=None):
            if(l in t):
                    continue
            try:    
                    x = urllib2.urlopen(l)
                    y=BeautifulSoup(x)
		    t.append(l)
                    y=str(y)
                    fd1=open(str(i)+"_a.txt","w")
                    fd1.write(y)         
                    i+=1
                    fd1.close()
            except HTTPError as e:
                    print("-----------------------------HTTP ERROR---------------------------")
            except UnicodeEncodeError as u:
                    print("---------------------------Unicode ERROR--------------------------")
	    except URLError as uu:
		    print("-----------------------------URL ERROR----------------------------")

#print("Round 2:")
page2 = urllib2.urlopen( webnm )
soup2 = BeautifulSoup(page2)
k=0
map_names = {}
f=open(str(k)+"_b.txt", "w")
f.write( str(soup2) )                
f.close()
map_names[str(k)+"_b.txt"] = webnm
k+=1
s=[]


for link in soup2.find_all('a'):
    l=link.get('href')
    l=str(l)
    if(re.match("^#",l)):
            continue    
    if(re.match("^http",l)!=None):
            if(l in s):
                    continue
            try:    
                    x = urllib2.urlopen(l)
                    y=BeautifulSoup(x)
		    s.append(l)
                    y=str(y)
                    fd2=open(str(k)+"_b.txt","w")
                    fd2.write(y)         
                    fd2.close()
		    map_names[str(k) + "_b.txt"] = l
		    k+=1
            except HTTPError as e:
                    print("-----------------------------HTTP ERROR---------------------------")
            except UnicodeEncodeError as u:
                    print("---------------------------Unicode ERROR--------------------------")
	    except URLError as uu:
		    print("-----------------------------URL ERROR----------------------------")

#print(map_names)
print("Total no of anchors: " + str(k))

f1 = open("result.txt", 'w+')
for i in range(0,k):
	cmd = "diff "+str(i)+"_a.txt "+str(i)+"_b.txt"
	print( (str(i) + "_b.txt") , file=f1 )
	handle = os.popen(cmd)
	print( handle.read() , file=f1 )
	handle.close()	
f1.close()


final = make_list( "result.txt" )
slist = dynchange( final )
changed_websites = []


f2 = open("dynamic.txt", 'w+')
for i in final:
	for j in i:
		print( j , file=f2 ) 
		print("----------------------------------------------------------------\n", file=f2 ) 
	print("************************************************************************\n", file=f2 ) 
f2.close()

f3 = open("static.txt", 'w+')
for i in slist:
	changed_websites.append( map_names.get( i[0] ) ) 
	for j in i:
		print( j , file=f3 ) 
		print("--------------------------------------------------------\n", file=f3 ) 
	print("****************************************************************\n", file=f3 )
f3.close()


print("\nList of Changed Websites are:\n")
for i in changed_websites:
	print(i + "\n")
print("\n")


