import requests
import setAuth

# folddict = []

# #getFolders
# url = ('https://api.boldchat.com/aid/' + str(setAuth.aid) + '/data/rest/json/v2/getFolders?auth=' + str(setAuth.auth))
# r = requests.get(url)
# FoldResponse = r.json()

# #Create Folder Dictionary
# for folder in FoldResponse['Data']:
#     #print(folder["FolderType"])
#     if folder['FolderType'] in [5]:
#         folddict.append(folder['FolderID'])
#         #print(folder["FolderID"])
#     else:
#         pass

# #print(folddict)

import requests
import sqlite3

def stringreplace(i):
    if i == 'RowNumber':
        pass #skip adding a Row Number to the DB for multipage items
    elif  '\\' in str(item[i]):  #\ in string will break SQL insert, replace with nothing
        valitem = str(item[i])
        valitem = valitem.replace('\\','')
        if '"' in valitem: #" will break SQL insert, replace with escaped single quote
            valitem = valitem.replace('"','\'')
            valueslist.append(str(valitem))
        else:
            valueslist.append(str(valitem))
    elif '"' in str(item[i]): #" will break SQL insert, replace with escaped single quote
        valitem = str(item[i])
        valitem = valitem.replace('"','\'')
        valueslist.append(str(valitem))
    else:
        valueslist.append(str(item[i])) #add item to list for insert



#for folder in folddict:
folderid = '151796850906294071'#'622107834138401481'
datablock = []
if datablock == []:
    whichcall = 'getInactiveChats'
    FromDate = "2019-08-12T05:00:00.397Z"
    ToDate = "2019-08-13T05:00:00.397Z"

    # CREATE THE CALL
    url = ('https://api.boldchat.com/aid/' + str(setAuth.aid) + '/data/rest/json/v2/'+ str(whichcall)+'?auth=' + str(setAuth.auth)+'&FromDate=' + str(FromDate)+'&ToDate=' + str(ToDate)+'&FolderID='+str(folderid))
    r = requests.get(url)
    Response = r.json()

    datablock = Response['Data']



if type(datablock) == list and datablock != []:
    reskeys=Response['Data'][0].keys()
elif datablock != []:
    reskeys=Response['Data'].keys()

#Determine what each column name should be for the call
#reskeys = Response['Data'][0].keys()
tablecols = []
for i in reskeys:
    tablecols.append(i)

#Build SQL Connnection
dbname = str(setAuth.aid)+'.db'
conn = sqlite3.connect(dbname)
c = conn.cursor()
table_name = "allfolderschatsSingleFolder"

#Check if table already exists, if not create it
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
    c.execute("CREATE TABLE if not exists "+ table_name + "(%s)" % ",".join(tablecols))

if 'Truncated' in Response:
    truncated = Response['Truncated']
else:
    truncated = False

#Populate the tables
#check for truncation
if truncated != True:
    #check if the call returns a single item
    if type(datablock) == dict:
        totallines = 0
        valueslist = []
        for item in datablock:
            totallines = totallines +1
            valueslist.append(str(datablock[item]))
            #This insert uses " " as string identifiers and , as separators
        c.execute('insert into  '+ table_name +' values ("%s")' % '","' .join(valueslist))
        print ('Lines added: ' , totallines)
    #or multiple items
    else:
        totallines = 0
        for item in datablock:
            valueslist = []
            totallines = totallines +1
            for i in item:
                stringreplace(i)             
            #This insert uses " " as string identifiers and , as separators
            c.execute('insert into  '+ table_name +' values ("%s")' % '","' .join(valueslist))
        print ('Lines added: ' , totallines)
#When truncated, handle paging

else:
    print(url)
    page = 0
    totallines = 0
    while truncated == True:
        conn.commit()
        #totallines = 0
        #Add each item as a row
        for item in datablock:
            valueslist = []
            totallines = totallines +1
            for i in item:
                stringreplace(i)

            #This insert uses " " as string identifiers and , as separators
            print(valueslist[0])
            c.execute('insert into  '+ table_name + ' values ("%s")' % '","' .join(valueslist))
        print ('Lines added: ' , totallines)
        
        nextpage = Response['NextPage']
        # CREATE THE Next CALL
        url = ('https://api.boldchat.com/aid/' + str(setAuth.aid) + '/data/rest/json/v2/'+str(whichcall)+'?auth=' + str(setAuth.auth)+'&NextPage='+str(nextpage)+'&FromDate=' + str(FromDate)+'&ToDate=' + str(ToDate)+'&FolderID='+str(folderid))
        r = requests.get(url)
        Response = r.json()
        #print(nextpage)
        if 'Message' in Response:
            print(Response['Message'])
            setAuth.settingauth()
            url = ('https://api.boldchat.com/aid/' + str(setAuth.aid) + '/data/rest/json/v2/'+str(whichcall)+'?auth=' + str(setAuth.auth)+'&NextPage='+str(nextpage)+'&FromDate=' + str(FromDate)+'&ToDate=' + str(ToDate)+'&FolderID='+str(folderid))
            r = requests.get(url)
            Response = r.json()
            #print(nextpage)
        else:
            pass
        datablock = Response['Data']
        truncated = Response['Truncated']
        page = page + 1
        print('Page count: ' , page)

    #handle last page
    #totallines = 0
    for item in datablock:
        valueslist = []
        totallines = totallines + 1
        for i in item:
            stringreplace(i)
        c.execute('insert into  ' + table_name + ' values ("%s")' % '","' .join(valueslist))
    print('Lines added: ' , totallines)
    

