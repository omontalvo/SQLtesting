import requests
import hashlib
import time
import csv
import setAuth
import sqlite3


sqlite_file = 'customer.db'    # name of the sqlite database file
table_name = setAuth.aid+'operators'   # name of the table to be created

#print(table_name)

#getOperators
url = ('https://api.boldchat.com/aid/' + str(setAuth.aid) + '/data/rest/json/v2/getOperators?auth=' + str(setAuth.auth))
r = requests.get(url)
OperResponse = r.json()

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

c.execute("CREATE TABLE if not exists {tb} (LoginID text PRIMARY KEY, Name text, UserName text, SSOID text, PermissionGroupID text)".\
                 format(tb='"'+table_name+'"'))

#getOperators to list SSO details, username and department association
for operator in OperResponse['Data']:
    #Request customer information to add to DB
    opnm = operator['Name']
    opusernm = operator['UserName']
    oplog = operator['LoginID']
    if operator['SSONameID'] == None:
        opsso = "None"
    else:
        opsso = operator['SSONameID']
    if operator['PermissionGroupID'] == None:
        opper = "Unlimited"
    else:
        opper = operator['PermissionGroupID']


    #Adds new customer information into DB
    c.execute("INSERT OR REPLACE INTO {tn} ('LoginID', 'Name', 'UserName','SSOID', 'PermissionGroupID') VALUES ({opl}, {opn}, {opu}, {ops}, {opper})".\
            format(tn='"'+table_name+'"', 
            opl='"' + oplog + '"', opn='"' + opnm + '"', opu = '"' + opusernm + '"', ops= '"' + opsso + '"', opper = '"' + opper + '"'
            ))

# Committing changes
conn.commit()
conn.close()


print("done")
