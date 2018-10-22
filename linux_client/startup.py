import json
import getpass
import requests
import sys
import os
from os import walk
import hashlib
from functools import partial
import tempfile

def md5sum(f):
    d = hashlib.md5()
    for buf in iter(partial(f.read, 128), b''):
        d.update(buf)
    return d.hexdigest()

def upload(login_URL,upload_URL,username,password,Base_Folder,To_Be_Uploaded):
    '''
    To Parikshit, please note the change in the method's arguments,
    it now needs the publickey file path as it's 5th argument
    '''

    client = requests.Session()
    client.get(login_URL)
    csrftoken = client.cookies['csrftoken']

    payload = {
        'csrfmiddlewaretoken': csrftoken,
        'username': username,
        'password': password
    }
    files = []
    r = client.post(login_URL, data=payload, headers=dict(Referer=login_URL))

    client.get(upload_URL)
    csrftoken = client.cookies['csrftoken']
    for (root, dirnames, filenames) in walk(To_Be_Uploaded):
    	for name in filenames:
	        files.append((name, (os.path.relpath(root, Base_Folder))))


    for file in files:
        file_path = file[1]
        temp = open(os.path.join(Base_Folder, file_path, file[0]), 'rb')
        md5sum1 = md5sum(temp)
        payload = {
            'csrfmiddlewaretoken': csrftoken,
            'file_path': file_path,
            'md5sum': md5sum1,
        }
        f = {"file": open(os.path.join(Base_Folder,file_path,file[0]), 'rb')}
        r = client.post(upload_URL, data=payload, files=f, headers=dict(Referer=upload_URL))
        print('.',end='',flush=True)

    print('Completed')
    print("Upload Successfull")

def set_url(parameter,url,out):
    with open(out) as f:
        data = json.load(f)
    data[parameter] = url
    with open(out, 'w') as outfile:
        json.dump(data, outfile)

def config_edit(out):
    with open(out) as f:
        data = json.load(f)
    data['username'] = input('Username : ')
    temp = getpass.getpass(prompt='Password : ', stream=None)
    temp1 = getpass.getpass(prompt='Confirm Password : ', stream=None)
    if (temp == temp1) :
        data['password'] = temp
    else :
        while (temp != temp1) :
            print ("The Passwords didn't match. Kindly try again.")
            temp = getpass.getpass(prompt='Password : ', stream=None)
            temp1 = getpass.getpass(prompt='Confirm Password : ', stream=None)
        data['password'] = temp
    print("Your configurations have been updated.")
    with open(out, 'w') as outfile:
        json.dump(data, outfile)

def empty_json(out):
    data = {}
    with open(out, 'w') as outfile:
        json.dump(data, outfile)

def sync(out):
    with open(out) as f:
        data = json.load(f)
    upload(data['server_url']+'accounts/login/',data['server_url']+'upload/test/',data['username'],data['password'],data['home_dir'],data['home_dir'])

if (sys.argv[1] == 'config') :
    config_edit(sys.argv[2])
if (sys.argv[1] == 'set_server') :
    set_url('server_url',sys.argv[2],sys.argv[3])
if (sys.argv[1] == 'observe') :
    set_url('home_dir',sys.argv[2],sys.argv[3])
if (sys.argv[1] == 'sync'):
    sync(sys.argv[2])
if (sys.argv[1] == 'empty_json'):
    empty_json(sys.argv[2])
