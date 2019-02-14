#!/usr/local/bin/python3

# IAM Compliance Audit script. Evaluates for inactive AWS IAM user accounts. 
#   - IAM User accounts not used in 90 days are disabled via removal of login profile and disablement access keys. 
#   - IAM User accounts not used in 180 days are removed from any IAM Groups and deleted.

import boto3
import collections
from datetime import datetime
from time import gmtime, strftime
#def lambda_handler(event, context):

disableDays = 90
deleteDays = 180
today = datetime.today().replace(tzinfo=None)
client = boto3.client('iam')
iam = boto3.resource('iam')

userList = client.list_users().get('Users', [])

for item in userList:
    user = iam.User(item.get('UserName'))
    if user.password_last_used != None:
        try:
            lastUsedDate = user.password_last_used.replace(tzinfo=None)
        except:
            continue
        #Evaluate if user has been active in last 90 days
        if (today - lastUsedDate).days > disableDays:
            recentKey = False
            for key in user.access_keys.all():
                try:
                    lastKeyUsedDate = client.get_access_key_last_used(AccessKeyId=key.id).get('AccessKeyLastUsed').get('LastUsedDate').replace(tzinfo=None)
                except:
                    continue
                if (today - lastKeyUsedDate).days < disableDays:
                    recentKey = True
                    break
            if not recentKey:
                #Delete user login profile
                try:
                    loginProfile = user.LoginProfile()
                    loginProfile.load()
                except:
                    pass
                else:
                    try:
                        print(user.user_name + " deleting login profile.")
                        loginProfile.delete()
                    except:
                        print(user.user_name + " doesn't seem to have a login profile or I couldn't delete it.")
                #Delete user access key
                for key in user.access_keys.all():
                    if key.status == 'Active':
                        print(user.user_name + " deleting key " + key.id)
                        key.deactivate()
                        key.delete()
        #Evaluate if user has been active in last 180. If not, then remove group memberships and delete user.
        if (today - lastUsedDate).days > deleteDays:
                activein180 = False
                #Remove user from all groups
                if not activein180:
                    try:
                        groups = client.list_groups_for_user(UserName=user.name)
                        for group in groups['Groups']:
                            client.remove_user_from_group(
                                GroupName=group['GroupName'],
                                UserName=user.name,
                            )
                        print(user.user_name + " removing from all IAM groups.")
                    except:
                        continue
                #Delete user account
                print(user.user_name + " deleting user account.")
                client.delete_user(
                    UserName=user.name
                )