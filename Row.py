import sqlite3

conn = sqlite3.connect("customerInfo.sqlite")
c = conn.cursor()


conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute('select * from cusKeys')

r = c.fetchone()

type(r)
print("type: ", type(r))

tuple(r)
print("tuple: ", tuple(r))

len(r)
print("length: ", len(r))

r[1]
print(r[0])

r.keys()
print(r.keys())

r['Name']
print(r['Name'])

for member in r:
    print(member)