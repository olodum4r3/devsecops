#!/usr/local/bin/python3

import boto3

iam = boto3.client('iam')

paginator = iam.get_paginator('get_policy')
for response in paginator.paginate():
    print(response)