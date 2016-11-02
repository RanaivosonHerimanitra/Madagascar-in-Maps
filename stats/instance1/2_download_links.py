import httplib
import urllib2
import psycopg2
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
#############################################################################################################
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
#####################################################
def read_links ():
    cursor.execute(""" select link from "all_page" """)
    all_page = [row[0] for row in cursor]
    cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
    mynames=cursor.fetchall()
    if ("base_links",) in mynames:
        cursor.execute(""" select link from "base_links" """)
        all_page1= [row[0] for row in cursor ]
    else:
        cursor.execute("""CREATE TABLE base_links (link TEXT)""")
        conn.commit()
        all_page1=[]
    return all_page, all_page1
all_page,all_page1 = read_links()
##################################################
def download_data(all_page=all_page, all_page1=all_page1):
    #randomy shuffle page
    all_page= random.sample(all_page,len(all_page))
    for i,s in enumerate(all_page):
        print i, s
        try:
            if "https" not in s and "pdf" not in s and "jpg" not in s and "javascript" not in s:
                req = urllib2.Request(s.decode('utf-8'), headers={'User-Agent' : "Magic Browser"})
                page = urllib2.urlopen( req,None,4. )
            else:
                return

        except urllib2.HTTPError,e:
                continue
        except urllib2.URLError, e:
                continue
        except httplib.HTTPException, e:
                continue
        except Exception:
                continue
        #handle page that does not actually exist
        mypage=page.read()
        if len(mypage)==0:
            print "the above page does not exist"
            continue
        else:
            soup = BeautifulSoup(mypage, "html.parser")
            #find all links from the current "page"
            all_links= soup.find_all("a")
            #ensure all links are not empty
            link_inside= [link.get("href") for link in all_links if link.get("href") is not None]
            link_inside= [x for x in link_inside if 'www.' in x or 'http://' in x]
            #ensure they are not pdf or image:
            link_inside= [x for x in link_inside if x.endswith(('jpg', 'pdf'))==False]
            #ensure they are not mail:
            link_inside= [x for x in link_inside if x.startswith(('mail'))==False]
            #do not scrape https link:
            link_inside= [x for x in link_inside if 'https://' not in x]
            #invalid links
            link_inside= [x for x in link_inside if '=http' not in x and '/http' not in x and '/https' not in x]
            #do not select social media:
            link_inside= [x for x in link_inside if 'google' not in x and 'facebook' not in x and 'twitter' not in x and 'linkedin' not in x  ]
            #do not append links from starter links
            link_inside = [link for link in link_inside if link not in site_web]
            #do not append links from previous records
            link_inside = [link for link in link_inside if link not in all_page]
            if all_page != all_page1:
                #do not append links in the current records
                link_inside = [link for link in link_inside if link not in all_page1]
            for k in np.unique(link_inside):
                cursor.execute(""" select * from "base_links" """)
                print k.encode('iso-8859-1'), cursor.rowcount
                k=k.encode('iso-8859-1')
                cursor.execute("INSERT INTO base_links(link) VALUES (%s)",[k] )
                conn.commit()

### this function should run undefinitely#######################################
while True:
    download_data(all_page=all_page, all_page1=all_page1)
    download_data(all_page=all_page1, all_page1=all_page1)
