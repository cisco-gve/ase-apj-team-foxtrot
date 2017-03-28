#
# Generated FMC REST API sample script
#
 
import json
import sys
import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
 
server = "https://198.18.133.8"
 
username = "admin"
if len(sys.argv) > 1:
    username = sys.argv[1]
password = "sf"
if len(sys.argv) > 2:
    password = sys.argv[2]
    
print "Retrieving all Access Policies..."

r = None
headers = {'Content-Type': 'application/json'}
api_auth_path = "/api/fmc_platform/v1/auth/generatetoken"
auth_url = server + api_auth_path
try:
    # 2 ways of making a REST call are provided:
    # One with "SSL verification turned off" and the other with "SSL verification turned on".
    # The one with "SSL verification turned off" is commented out. If you like to use that then 
    # uncomment the line where verify=False and comment the line with =verify='/path/to/ssl_certificate'
    # REST call with SSL verification turned off: 
    r = requests.post(auth_url, headers=headers, auth=requests.auth.HTTPBasicAuth(username,password), verify=False)
    # REST call with SSL verification turned on: Download SSL certificates from your FMC first and provide its path for verification.
    # r = requests.post(auth_url, headers=headers, auth=requests.auth.HTTPBasicAuth(username,password), verify='/path/to/ssl_certificate')
    auth_headers = r.headers
    auth_token = auth_headers.get('X-auth-access-token', default=None)
    if auth_token == None:
        print("auth_token not found. Exiting...")
        sys.exit()
except Exception as err:
    print ("Error in generating auth token --> "+str(err))
    sys.exit()
 
headers['X-auth-access-token']=auth_token
 
api_path = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/policy/accesspolicies"    # param
url = server + api_path
if (url[-1] == '/'):
    url = url[:-1]
 
# GET OPERATION
 

try:
    # REST call with SSL verification turned off: 
    r = requests.get(url, headers=headers, verify=False)
    # REST call with SSL verification turned on:
    # r = requests.get(url, headers=headers, verify='/path/to/ssl_certificate')
    status_code = r.status_code
    resp = r.text
    if (status_code == 200):
        #print("GET successful. Response data --> ")
        print "The current Access Policies are: "
        json_resp = json.loads(resp)
        for i in range(len(json_resp["items"])):
            print json_resp["items"][i]["name"]
        #print(json.dumps(json_resp,sort_keys=True,indent=4, separators=(',', ': ')))
    else:
        r.raise_for_status()
        print("Error occurred in GET --> "+resp)
except requests.exceptions.HTTPError as err:
    print ("Error in connection --> "+str(err)) 
finally:
    if r : r.close()

choice = raw_input("Type the name of the Access Policy for which you would like to see the rules: ")

for i in range(len(json_resp["items"])):
    if choice in json_resp["items"][i].values():
        container_id = json_resp["items"][i]["id"]

api_path = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/policy/accesspolicies/" + container_id + "/accessrules"    # param
url = server + api_path
if (url[-1] == '/'):
    url = url[:-1]

print "Fetching rules..."

try:
    # REST call with SSL verification turned off: 
    r = requests.get(url, headers=headers, verify=False)
    # REST call with SSL verification turned on:
    # r = requests.get(url, headers=headers, verify='/path/to/ssl_certificate')
    status_code = r.status_code
    resp = r.text
    if (status_code == 200):
        #print("GET successful. Response data --> ")
        json_resp = json.loads(resp)
        for i in range(len(json_resp["items"])):
            print json_resp["items"][i]["name"]
            #if json_resp["items"][i]["enabled"] == True:
            #    print "Enabled"
            #else:
            #    print "Disabled"      
        #print(json.dumps(json_resp,sort_keys=True,indent=4, separators=(',', ': ')))
    else:
        r.raise_for_status()
        print("Error occurred in GET --> "+resp)
except requests.exceptions.HTTPError as err:
    print ("Error in connection --> "+str(err)) 
finally:
    if r : r.close()


choice2 = raw_input("Type the name of rule which you would like to enable / disable: ")

for i in range(len(json_resp["items"])):
    if choice2 in json_resp["items"][i].values():
        rule_id = json_resp["items"][i]["id"]

api_path = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/policy/accesspolicies/" + container_id + "/accessrules/" + rule_id
url = server + api_path
if (url[-1] == '/'):
    url = url[:-1]

try:
    # REST call with SSL verification turned off: 
    r = requests.get(url, headers=headers, verify=False)
    # REST call with SSL verification turned on:
    # r = requests.get(url, headers=headers, verify='/path/to/ssl_certificate')
    status_code = r.status_code
    resp = r.text
    if (status_code == 200):
        #print("GET successful. Response data --> ")
        json_resp = json.loads(resp)
       # print json.dumps(json_resp["metadata"])
       # for i in range(len(json_resp["items"])):
       #     print json_resp["items"][i]["name"]
       #     print json_resp["items"][i]["id"]         
        #print(json.dumps(json_resp,sort_keys=True,indent=4, separators=(',', ': ')))
    else:
        r.raise_for_status()
        print("Error occurred in GET --> "+resp)
except requests.exceptions.HTTPError as err:
    print ("Error in connection --> "+str(err)) 
finally:
    if r : r.close()

newBool = True

if json_resp["enabled"] == True:
    print choice2 + " will be DISABLED"
    newBool = False
else:
    print choice2 + " will be ENABLED"  

put_data = {
  "action": json_resp["action"],
  "enabled": newBool,
  "type": json_resp["type"],
  "name": json_resp["name"],
  "id": json_resp["id"],
  "sourceZones": json_resp["sourceZones"],
  "destinationZones": json_resp["destinationZones"],
  "logFiles": False,
  "logBegin": False,
  "logEnd": False,
}

try:
    # REST call with SSL verification turned off:
    r = requests.put(url, data=json.dumps(put_data), headers=headers, verify=False)
    # REST call with SSL verification turned on:
    # r = requests.put(url, data=json.dumps(put_data), headers=headers, verify='/path/to/ssl_certificate')
    status_code = r.status_code
    resp = r.text
    if (status_code == 200):
        #print("Put was successful...")
        json_resp = json.loads(resp)
        print "Done"
        #print(json.dumps(json_resp,sort_keys=True,indent=4, separators=(',', ': ')))
    else:
        r.raise_for_status()
        print("Status code:-->"+status_code)
        print("Error occurred in PUT --> "+resp)
except requests.exceptions.HTTPError as err:
    print ("Error in connection --> "+str(err))
finally:
    if r: r.close()

 

 
