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
site_web=pd.read_csv("data/site_web.csv",sep=",",encoding="utf-8")
site_web= list(site_web.link)
#####################################################
if os.path.isfile("data/all_page.csv"):
    all_page=pd.read_csv("data/all_page.csv",sep=";",encoding="utf-8")
    all_page= list(all_page.link)
else:
    all_page=[]
if os.path.isfile("data/base_links.csv"):
    all_page1=pd.read_csv("data/base_links.csv",sep=";",encoding="utf-8")
    all_page1= list(all_page1.link)
else:
    all_page1 = []
#####################################################
for i,s in enumerate(site_web):
    print i,s
    try:
        req = urllib2.Request(s.decode('utf-8'), headers={'User-Agent' : "Magic Browser"})
        page = urllib2.urlopen( req )
        soup = BeautifulSoup(page)
    except urllib2.HTTPError,e:
        continue
    except urllib2.URLError, e:
        continue
    except httplib.HTTPException, e:
        continue
    except Exception:
        continue
    #find all links
    all_links= soup.find_all("a")
    #ensure all links are valid
    link_inside= [link.get("href") for link in all_links if link.get("href") is not None]
    link_inside= [link if link.startswith('http') or link.startswith('www') else s + link for link in link_inside]
    #do not keep links from starter links
    link_inside = [link for link in link_inside if link not in site_web]
    #do not keep links that have been already recorded from the current loop
    link_inside = [link for link in link_inside if link not in all_page]
    if all_page1!=[]:
        link_inside = [link for link in link_inside if link not in all_page1]
    for k in np.unique(link_inside):
        print k
        all_page.append(k)
############## save data #######################
all_page=np.unique(all_page)
len(all_page)
df = pd.DataFrame(data=all_page, index= range(len(all_page)), columns=['link'])
df.to_csv("data/all_page.csv",sep=";",encoding="utf-8")
print df.shape
