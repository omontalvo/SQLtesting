import requests
import csv
import urllib.parse
import setAuth
import sqlite3



# CREATE THE CALL TO GET CHAT IDS

url = ('https://api.boldchat.com/aid/' + str(setAuth.aid) + '/data/rest/json/v2/getInactiveChats?auth=' + str(setAuth.auth) + '&FolderID=' + str(folselect) + '&NextPage=' + str(NextPageHash))
r = requests.get(url)
Response = r.json()
Truncated = Response['Truncated']
if Truncated == True:
    NextPageHash = Response['NextPage']

# CHECK THE STATUS CODE
status_code = r.status_code
error_code = r.json().get('Status')

#print(Response)
