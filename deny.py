#!/usr/local/bin/python3

import json
import boto3

iam = boto3.client('iam')

deny_all_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Action": "*",
            "Resource": "*"
        }
    ]
}

response = iam.create_policy(
    PolicyName='DenyAllPolicy',
    PolicyDocument=json.dumps(deny_all_policy)
)
print(response)