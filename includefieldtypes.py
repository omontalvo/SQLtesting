import requests
import hashlib
import time
import csv
import setAuth
import sqlite3
import urllib.parse
import json

calllist = []

# #Full API List
# allapicalls = [
# "getChat",
# "getVisit",
# "getEmailThread",
# "getTicket",
# "getContact",
# "getFolder",
# "getDepartment",
# "getOperator",
# "getInactiveChats",
# "getAllChatMessages",
# "getInactiveVisits",
# "getAllPageViews-v1",
# "getAllPageViews-v2",
# "getAllInvitations",
# "getConversions",
# "getEmailThreads",
# "getOpenEmailThreads",
# "getClosedEmailThreads",
# "getTickets",
# "getClosedTickets",
# "getOpenTickets",
# "getContacts",
# "getLoginActivity",
# "getChatMessages",
# "getActiveChats",
# "getChatAssignments",
# "getPageViews",
# "getActiveVisits",
# "getInvitations",
# "getEmails",
# "getEmailAttachmentEntries",
# "getEmailThreadAssignments",
# "getTicketAssignments",
# "getOperatorDiscussions",
# "getSetupItems",
# "getFolders",
# "getDepartments",
# "getOperators",
# "getOperatorClients",
# "getDepartmentOperators",
# "getOperatorDepartments",
# "runReport",
# "getReport",
# "getSetupFolders",
# "createSetupFolder",
# "editSetupFolder",
# "deleteSetupFolder",
# "getChatCannedMessages",
# "createChatCannedMessage",
# "editChatCannedMessage",
# "deleteChatCannedMessage",
# "assignChat",
# "getEstimatedWaitTime",
# "enableAcdForChat",
# "getOperatorActiveChatCount",
# "getOperatorAvailability",
# "setOperatorAvailability",
# "createOperatorFromTemplate",
# "deleteOperator",
# "editOperator",
# "operatorLoginControl",
# "getCustomOperatorStatuses"
# ]

#Useful API list
allapicalls = [
"getContact",
"getEmailAttachmentEntries",
"getSetupItems",
"getOperatorAvailability",
"getLoginActivity",
"getChat",
"getChatMessages",
"getChatAssignments",
"getVisit",
"getPageViews",
"getInvitations",
"getEmailThread",
"getEmails",
"getEmailThreadAssignments",
"getTicket",
"getTicketAssignments",
"getDepartment",
"getDepartmentOperators",
"getOperator",
"getOperatorDepartments",
"getAllChatMessages",
"getAllInvitations",
"getFolders",
"getOperatorClients",
"getChatCannedMessages",
"getEstimatedWaitTime",
"getOperatorActiveChatCount",
"getCustomOperatorStatuses",
"getFolder","getInactiveChats", #Chat folders
"getEmailThreads","getOpenEmailThreads","getClosedEmailThreads", #Email Folders
"getTickets","getClosedTickets","getOpenTickets", #ticket folders
"getInactiveVisits","getConversions","getActiveVisits", #Visit Folders
"getContacts" #Contact Folders
]

missDict = {
'ChatID':'623638880973803728',
'VisitID':'623639645370484980',
'EmailThreadID':'3924341831011306775',
'TicketID':'2146920448858729817',
'ContactID':'1681073016909011362',
'DepartmentID':'3182880385675655036',
'OperatorID':'5676748830204723022',
'ServiceType':'1',
'ServiceTypeID':'1',
'EmailID':'4753038412152247658',
'FolderType':'97',
}

folderDict = {
'ChatFolderID':'622107834138401481',
'VisitsFolderID':'622107834503106727',
'EmailFolderID':'622107833801030026',
'TicketsFolderID':'622107834176585939',
'ContactsFolderID':'622107834439872219',
}

for i in allapicalls:

    # CREATE THE CALL
    url = ('https://api.boldchat.com/aid/' + str(setAuth.aid) + '/data/rest/json/v2/'+ i +'?auth=' + str(setAuth.auth)+'&IncludeFieldTypes=true')
    r = requests.get(url)
    Response = r.json()

    #calllist.append(i)
    #print(i)
    parkey =''
    parvalue = ''
    if 'Message' in Response:
        if str.split(Response['Message'])[0] == 'Missing':
            reqvar = str.split(Response['Message'])[1]
            reqcall = {'Required':reqvar}
            calldict = {i: reqcall}
            calllist.append(dict(calldict))
            print(i +": " +Response['Message'])

            # #Get missing values
            # parvalue = input(Response['Message']+": ")
            parkey = str.split(Response['Message'])[1]
            parvalue = missDict.get(str.split(Response['Message'])[1])


            #test folder breakdown
            if i in["getFolder","getInactiveChats"]:
                parvalue = '622107834138401481'
            elif i in ["getEmailThreads","getOpenEmailThreads","getClosedEmailThreads"]:
                parvalue = '622107833801030026'
            elif i in ["getTickets","getClosedTickets","getOpenTickets"]:
                parvalue = '622107834176585939'
            elif i in ["getInactiveVisits","getConversions","getActiveVisits"]:
                parvalue = '622107834503106727'
            elif i == "getContacts":
                parvalue = '622107834439872219'


            url = ('https://api.boldchat.com/aid/' + str(setAuth.aid) + '/data/rest/json/v2/'+ i +'?auth=' + str(setAuth.auth)+'&'+str(parkey) + '='+ str(parvalue)+'&IncludeFieldTypes=true')
            r = requests.get(url)
            Response = r.json()
            print(Response['Status'])
            filePathNameWExt = i+'.txt'
            with open(filePathNameWExt, 'w') as fp:
                json.dump(Response, fp,indent = 4)
        else:
            pass
    else:
        print(i+ ": nothing required")
        reqvar = "none"
        reqcall = {i:reqvar}
        calllist.append(dict(reqcall))
        #print(Response)

        # Write file
        filePathNameWExt = i+'.txt'
        with open(filePathNameWExt, 'w') as fp:
            json.dump(Response, fp,indent = 4)
        #end write file

        # url = ('https://api.boldchat.com/aid/' + str(setAuth.aid) + '/data/rest/json/v2/'+ i +'?auth=' + str(setAuth.auth)+'&IncludeFieldTypes=true')
        # r = requests.get(url)
        # Response = r.json()
        # if 'Message' in Response:
        #     print(Response['Message'])
        # elif 'FieldTypes' in Response:
        #     #print(Response['FieldTypes'].keys())
        #     # for field in Response['FieldTypes']:
        #     #     print(field)
        #     # #print(Response['FieldTypes'])
        #     pass
        # else:
        #     print('Field types are not provided for this call')


#print(calllist)