#!/usr/local/bin/python3

import boto3
import collections
from datetime import datetime
from time import gmtime, strftime

today = datetime.today().replace(tzinfo=None)
client = boto3.client('iam')
iam = boto3.resource('iam')

users = client.list_users()
for u in users['Users']:
    print(u['UserName'])
    groups = client.list_groups_for_user(UserName=u['UserName'])
    for g in groups['Groups']:
        print(g['GroupName'])
        response = client.remove_user_from_group(
            GroupName=g['GroupName'],
            UserName=u['UserName'],
        )
        print(response)