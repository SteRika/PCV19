from tkinter import *
import tkinter as tk
from decimal import Decimal,getcontext
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import urllib.request as urllibreq
import requests
import json
import sys
from functools import partial
from gql import Client, gql
import pytest
from graphqlclient import *
username = '038129'
password = 'asdasdqwe'

query = """mutation login {
        logIn(input: { username: "%s", password: "%s" }) {
          viewer {
            sessionToken
            user {
              objectId
              username
              ptsnUser {
                fullname
              }
            }
          }
        }
        }""" % (username,password)
headers = {
  "X-Parse-Application-Id": "myAppId",
}
url = 'http://192.168.88.19:1338/graphql'
r = requests.post(url, json={'query': query},headers=headers)
a = r.text
a = a.strip('{')
a = a.replace('{','')
a = a.replace('}','')
a = a.replace('"','')
a = a.replace(',',':')
final = a.split(':')
#print(final)
testid = final[8]
name = final[13].strip()
badge = final[10]
token = final[4]+':'+final[5]
'''print(r.text)
print(final)
print(token)
print(testid)
print("name is %s" % name)
print("Employee Number is %s" % badge)'''

query2 = '''query test {
            roles(where: {
              users: {
                have: {
                  objectId: {
                    equalTo: "%s"
                  } 
                }
              }
            }){
              edges {
                node {
                  name
                }
              }
            }
          }''' % (testid)
headers2 = {
  "X-Parse-Application-Id": "myAppId",
  "X-Parse-Session-Token": "%s"%token
}
r2 = requests.post(url, json={'query': query2},headers=headers2)
'''print(query2)
print(r2.text)'''
b = r2.text
b = b.strip('{')
b = b.replace('{','')
b = b.replace('}','')
b = b.replace('"','')
b = b.replace(',',':')
final2 = b.split(':')
print (final2)
role = final2[5].strip()
role = role.replace(']','')
testbadge = '038985'
client = GraphQLClient('http://192.168.88.19:1337/graphql')

query3 = '''query MyQuery {
    ptsnUsers(where: {badgeNo: {equalTo: "%s"}}) {
      edges {
        node {
          objectId
        }
      }
    }
}'''% testbadge


headers3 = {
  "X-Parse-Application-Id": "myAppId",
  "X-Parse-Session-Token": "%s"%token
}

r3 = requests.post(url, json={'query': query3},headers=headers3)

c = r3.text
c = c.strip('{')
c = c.replace('{','')
c = c.replace('}','')
c = c.replace('"','')
c = c.replace(',',':')
final3 = c.split(':')
objectid = final3[5].strip()
objectid = objectid.replace(']','')
print(objectid)
print (final3)
#print(objectid)

json = {
  "query": '''   
    mutation saveMonitoredUser($input: CreateMonitoredUserFieldsInput!) {
		createMonitoredUser(input: { fields: $input }) {
			monitoredUser {
				id
			}
		}
	}
  ''',
  "variables": {
    "input": {
    "ptsnUser": {
      "link": "%s"%objectid
    },
    "status": "OC", 
    "remarks": "DIARE,DEMAM,HIDUNG TERSUMBAT,NYERI PUNGGUNG,SESAK NAFAS,SAKIT KEPALA,MENGGIGIL,BATUK KERING,HILANG PENCIUMAN,MATA MERAH,KELELAHAN,38.5"
	}
}
  }

headers4 = {
  "X-Parse-Application-Id": "myAppId",
  "X-Parse-Session-Token": "%s"%token
}

r4 = requests.post(url, json=json,headers=headers4)

#print(r4.text)


