#!/usr/local/bin/python3
import boto3

iam = boto3.client('iam')

def find_user_and_groups():
    for userlist in iam.list_users()['Users']:
        userGroups = iam.list_groups_for_user(UserName=userlist['UserName'])
        print("Username: "  + userlist['UserName'])
        print("Assigned groups: ")
        for groupName in userGroups['Groups']:
            print(groupName['GroupName'])
        print("----------------------------")