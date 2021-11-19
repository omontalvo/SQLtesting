import sqlite3
import hashlib
import time


sqlite_file = 'customer.db'    # name of the sqlite database file
table_name = 'API'   # name of the table to be created

deleinput = ''


def addCustomer():
        # Connecting to the database file
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()

        #Request customer information to add to DB
        custname = persvariable 
        #input("Please provide the customer name: ")
        aid = input("Please provide the customer AID: ")
        settingsID = input("What is the Settings ID: ")
        api_key = input("What is the API Key: ")

        #Adds new customer information into DB
        c.execute("INSERT OR REPLACE INTO {tn} (aid, settingID, apiKey,Name) VALUES ({custaid}, {custsettings}, {custkey}, {cusname})".\
                format(tn=table_name, 
                custaid=aid, custsettings=settingsID, cusname = '"' + custname + '"', custkey= '"' + api_key + '"'
                ))

        # Committing changes
        conn.commit()
        conn.close()

def listCust():
        # Connecting to the database file
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        
        #Selects all AIDs and Names for customers in table
        c.execute('SELECT "aid", "Name" FROM {tn} '.\
                format(tn=table_name))
        all_rows = c.fetchall()
        
        #Prints Name and AID for all customers in table
        for member in all_rows:
                print(member[1],member[0])
        conn.close()

def delCust(todel):
        # Connecting to the database file
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        #Deletes a row based on Name column
        c.execute('DELETE FROM {tn} WHERE "Name" = {dl}'.\
                format(tn=table_name, dl = '"'+todel+'"'))
        conn.commit()
        conn.close()


def settingauth():
        # SET AUTH parameters
        seconds = time.time()
        timestamp = int(seconds * 1000)
        token = str(aid) + ":" + str(settingID) + ":" + str(timestamp) + str(api_key)
        hash = hashlib.sha512(token.encode('utf-8')).hexdigest()
        global auth
        auth = str(aid) + ":" + str(settingID) + ":" + str(timestamp) + ":" + str(hash)


auth = ""

listCust()
print()
persvariable = 'personal'


# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()


#Selects all data for selected customer
c.execute('SELECT * FROM {tn} WHERE "Name" = {pv}'.\
        format(tn=table_name, pv='"'+persvariable+'"'))
all_rows = c.fetchall()



if persvariable == 'delete':
        deleinput = input('Who do you want to delete(cannot be recovered): ')
        delCust(deleinput)
        quit()
elif all_rows == []:
        addCustomer()
        pass
else:
        pass

#Set Account info from Dictionary file
aid = all_rows[0][0]
settingID = all_rows[0][1]
api_key = all_rows[0][2]
name = all_rows[0][3]

settingauth()



