#!/usr/bin/env python
import subprocess
from datetime import date
import psycopg2
from psycopg2.extensions import AsIs
import time
import locale
from itertools import *
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
import sys
##
#establish connection:
conn = psycopg2.connect(database='...',
                        user='...',
                        password='...',
                        host='...',
                        port='5432', sslmode='require')
# get a cursor object used to execute SQL commands
cursor = conn.cursor()

#potential_crimes= pd.read_csv("data/potential_crimes_stories.csv",sep=";",encoding="utf-8")
code_ocha= pd.read_csv("data/code_OCHA.csv",sep=",",encoding="utf-8")

def search_location_in (invar='story',newvar='location',fromvar='FOKONTANY'):
    cursor.execute(""" select * from "potential_pages" """)
    potential_pages= [row for row in cursor]
    potential_pages_link= [ x[0] for x in potential_pages ]
    potential_pages_story=[ x[1] for x in potential_pages ]
    #shuffle to give randomness
    potential_pages_link=random.sample(potential_pages_link,len(potential_pages_link))
    potential_pages_story=random.sample(potential_pages_story,len(potential_pages_story))
    #
    colnames = [desc[0] for desc in cursor.description]
    if newvar not in colnames:
        #ALTER here (add a column in the table):
        query = "alter table potential_pages add column %s text"
        cols = (newvar)
        cursor.execute(query, (AsIs(cols),))
        conn.commit()
    for x in code_ocha[fromvar]:
        #retrieve index
        cursor.execute(""" select %s from "potential_pages" """,newvar)
        tmp=[row[0] for row in cursor]
        if newvar.endswith('story'):
            tmp0=potential_pages_story
        if newvar.endswith('link'):
            tmp0=potential_pages_link
        #
        i = [i for i,j in enumerate(tmp0) if x in j and tmp[i]!=[] ]
        if len(i)==1:
            print x,i ,  tmp[i]
            cursor.execute(""" UPDATE potential_pages SET %s=%s WHERE link = %s""", (newvar,x,tmp[i]) )
            conn.commit()
        else:
            for i1 in i:
                print x, i1 ,  tmp[i1]
                cursor.execute(""" UPDATE potential_pages SET %s=%s WHERE link = %s""", (newvar,x,tmp[i1]) )
                conn.commit()

### run functions with different combin of params:
search_location_in(invar='story',newvar='location_fkt_story',fromvar='FOKONTANY')
search_location_in(invar='story',newvar='location_fkt_story',fromvar='FOKONTANY')
search_location_in(invar='story',newvar='location_reg_story',fromvar='REGION')
search_location_in(invar='story',newvar='location_reg_story',fromvar='REGION')
search_location_in(invar='story',newvar='location_com_story',fromvar='COMMUNE')
search_location_in(invar='story',newvar='location_com_story',fromvar='COMMUNE')
search_location_in(invar='link',newvar='location_fkt_link',fromvar='FOKONTANY')
search_location_in(invar='link',newvar='location_fkt_link',fromvar='FOKONTANY')
search_location_in(invar='link',newvar='location_reg_link',fromvar='REGION')
search_location_in(invar='link',newvar='location_reg_link',fromvar='REGION')
search_location_in(invar='link',newvar='location_com_link',fromvar='COMMUNE')
search_location_in(invar='link',newvar='location_com_link',fromvar='COMMUNE')
