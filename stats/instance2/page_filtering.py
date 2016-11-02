from itertools import *
import psycopg2
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

### load data (keywords also) ########################################
#establish connection:
conn = psycopg2.connect(database='...',
                        user='...',
                        password='...',
                        host='...',
                        port='5432', sslmode='require')
# get a cursor object used to execute SQL commands
cursor = conn.cursor()
cursor.execute(""" select link from "all_page" """)
all_page=[row[0] for row in cursor ]
cursor.execute(""" select link from "base_links" """)
all_page1=[row[0] for row in cursor ]
cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
mynames=cursor.fetchall()
if ("keywords",) in mynames:
    cursor.execute(""" select kwd from "keywords" """)
    keys= [row[0] for row in cursor ]
    mykeywords="|".join(list(keys))
else:
    cursor.execute("""CREATE TABLE keywords (kwd TEXT)""")
    conn.commit()
    keys=pd.read_csv("data/keywords.csv",sep=",")
    keys=keys.kwd
    #insert in one go:
    args_str = ','.join(['%s'] * len(keys))
    myquery = 'INSERT INTO keywords VALUES {0}'.format(args_str)
    cursor.execute(myquery, [(k,) for k in keys] )
    conn.commit()
    mykeywords="|".join(list(keys))

######################################################################
def search_for_page():
    #ensure links contain keywords we specified
    X1= [x for x in all_page1 if re.search(mykeywords,x) is not None]
    X2= [x for x in all_page if re.search(mykeywords,x) is not None]
    X=X1 + X2
    X=list(np.unique(X))
    cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
    mynames=cursor.fetchall()
    if ("potential_pages",) not in mynames:
        cursor.execute("""CREATE TABLE potential_pages (link TEXT)""")
        conn.commit()
    else:
        cursor.execute("""select link from "potential_pages" """)
        potential_pages= [row[0] for row in cursor]
        X = [x for x in X if x not in potential_pages ]
    #insert if there is something to insert:
    if X!=[]:
        #insert in one go:
        args_str = ','.join(['%s'] * len(X))
        myquery = 'INSERT INTO potential_pages VALUES {0}'.format(args_str)
        cursor.execute(myquery, [(k,) for k in X] )
        conn.commit()
    #print information for the end user
    print "pages inserted in database:"+str(len(X))
    cursor.execute("""select link from "potential_pages" """)
    print "num of obs. in potential_pages database:"+ str(cursor.rowcount)
################## run the function#################################
if __name__ == '__main__':
    search_for_page()
