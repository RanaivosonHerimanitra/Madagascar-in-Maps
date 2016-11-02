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
#cursor.execute("""CREATE TABLE all_page (link TEXT)""")
#conn.commit()
## write files:
all_page=pd.read_csv("../data/all_page.csv",sep=";",encoding="utf-8")
all_page= list(all_page.link)
for j in all_page:
    print j
    cursor.execute("INSERT INTO all_page(link) VALUES (%s)",[j] )
    conn.commit()
    cursor.execute(""" select * from "all_page" """)
    print cursor.rowcount
# close the database connection
conn.close()
