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
#initialization:
def search_date_in (form="year/month",var='link'):
    print "querying db..."
    cursor.execute(""" select * from "potential_pages" """)
    print "ok"
    print " get variables..."
    potential_pages= [row for row in cursor]
    potential_pages_link= [ x[0] for x in potential_pages ]
    potential_pages_story=[ x[1] for x in potential_pages ]
    print "ok"
    print "shuffle it to have randomness..."
    potential_pages_link= random.sample(potential_pages_link,len(potential_pages_link))
    potential_pages_story= random.sample(potential_pages_story,len(potential_pages_story))
    print "ok"
    print "get column names from potential_pages..."
    cursor.execute("Select * FROM potential_pages LIMIT 0")
    colnames = [desc[0] for desc in cursor.description]
    print "ok"
    ##
    years = range(2003,2017)
    months= ["01","02","03","04","05","06","07","08","09","10","11","12"]
    days= range(1,31)
    date_combinations = product(years,months,days)
    conversion_mois={"January":'Janvier',"February":"Fevrier","March":"mars","April":"avril",
                    "May":"mai","June":"juin","July":"juillet","August":"aout","September":"septembre",
                    "October":"octobre","November":"novembre","December":"decembre"}
    ##

    if 'dates' not in colnames:
        #ALTER here (add a column in the table):
        query = "alter table potential_pages add column %s text"
        cols = ('dates')
        cursor.execute(query, (AsIs(cols),))
        conn.commit()
    for x in date_combinations:
        y,m,d = x
        if form=="year/month":
            mymonth = str(y) + "/" + m
        if form=="year-month":
            mymonth = str(y) + "-" + m
        if form=="text":
            mymonth= date(y, int(m), d)
            mymonth=mymonth.strftime("%d %B %Y")
            d0= d.split()[1]
            mymonth=mymonth.replace(d0,conversion_mois[d0])
        #retrieve index
        if var=='link':
            tmp=potential_pages_link
        if var=='story':
            #tmp=potential_pages_story
            tmp=[z.decode("utf8") if z is not None else [] for z in potential_pages_story ]
        i = [i for i,j in enumerate(tmp) if mymonth in j and tmp[i]!=[] ]
        if isinstance(i,int):
            print mymonth, i ,  tmp[i]
            cursor.execute(""" UPDATE potential_pages SET dates=%s WHERE link = %s""",
            ( (mymonth,),(tmp[i],) ) )
            conn.commit()
        else:
            if isinstance(i,list) and len(i)==1:
                p=int(''.join( str(e) for e in i ))
                print mymonth, p ,  tmp[p]
                cursor.execute(""" UPDATE potential_pages SET dates=%s WHERE link = %s""",
                ( (mymonth,),(tmp[p],) ) )
                conn.commit()
            if len(i)>1:
               for i1 in i:
                   print mymonth, i1 ,  tmp[i1]
                   cursor.execute(""" UPDATE potential_pages SET dates=%s WHERE link = %s""",
                   ( (mymonth,),(tmp[i1],) ) )
                   conn.commit()
#######################run functions#######################
search_date_in(form="year/month",var='link')
search_date_in(form="year-month",var='link')
search_date_in(form="year/month",var='story')
search_date_in(form="year-month",var='story')
search_date_in(form="text",var='link')
search_date_in(form="text",var='story')
