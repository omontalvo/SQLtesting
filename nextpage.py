import requests
import hashlib
import time
import csv
import setAuth
import sqlite3
import urllib.parse


def maketable(table_name,calldict):
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablenames = c.fetchall()
    tablelist = []
    for tables in tablenames:
        tablelist.append(tables[0])


    if table_name in tablelist:
        print('Table is there')
        pass
    else:
        print('Table not exist')
        c.execute("CREATE TABLE if not exists {tb} (Item TEXT PRIMARY KEY, custAID)".\
                        format(tb='"'+str(table_name)+'"'))

        #Run through the first data set and add columns to the table for each key in the data set
        for info in callkeys:
            c.execute("ALTER TABLE {tb} ADD COLUMN {fd} TEXT".\
                        format(tb='"'+str(table_name)+'"', fd='"'+str(info)+'"'))

def filltable(table_name, calldict):
    #run through the Response dictionary for every entry in the keylist 
    #Script built for no valid data point as primary key
    #Set Row for current item 
    itemcount = 0

    for item in calldict:
        #X represents each set of values/keys
        x = 0

        #Get the value for the current pair we will insert 
        itemvalue = calldict[itemcount][callkeyslist[x]]
        itemkey = callkeyslist[x]

        c.execute("INSERT INTO {tn} (Item, custAID) VALUES ({item}, {cAID})".\
                format(tn=table_name, 
                cn=itemkey,
                item=itemcount, cAID=setAuth.aid
                ))
        conn.commit()

        #For this item get all value/key pairs into table 
        calldictlength = len(calldict[x])
        while x < calldictlength:
            itemvalue = calldict[itemcount][callkeyslist[x]]
            itemkey = callkeyslist[x]

            if itemvalue == None:
                itemvalue = " "
            else:
                pass

            c.execute("UPDATE {tn} SET {cn} = {itemval} WHERE Item = {item}".\
                    format(tn=table_name, 
                    cn=itemkey,
                    item=itemcount, itemval='"'+str(itemvalue)+'"'
                    ))
            conn.commit()
            
            x += 1
        itemcount += 1

    conn.close()



whichcall = "getInactiveChats"#input("What call do you want to make? ")

# CREATE THE CALL
url = ('https://api.boldchat.com/aid/' + str(setAuth.aid) + '/data/rest/json/v2/'+ str(whichcall)+'?auth=' + str(setAuth.auth)+"&FolderID=622107834138401481")
r = requests.get(url)
Response = r.json()



#Build SQL Connnection
conn = sqlite3.connect('scratch5.db')
c = conn.cursor()
table_name = whichcall + setAuth.aid

#dictionary of all items 
calldict = Response['Data']

#look at the Data section in the response, determine if it is a single item or multiline item

callkeys=Response['Data'][0].keys()
callkeyslist=list(Response['Data'][0].keys())
#maketable(table_name,calldict)

filltable(table_name,calldict)
