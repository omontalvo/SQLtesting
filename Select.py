import sqlite3


sqlite_file = 'customerInfo.sqlite'    # name of the sqlite database file
table_name = 'cusKeys'   # name of the table to be created

column_type = 'TEXT' # E.g., INTEGER, TEXT, NULL, REAL, BLOB


colone = 'aid'
coltwo = 'settingID'
colthree = 'apiKey'
colfour = 'Name'

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



#Deletes a row based on Name column
c.execute('DELETE FROM {tn} WHERE "Name" = "test"'.\
        format(tn=table_name))


# Closing the connection to the database file
conn.commit()
conn.close()