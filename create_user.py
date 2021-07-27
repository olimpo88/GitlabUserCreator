#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import sys
import csv
from os import path

if len(sys.argv)<2:
	print("This script requires at least two parameters 'python create_user.py url token path_csv_file(optional)'")
	exit()
else:
	API_URL="%s/api/v4"%(sys.argv[1])
	HEADERS={'PRIVATE-TOKEN': sys.argv[2]}

PATH_FILE='users.csv'
if len(sys.argv)==4:
	PATH_FILE=sys.argv[3]
	
def get_users():
	users=[]
	if not path.exists(PATH_FILE):
		print("No such file or directory: %s"%PATH_FILE)
		return users

	with open(PATH_FILE) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			admin="false"
			if row[3]=='admin':
				admin="true"
			users.append({'name':row[0], 'username':row[1], 'email':row[2], 'admin':admin})
	return users

def search_user(search):
	r = requests.get("%s/users?search=%s"%(API_URL,search),headers=HEADERS)
	if r.status_code==200:
		if len(r.json())==1:
			return r.json()[0]['id']
		elif len(r.json())>1:
			print("Error: more than one match searching %s"%search)
	else:
		print("Error: ",r.text)
	return False

def edit_user(id_user,user_data):
	payload = { 'name': user_data['name'], 'admin': user_data['admin']}
	r = requests.put("%s/users/%s"%(API_URL,id_user),headers=HEADERS,data=payload)
	if r.status_code==200:
		return True
	else:
		print("Error: ",r.text)
	return False

def create_user(user_data):
	payload = { 'name': user_data['name'], 'username': user_data['username'], 'email':user_data['email'], 'admin': user_data['admin'], 'reset_password': 'true', 'force_random_password': 'true'}
	r = requests.post("%s/users"%(API_URL),headers=HEADERS,data=payload)
	if r.status_code==201:
		return True
	else:
		print("Error: ",r.text)
	return False

users=get_users()
for u in users:
	id_user=search_user(u['email'])
	if id_user:
		if edit_user(id_user,u):
			print("User %s was edited"%(u['email']))
	else:
		id_user=search_user(u['username'])
		if id_user:
			print("It is not possible to create the user %s, it already exists"%u['username'])
		else:
			if create_user(u):
				print("User %s was created"%(u['email']))