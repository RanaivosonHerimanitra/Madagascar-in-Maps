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
#############################################################################################################
# Fetch arguments from command line.
if __name__ == '__main__':
    link0 = sys.argv[1]
    link1 = sys.argv[2]
    if len(link0) ==0:
        usage = '''
        Point to the paths of the link list origin
        '''
        print(usage)
        sys.exit(1)
#####################################################
def read_links (link0=None,link1=None):
    if link0 is None:
        print "error, you must provide origin link"
        return
    else:
        all_page=pd.read_csv(link0,sep=";")
        all_page=list(all_page.link)
        if os.path.isfile(link1):
            all_page1=pd.read_csv(link1,sep=";")
            all_page1=list(all_page1.link)
        else:
            all_page1=[]
            link1= "data/base_links.csv"
    return all_page, all_page1,link1
all_page,all_page1,link1 = read_links(link0,link1)
##################################################
def download_data(all_page=all_page, all_page1=all_page1,link1=link1):
    #randomy shuffle page
    all_page= random.sample(all_page,len(all_page))
    for i,s in enumerate(all_page):
        print i, s
        try:
            if "pdf" not in s and "jpg" not in s and "javascript" not in s:
                req = urllib2.Request(s.decode('utf-8'), headers={'User-Agent' : "Magic Browser"})
                page = urllib2.urlopen( req )
            else:
                continue
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
            soup = BeautifulSoup(mypage)
            #find all links from the current "page"
            all_links= soup.find_all("a")
            #ensure all links are valid
            link_inside= [link.get("href") for link in all_links if link.get("href") is not None]
            link_inside= [x for x in link_inside if 'www.' in x or 'http://' in x]
            #do not append links from starter links
            link_inside = [link for link in link_inside if link not in site_web]
            #do not append links from previous records
            link_inside = [link for link in link_inside if link not in all_page]
            #do not append links in the current records
            link_inside = [link for link in link_inside if link not in all_page1]
            for k in np.unique(link_inside):
                print k, len(all_page1)
                all_page1.append(k)
        #save on the fly (at each loop)
        df = pd.DataFrame(data=all_page1, index= range(len(all_page1)), columns=['link'])
        df.to_csv(link1,sep=";",encoding="utf-8")
### run function #################################################    
if os.path.isfile(link1):
    download_data(all_page=all_page1, all_page1=all_page1,link1=link1)
else:
    download_data(all_page=all_page, all_page1=all_page1,link1=link1)