conn.commit()
conn.close()

#get each chat id in datablock and get assignment info
for line in datablock:
    print(line['ChatID'])

    chatid = line['ChatID']
    datablock = []
    if datablock == []:
        whichcall = 'getChatAssignments'
        FromDate = "2019-08-12T05:00:00.397Z"
        ToDate = "2019-08-13T05:00:00.397Z"

        # CREATE THE CALL
        url = ('https://api.boldchat.com/aid/' + str(setAuth.aid) + '/data/rest/json/v2/'+ str(whichcall)+'?auth=' + str(setAuth.auth)+'&ChatID='+str(chatid))
        r = requests.get(url)
        Response = r.json()

        datablock = Response['Data']



    if type(datablock) == list and datablock != []:
        reskeys=Response['Data'][0].keys()
    elif datablock != []:
        reskeys=Response['Data'].keys()

    #Determine what each column name should be for the call
    #reskeys = Response['Data'][0].keys()
    tablecols = []
    for i in reskeys:
        tablecols.append(i)

    #Build SQL Connnection
    dbname = str(setAuth.aid)+'.db'
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    table_name = "getChatAssignments"

    #Check if table already exists, if not create it
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
        c.execute("CREATE TABLE if not exists "+ table_name + "(%s)" % ",".join(tablecols))

    if 'Truncated' in Response:
        truncated = Response['Truncated']
    else:
        truncated = False

    #Populate the tables
    #check for truncation
    if truncated != True:
        #check if the call returns a single item
        if type(datablock) == dict:
            totallines = 0
            valueslist = []
            for item in datablock:
                totallines = totallines +1
                valueslist.append(str(datablock[item]))
                #This insert uses " " as string identifiers and , as separators
            c.execute('insert into  '+ table_name +' values ("%s")' % '","' .join(valueslist))
            print ('Lines added: ' , totallines)
        #or multiple items
        else:
            totallines = 0
            for item in datablock:
                valueslist = []
                totallines = totallines +1
                for i in item:
                    stringreplace(i)             
                #This insert uses " " as string identifiers and , as separators
                c.execute('insert into  '+ table_name +' values ("%s")' % '","' .join(valueslist))
            print ('Lines added: ' , totallines)
    #When truncated, handle paging

    else:
        print(url)
        page = 0
        totallines = 0
        while truncated == True:
            conn.commit()
            #totallines = 0
            #Add each item as a row
            for item in datablock:
                valueslist = []
                totallines = totallines +1
                for i in item:
                    stringreplace(i)

                #This insert uses " " as string identifiers and , as separators
                print(valueslist[0])
                c.execute('insert into  '+ table_name + ' values ("%s")' % '","' .join(valueslist))
            print ('Lines added: ' , totallines)
            
            nextpage = Response['NextPage']
            # CREATE THE Next CALL
            url = ('https://api.boldchat.com/aid/' + str(setAuth.aid) + '/data/rest/json/v2/'+ str(whichcall)+'?auth=' + str(setAuth.auth)+'&ChatID='+str(chatid))
            r = requests.get(url)
            Response = r.json()
            #print(nextpage)
            if 'Message' in Response:
                print(Response['Message'])
                setAuth.settingauth()
                url = ('https://api.boldchat.com/aid/' + str(setAuth.aid) + '/data/rest/json/v2/'+ str(whichcall)+'?auth=' + str(setAuth.auth)+'&ChatID='+str(chatid))
                r = requests.get(url)
                Response = r.json()
                #print(nextpage)
            else:
                pass
            datablock = Response['Data']
            truncated = Response['Truncated']
            page = page + 1
            print('Page count: ' , page)

        #handle last page
        #totallines = 0
        for item in datablock:
            valueslist = []
            totallines = totallines + 1
            for i in item:
                stringreplace(i)
            c.execute('insert into  ' + table_name + ' values ("%s")' % '","' .join(valueslist))
        print('Lines added: ' , totallines)
        

    conn.commit()
    conn.close()