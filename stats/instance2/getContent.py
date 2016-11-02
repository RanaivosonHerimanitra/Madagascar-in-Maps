import httplib
import psycopg2
from psycopg2.extensions import AsIs
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
#############################################################################################################
#establish connection:
conn = psycopg2.connect(database='...',
                        user='...',
                        password='...',
                        host='...',
                        port='5432', sslmode='require')
# get a cursor object used to execute SQL commands
cursor = conn.cursor()
############################
def append_story_todf():
    cursor.execute(""" select * from "potential_pages" """)
    presence=[row for row in cursor ]
    potential_pages=[row[0] for row in presence ]
    #introduce random :
    potential_pages=random.sample(potential_pages,len(potential_pages))
    #####################################add story if doesnt exist yet##############
    # what are columns in potential pages:
    cursor.execute("Select * FROM potential_pages LIMIT 0")
    colnames = [desc[0] for desc in cursor.description]
    #
    if "story" not in colnames:
        query = "alter table potential_pages add column %s text"
        cols = ('story')
        cursor.execute(query, (AsIs(cols),))
        conn.commit()
    for j , url in enumerate(potential_pages):
        print j, url
        #test if url already exists and has a story in potential_pages database:
        if presence[j][1] is not None:
            continue
        try:
            req = urllib2.Request(url.decode('utf-8'), headers={'User-Agent' : "Magic Browser"})
            page = urllib2.urlopen( req,None,7.) # 7s waiting before skipping to another url
        except urllib2.HTTPError,e:
            continue
        except urllib2.URLError, e:
            continue
        except httplib.HTTPException, e:
            continue
        except Exception:
            continue
        mypage=page.read()
        if len(mypage)==0:
            print "the above page does not exist"
            continue
        else:

            soup = BeautifulSoup(mypage, "html.parser")
            #find all paragraphs from the current "page"
            all_para=[]
            components= soup.find_all('span') + soup.find_all('time') + soup.find_all('p')
            components += soup.find_all('h1')+ soup.find_all('h2')
            for i,para in enumerate(components):
                all_para.append(para.text)
            #once appended , merge in on big string and insert(i.e UPDATE) into the database
            print str(i)+'components appended to '+url
            k=' '.join(all_para).strip()
            k=k.replace("'"," ")
            cursor.execute(""" UPDATE potential_pages SET story=%s WHERE link = %s""", (k,url) )
            conn.commit()
#################### run the function forever#############################
if __name__ == '__main__':
    append_story_todf()
