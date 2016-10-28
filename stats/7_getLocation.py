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
code_ocha= pd.read_csv("data/code_OCHA.csv",sep=",",encoding="utf-8")
##
potential_crimes= potential_crimes.dropna()
potential_crimes.index = range(potential_crimes.shape[0])
##
#initialization:
def search_location_in (invar='story',newvar='location',fromvar='FOKONTANY'):
    if newvar not in potential_crimes.columns:
        potential_crimes[newvar]=''
    for x in code_ocha[fromvar]:
        #retrieve index
        i = [i for i,j in enumerate(potential_crimes[invar]) if x in j and potential_crimes.loc[i,newvar]!=[] ]
        if len(i)==1:
            print (x,i ,  potential_crimes.loc[i, invar])
            potential_crimes.loc[i, newvar]=x
        else:
            for i1 in i:
                print (x, i1 ,  potential_crimes.loc[i1,invar])
                potential_crimes.loc[i1,newvar]=x
###
search_location_in(invar='story',newvar='location_fkt_story',fromvar='FOKONTANY')
search_location_in(invar='story',newvar='location_fkt_story',fromvar='FOKONTANY')
search_location_in(invar='story',newvar='location_reg_story',fromvar='REGION')
search_location_in(invar='story',newvar='location_reg_story',fromvar='REGION')
search_location_in(invar='story',newvar='location_com_story',fromvar='COMMUNE')
search_location_in(invar='story',newvar='location_com_story',fromvar='COMMUNE')
###
search_location_in(invar='link',newvar='location_fkt_link',fromvar='FOKONTANY')
search_location_in(invar='link',newvar='location_fkt_link',fromvar='FOKONTANY')
search_location_in(invar='link',newvar='location_reg_link',fromvar='REGION')
search_location_in(invar='link',newvar='location_reg_link',fromvar='REGION')
search_location_in(invar='link',newvar='location_com_link',fromvar='COMMUNE')
search_location_in(invar='link',newvar='location_com_link',fromvar='COMMUNE')
### save
potential_crimes.to_csv("data/potential_crimes_stories.csv",sep=";",encoding="utf-8")