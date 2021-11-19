import requests
import hashlib
import time
import csv
import setAuth
import sqlite3


sqlite_file = 'customer.db'    # name of the sqlite database file
table_name = setAuth.aid+'folders'   # name of the table to be created

#getFolders
url = ('https://api.boldchat.com/aid/' + str(setAuth.aid) + '/data/rest/json/v2/getFolders?auth=' + str(setAuth.auth))
r = requests.get(url)
FoldResponse = r.json()

#print(FoldResponse['Data'][1])
# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

c.execute("CREATE TABLE if not exists {tb} (FolderID text PRIMARY KEY, Name text, FolderType text, ParentFolderID text)".\
                 format(tb='"'+table_name+'"'))

for folder in FoldResponse['Data']:
    #Request customer information to add to DB
    flnm = folder['Name']
    flid = folder['FolderID']
    fltp = folder['FolderType']
    if folder['ParentFolderID'] == None:
        flpf = "None"
    else:
        flpf = folder['ParentFolderID']

    #Adds new customer information into DB
    c.execute("INSERT OR REPLACE INTO {tn} ('FolderID', 'Name', 'FolderType','ParentFolderID') VALUES ({flid}, {fln}, {flt}, {fpf})".\
            format(tn='"'+table_name+'"', 
            flt='"' + str(fltp) + '"', fln='"' + str(flnm) + '"', flid = '"' + str(flid) + '"', fpf= '"' + str(flpf) + '"'
            ))

# Committing changes
conn.commit()
conn.close()


#print("done")
