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
#############################################################################################################
df= pd.read_csv("data/potential_crimes.csv",sep=";",encoding="utf-8")
#############################################################################################################
if 'story' not in df.columns:
    df['story']=''
############################
def append_story_todf():
    for i , url in enumerate(df.link):
        print i, url
        try:
            req = urllib2.Request(url.decode('utf-8'), headers={'User-Agent' : "Magic Browser"})
            page = urllib2.urlopen( req )
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
            soup = BeautifulSoup(mypage)
            #find all paragraphs from the current "page"
            all_para=[]
            components= soup.find_all('span') + soup.find_all('time') + soup.find_all('p') 
            components += soup.find_all('h1')+ soup.find_all('h2')
            for para in components:
                all_para.append(para.text)
                #join in one paragraph
                df.loc[i,'story']= ' '.join(all_para).strip() 
append_story_todf()
#save data because It is lengthy task
df.to_csv("data/potential_crimes_stories.csv",sep=";",encoding="utf-8")