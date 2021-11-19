import requests
import setAuth
import sqlite3

whichcall = 'getDepartmentOperators'

# CREATE THE CALL
url = ('https://api.boldchat.com/aid/' + str(setAuth.aid) + '/data/rest/json/v2/'+str(whichcall)+'?auth=' + str(setAuth.auth)+"&DepartmentID=2720544441854219774")
r = requests.get(url)
Response = r.json()

# #Determine what each column name should be for the call
# reskeys = Response['Data'].keys()
# tablecols = []
# for i in reskeys:
#     tablecols.append(i)

# name = input("who are you?")

# lis='asdfa'
# print("hello %s %s" % (name, lis))

# print("CREATE TABLE if not exists ", name, "(%s)" % ",".join(tablecols), 'just more stuff')



datablock = Response['Data']
table_name = 'getChat'

# if 'Truncated' in Response:
#     print('truncated')
# else:
#     print('not truncated')
print (type(datablock))

if datablock == []:
    print('empty')
else:
    print('full')

# totallines = 0
# valueslist = []
# for item in datablock:
#     totallines = totallines +1
#     #print(datablock[item])
#     valueslist.append(str(datablock[item]))
#     #This insert uses " " as string identifiers and , as separators
# print('insert into  '+ table_name +' values ("%s")' % '","' .join(valueslist))
# print (totallines)