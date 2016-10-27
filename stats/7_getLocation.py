from datetime import date
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
potential_crimes= pd.read_csv("data/potential_crimes_stories.csv",sep=";",encoding="utf-8")
##
years = range(2003,2017)
months= ["01","02","03","04","05","06","07","08","09","10","11","12"]
days= range(1,31)
date_combinations = product(years,months,days)
conversion_mois={"January":'Janvier',"February":"Fevrier","March":"mars","April":"avril",
                "May":"mai","June":"juin","July":"juillet","August":"aout","September":"septembre",
                "October":"octobre","November":"novembre","December":"decembre"}
##
#initialization:
def search_date_in (form="year/month",var='link'):
    if 'date' not in potential_crimes.columns:
        potential_crimes['date']=''
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
        i = [i for i,j in enumerate(potential_crimes[var]) if mymonth in j and potential_crimes.loc[i,var]!=[] ]
        if len(i)==1:
            print mymonth,i ,  potential_crimes.loc[i, var]
            potential_crimes.loc[i, 'date']=mymonth
        else:
            for i1 in i:
                print mymonth, i1 ,  potential_crimes.loc[i1,var]
                potential_crimes.loc[i1, 'date']=mymonth
                
##run all functions that search for dates
search_date_in(form="year/month",var='link')
search_date_in(form="year-month",var='link')
search_date_in(form="year/month",var='story')
search_date_in(form="year-month",var='story')
search_date_in(form="text",var='link')
search_date_in(form="text",var='story')
potential_crimes.to_csv("data/potential_crimes_stories.csv",sep=";",encoding="utf-8")