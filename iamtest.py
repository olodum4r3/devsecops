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
    print(u)