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
import os.path
import sys  
reload(sys)  
sys.setdefaultencoding('latin-1')
### laod data (keywords also)
all_page=pd.read_csv("data/all_page.csv",sep=";",encoding="utf-8")
all_page= list(all_page.link)
all_page1=pd.read_csv("data/base_links.csv",sep=";",encoding="utf-8")
all_page1= list(all_page1.link)
keys=pd.read_csv("data/keywords.csv",sep=",")
mykeywords="|".join(list(keys.kwd))
###
#2nd iter
X1= [x for x in all_page1 if re.search(mykeywords,x) is not None]
#1st iter
X2= [x for x in all_page if re.search(mykeywords,x) is not None]
X=X1 + X2
X=np.unique(X)
len(X)
df = pd.DataFrame(data=X, index= range(len(X)), columns=['link'])
df.to_csv("data/potential_crimes.csv",sep=";",encoding="utf-8")
df.shape