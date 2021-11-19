import requests
import hashlib
import time
import csv
import setAuth
import sqlite3
import foldersDB

calldict = {}

def tablemaker():
    global calldict
    #look at the Data section in the response, pull the first item from the response and use that to define keys
    callkeys=calldict[0].keys()
    callkeyslist=list(calldict[0].keys())

    #Build SQL Connnection
    conn = sqlite3.connect('scratch.db')
    c = conn.cursor()
    table_name = setAuth.aid+whichcall
    c.execute("CREATE TABLE if not exists {tb} (Item TEXT PRIMARY KEY)".\
                    format(tb='"'+str(table_name)+'"'))

    #Run through the first data set and add columns to the table for each key in the data set
    for info in callkeys:
        c.execute("ALTER TABLE {tb} ADD COLUMN {fd} TEXT".\
                    format(tb='"'+str(table_name)+'"', fd='"'+str(info)+'"'))

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

        # #URL Encode
        

        # if itemvalue == None:
        #     itemvalue = ""
        # else:
        #     pass
    

        c.execute("INSERT INTO {tn} (Item) VALUES ({item})".\
                format(tn=table_name, 
                cn=itemkey,
                item=itemcount, itemval='"'+str(itemvalue)+'"'
                ))
        conn.commit()

        #For this item get all value/key pairs into table
        
        calldictlength = len(calldict[x])
        while x < calldictlength:
            itemvalue = calldict[itemcount][callkeyslist[x]]
            itemkey = callkeyslist[x]

            if itemvalue == None:
                itemvalue = " "
            elif itemvalue == "":
                pass
            else:
                #URL Encode
                itemvalue = urllib.parse.quote(itemvalue)
                pass




            #print("x= ",x)
            #print(itemkey,itemvalue)
            c.execute("UPDATE {tn} SET {cn} = {itemval} WHERE Item = {item}".\
                    format(tn=table_name, 
                    cn=itemkey,
                    item=itemcount, itemval='"'+str(itemvalue)+'"'
                    ))
            #print(c.execute)
            conn.commit()
            
            x += 1
        itemcount += 1

    conn.close()
