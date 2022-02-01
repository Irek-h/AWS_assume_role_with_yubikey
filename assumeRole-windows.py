from time import sleep
import boto3
import os
from subprocess import check_output
import sys
import pickle

from numpy import append



# User values



# ----
sts_client = boto3.client('sts')

def get_mfa_value():
    return sts_client.get_caller_identity()['Arn'].replace("user","mfa")

def backup_default_keys():
    with open('C:/Users/ireneusz.opalinski/.aws/credentials') as file:
        default_credentials = file.read()
    with open("C:/Users/ireneusz.opalinski/.aws/backup_credentials", 'w+') as backup:
        backup.write(default_credentials)
        return 0
    # os.popen('copy "C:/Users/ireneusz.opalinski/.aws/credentials" "C:/Users/ireneusz.opalinski/.aws/backup_credentials"')
    return 1

def get_token():
    return check_output('ykman oath accounts code -s').replace('\n', '')


def get_session_token():
    print("When yubikey lights up - touch it") 
    session_token = check_output('aws sts get-session-token --serial-number '+get_mfa_value()+' --token-code '+get_token())
    new = session_token.replace('{','').replace('}','').replace(':','').strip().split()
    del new[0]

    keys = list()
    values = list()
    for i in range(len(new)):
        
        if i%2==0:
            keys.append(new[i])
        else:
            values.append(new[i])

    return dict(zip(keys, values))

session_token = get_session_token()

print(session_token)

# def replace_credentials_with_sessionToken(sessionToken):
#     with open('testing.txt', 'w+') as file:
#         file.write(pickle.dumps(sessionToken))
#     return 0

# replace_credentials_with_sessionToken(session_token)