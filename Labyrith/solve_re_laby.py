#import from py
import re

#outside imports
from pwn import *

#used for pulling the flag from output
flag_regex = r"flag\{[^}]+\}"
global_timeout = 5 #seconds

#challenge-specific info
host = 'offsec-chalbroker.osiris.cyber.nyu.edu'
port = 1253
netid='pk1898'

do_remote = False
binary_name = './labyrinth'

#for doing local debugging
is_local_dbg = True
gdb_script = '''
set pagination off
set disassembly-flavor intel
i proc mappings
b *0x004008ec
'''

#universal flag finder, given a string
def find_flag(input):
    m = re.findall(flag_regex, input)
    if(m != []):
        return m[0]
    else:
        return None


#some address
solution = 0x00400938
def solve(target):
    for x in range(200000):
        print(target.readline())
        print(target.sendline(str(x)))
        try:
            print(target.readline())
        except:
            print("An exception occurred")
    return target.readline()


#universal target setup for remote-only
def target():
    if(do_remote):
        r = remote(host, port)
        r.sendline(netid)
        r.recvline() # eat interstitial
        return r
    else:
        if(is_local_dbg):
            target = gdb.debug(binary_name, gdb_script)
        else:
            target = process(binary_name)
        return target

#scaffolding
def main():
    with target() as p:
        flag = solve(p)
    if(flag):
        print("Challenge Solved: %s" % flag)
    else:
        print("Challenge Not Solved")

if __name__ == '__main__':
    main()
