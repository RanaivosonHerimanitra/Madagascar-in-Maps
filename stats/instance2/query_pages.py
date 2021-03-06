######################libraries I need #######################################################################
from itertools import *
import psycopg2
import httplib
import urllib2
import random
import re
import requests
from httplib import IncompleteRead
import json
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os.path
import sys
reload(sys)
sys.setdefaultencoding('latin-1')
####################################load data################################################################
#establish connection:
conn = psycopg2.connect(database='...',
                        user='...',
                        password='...',
                        host='...',
                        port='5432', sslmode='require')
# get a cursor object used to execute SQL commands
cursor = conn.cursor()
cursor.execute(""" select link from "website" """)
site_web=[row[0] for row in cursor ]
cursor.execute(""" select link from "all_page" """)
all_page=[row[0] for row in cursor ]

tobecorrected= [x for x in all_page if "comspip" in x]
if len(tobecorrected)>0:
    for k in tobecorrected:
        k_rep=k.replace("comspip","com/spip")
        cursor.execute("UPDATE all_page SET link=(%s) WHERE link = (%s)", (k_rep,k,))
        conn.commit()
cursor.execute(""" select link from "base_links" """)
all_page1=[row[0] for row in cursor ]
############################Customized queries for the following websites####################################
### http://www.midi-madagasikara.mg/year/month/day
### http://www.madagascar-tribune.com/spip.php?page=archives&archives=year-month-day
### http://www.newsmada.com/year/month/day
### http://www.policenationale.gov.mg/?m=201609 (yearmonth)
### http://www.population.gov.mg/?m=201204 (yearmonth)
### http://www.sobikamada.com/jmj/itemlist/date/2015/09/5.html (year month day)
pages= ["http://www.midi-madagasikara.mg/","http://www.madagascar-tribune.com/spip.php?page=archives&archives="]
pages += ["http://www.newsmada.com/","http://www.policenationale.gov.mg/?m=","http://www.population.gov.mg/?m="]
pages += ["http://www.sobikamada.com/jmj/itemlist/date/","http://www.gendarmerie.gov.mg/blog/"]
######################## prepare query parameters (mainly dates #######################
years = range(2013,2016)
months= ["01","02","03","04","05","06","07","08","09","10","11","12"]
days= range(1,31)
date_combinations = product(years,months,days)
###################### Function to query these pages ##################################
def query_pages(url=None,all_page1=all_page1,all_page=all_page,site_web=site_web,append_origin=False,url_origin=None):
    try:
        if "pdf" not in url and "jpg" not in url and "javascript" not in url:
            req = urllib2.Request(url.decode('utf-8'), headers={'User-Agent' : "Magic Browser"})
            page = urllib2.urlopen( req,None,7. )
        else:
            return
    except urllib2.HTTPError,e:
        print e
        return
    except urllib2.URLError, e:
        print e
        return
    except httplib.HTTPException, e:
        print e
        return
    except Exception,e:
        print e
        return
    #handle page that does not actually exist
    mypage=page.read()
    if len(mypage)==0:
        print "the above page does not exist"
    else:
        soup = BeautifulSoup(mypage, "html.parser")
        #find all links from the current "page"
        all_links= soup.find_all("a")
        #ensure all links are valid
        link_inside= [link.get("href") for link in all_links if link.get("href") is not None]
        if append_origin==True and url_origin is not None:
            link_inside= [ url_origin + x for x in link_inside if 'www.' not in x or 'http://' not in x ]
        link_inside= [x for x in link_inside if 'www.' in x or 'http://' in x]
        #do not append links from starter links
        link_inside = [link for link in link_inside if link not in site_web]
        #do not append links from previous records
        link_inside = [link for link in link_inside if link not in all_page]
        #do not append links in the current records
        link_inside = [link for link in link_inside if link not in all_page1]
        for k in np.unique(link_inside):
            cursor.execute(""" select * from "base_links" """)
            print k.encode('iso-8859-1'), cursor.rowcount
            k=k.encode('iso-8859-1')
            cursor.execute("INSERT INTO base_links(link) VALUES (%s)",[k] )
            conn.commit()
############################### queries #############################################################################
for i,p in enumerate(pages):
    if i in [0,2]:
        for date in date_combinations:
            year,month,day= date
            url= p+str(year)+"/"+month+"/"+str(day)
            print url
            query_pages(url=url,all_page1=all_page1,all_page=all_page,site_web=site_web)
        date_combinations = product(years,months,days)
    elif i==1:
        for date in date_combinations:
            year,month,day= date
            url= p+str(year)+"-"+month+"-"+str(day)
            print url
            query_pages(url=url,all_page1=all_page1,all_page=all_page,site_web=site_web,
                        append_origin=True,url_origin="http://www.madagascar-tribune.com/")
        date_combinations = product(years,months,days)
    elif i in [3,4]:
        for date in date_combinations:
            year,month,_= date
            url= p+str(year)+month
            print url
            query_pages(url,all_page1=all_page1,all_page=all_page,site_web=site_web)
        date_combinations = product(years,months,days)
    elif i ==5:
        for date in date_combinations:
            year,month,day= date
            url= p+str(year)+"-"+month+"-"+str(day)+".html"
            print url
            query_pages(url=url,all_page1=all_page1,all_page=all_page,site_web=site_web,
                        append_origin=True,url_origin="www.sobikamada.com/")
        date_combinations = product(years,months,days)
    elif i ==6:
        for date in date_combinations:
            year,month,_= date
            url= p+str(year)+"/"+month
            print url
            query_pages(url=url,all_page1=all_page1,all_page=all_page,site_web=site_web)

## Special treatment for Midi and tribune because they have archives available
tribune="http://www.madagascar-tribune.com/spip.php?page=archives&debut_articles_recents="
k=10
while k<18650:
    url = tribune + str(k) + "#pagination_articles_recents"
    print k, url
    query_pages(url=url,all_page1=all_page1,all_page=all_page,site_web=site_web,append_origin=True,
                url_origin="http://www.madagascar-tribune.com/")
    k += 10
##
midi= "http://www.midi-madagasikara.mg/2013/"
query_pages(url=midi,all_page1=all_page1,all_page=all_page,site_web=site_web)
midi="http://www.midi-madagasikara.mg/2013/page/"
k=2
while k<127:
    url = midi + str(k)
    query_pages(url=url,all_page1=all_page1,all_page=all_page,site_web=site_web)
    k += 1
