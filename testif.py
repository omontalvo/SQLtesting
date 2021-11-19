all_rows = [('getInactiveChats627499986405274345',), ('getInactiveChats',)]

all_rows = dict(all_rows)
which_call = 'getInactiveChats'

#print(type(all_rows[0]))
print(type(which_call))

if which_call in all_rows:
    print('its there')
else:
    print('not there')