import requests
import setAuth
import sqlite3

whichcall = "getFolders"

# CREATE THE CALL
url = ('https://api.boldchat.com/aid/' + str(setAuth.aid) + '/data/rest/json/v2/'+ str(whichcall)+'?auth=' + str(setAuth.auth)+'&FromDate=2019-07-01T00:00:00.397Z&ToDate=2019-07-01T20:39:32.397Z')
r = requests.get(url)
Response = r.json()

parkey =''
parvalue = ''
#get folders list
print("Chat Folder IDs:")
for i in Response['Data']:
    if i['FolderType'] == 5:
        print( i['FolderID'], i['Name'])
    else:
        pass

folder = input("Which folder id do you want? ")
fromdate = input("What day do you want to start from?(2019-01-01)")
enddate = input("What day do you want to end on?(2019-01-01)")

#get all chats in period
url = ('https://api.boldchat.com/aid/' + str(setAuth.aid) + '/data/rest/json/v2/getInactiveChats?auth=' + str(setAuth.auth)+'&FromDate='+str(fromdate)+'T00:00:00.397Z&ToDate='+str(enddate)+'T20:39:32.397Z&FolderID='+folder)
r = requests.get(url)
Response = r.json()

for i in Response['Data']:
    chatid = i['ChatID']
    url = ('https://api.boldchat.com/aid/' + str(setAuth.aid) + '/data/rest/json/v2/getChatAssignments?auth=' + str(setAuth.auth)+'&ChatID='+chatid)
    r = requests.get(url)
    Response = r.json()
    if Response['Data']==[]:
        pass
    else:
        print (i['ChatID'])
        for assignments in Response['Data']:
            print(assignments)
        # print(Response['Data'])