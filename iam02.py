import boto3
import collections
from datetime import datetime
from time import gmtime, strftime

notOkayDays = 120
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
        if (today - lastUsedDate).days > notOkayDays:
            recentKey = False
            for key in user.access_keys.all():
                lastKeyUsedDate = client.get_access_key_last_used(AccessKeyId=key.id).get('AccessKeyLastUsed').get('LastUsedDate').replace(tzinfo=None)
                if (today - lastKeyUsedDate).days < notOkayDays:
                    recentKey = True
                    break
            if not recentKey:
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
                for key in user.access_keys.all():
                    if key.status == 'Active':
                        print(user.user_name + " deactivating key " + key.id)
                        key.deactivate()