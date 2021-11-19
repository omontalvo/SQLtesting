import requests
import setAuth
import sqlite3

departmentlist = []

sqlite_file = 'customer.db'    # name of the sqlite database file
table_name = setAuth.aid+'departments'   # name of the table to be created

#get departments
url = ('https://api.boldchat.com/aid/' + str(setAuth.aid) + '/data/rest/json/v2/getDepartments?auth=' + str(setAuth.auth))
r = requests.get(url)
DeptResponse = r.json()

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

c.execute("CREATE TABLE if not exists {tb} (DepartmentID text PRIMARY KEY, DeptName text)".\
                 format(tb='"'+table_name+'"'))

# if DeptResponse['Status'] == 'error':
#     print(DeptResponse['Message'])
# else:
#     for dept in DeptResponse['Data']:
#         print(dept['Name'], " ", dept['DepartmentID'])

#getdepts to list SSO details, username and department association
for dept in DeptResponse['Data']:
    #Request customer information to add to DB
    dpnm = dept['Name']
    dpID = dept['DepartmentID']  

    #Adds new customer information into DB
    c.execute("INSERT OR REPLACE INTO {tn} ('DepartmentID', 'DeptName') VALUES ({dpi}, {dpn})".\
            format(tn='"'+table_name+'"', 
            dpi='"' + dpID + '"', dpn='"' + dpnm + '"'
            ))

# Committing changes
conn.commit()
conn.close()


print("done")
