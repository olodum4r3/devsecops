#!/usr/local/bin/python3

users = [
    {'admin': True, 'active': True, 'name': 'Kevin'},
    {'admin': True, 'active': False, 'name': 'Bob'},
    {'admin': False, 'active': True, 'name': 'Ted'},
    {'admin': False, 'active': False, 'name': 'Mary'},
]   

line = 1

for user in users:
    prefix = f"{line} "


    if user['admin'] and user['active']:
        prefix = "Active - (ADMIN) "
    elif user['admin']:
        prefix = "(ADMIN) "
    elif user['active']:
        prefix = "ACTIVE - "
    else:
        prefix = ""

    print(prefix + user['name'])
    line += 1