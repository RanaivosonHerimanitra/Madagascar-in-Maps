import psycopg2
import pandas as pd
#establish connection:
conn = psycopg2.connect(database='...',
                        user='...',
                        password='...',
                        host='...',
                        port='5432', sslmode='require')
# get a cursor object used to execute SQL commands
cursor = conn.cursor()
###################################### create table if It doesn't exist yet:#########################################################
##
cursor.execute("""CREATE TABLE website (link TEXT)""")
conn.commit()
## write files:
site_web=pd.read_csv("../data/site_web.csv",sep=",",encoding="utf-8")
site_web= list(site_web.link)
for j in site_web:
    print j
    cursor.execute("INSERT INTO website(link) VALUES (%s)",[j] )
    conn.commit()
    cursor.execute(""" select * from "website" """)
    print cursor.rowcount
# close the database connection
conn.close()
