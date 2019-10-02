#!/usr/bin/env python3

import pyotp
import requests
import base64
import json
import sys

if len(sys.argv) < 2:
    print("Usage: python duo_activate.py <url to duo qr>")
    sys.exit()

qr_url = sys.argv[1]

host = 'api-%s' % (qr_url.split('/')[2].split('-')[1],)
code = qr_url.rsplit('/qr?value=',1)[1].split('-')[0]

url = 'https://{host}/push/v2/activation/{code}?customer_protocol=1'.format(host=host, code=code)
print("url", url)
headers = {'User-Agent': 'okhttp/2.7.5'}
data = {'jailbroken': 'false',
        'architecture': 'armv7',
        'region': 'NL',
        'app_id': 'com.duosecurity.duomobile',
        'full_disk_encryption': 'true',
        'passcode_status': 'true',
        'platform': 'Android',
        'app_version': '3.29.1',
        'app_build_number': '329101',
        'version': '10.0',
        'manufacturer': 'unknown',
        'language': 'en',
        'model': 'Command line',
        'security_patch_level': '2019-10-01'}

r = requests.post(url, headers=headers, data=data)
response = json.loads(r.text)

try:
  secret = base64.b32encode(response['response']['hotp_secret'].encode("UTF-8"))
except KeyError:
  print(response)
  sys.exit(1)

print("secret", secret)

f = open('duotoken.hotp', 'w')
f.write(secret.decode("UTF-8"))
f.write("\n0")
f.close()

with open('response.json', 'w') as resp:
    resp.write(r.text)
