import requests
import json

vmanage_host = input("vManage IP or FQDN:")
username = input("vManage Username:")
password = input("vManage Password:")

url = "https://{}/j_security_check".format(vmanage_host)

payload="j_username={}&j_password={}".format(username,password)
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

if response.text.startswith('<html>'):
    print("Could not login to device, check user creds")
    exit()
if response.status_code == 200:
    cookie = response.cookies

url = "https://{}:443/dataservice/template/device".format(vmanage_host)
payload = {}
headers = {
}

response = requests.request("GET", url, cookies=cookie, headers=headers, data=payload, verify=False)

print("Retrieved list of device templates.")
print("Raw Data:")
print(response.json())
device_body = response.json()


for device in device_body['data']:

    url = "https://{}:443/dataservice/template/device/object/{}".format(vmanage_host, device['templateId'])
    payload = {}
    headers = {
    }
    object_response = requests.request("GET", url, cookies=cookie, headers=headers, data=payload, verify=False)
    if object_response.json():
        object = object_response.json()
        print("Retrieved template name {}, template ID {}".format(object['templateName'], object['templateId']))
