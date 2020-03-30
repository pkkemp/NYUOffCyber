#import from py
import re
from collections import Counter

#outside imports
from pwn import *

#used for pulling the flag from output
flag_regex = r"flag\{[^}]+\}"
global_timeout = 5 #seconds

#challenge-specific info
host = 'offsec-chalbroker.osiris.cyber.nyu.edu'
port = 1250
netid='pk1898'

do_remote = False
binary_name = './dora'

#for doing local debugging
is_local_dbg = True
gdb_script = '''
set pagination off
set disassembly-flavor intel
i proc mappings
b *0x004008dd
c
'''

#universal flag finder, given a string
def find_flag(input):
    m = re.findall(flag_regex, input)
    if(m != []):
        return m[0]
    else:
        return None


#some address
read_flag = '974623344d8ac47e7c7c7c737997472234f5bbc6837c7c7cc47c7c7c7c7379c37d7c7c7cc6837c7c7cc47d7c7c7c7379c37c7c7c7cc4407c7c7c737994bd8383831a101d1b520804087c94bc83838300'.decode('hex')
def most_frequent():
    most_frequent_byte = Counter(read_flag).most_common(1)[0][0]
    return ord(most_frequent_byte)

def solve(target):
    for x in range(1):
        print 'discarded: %s' % target.readline()
    most_frequent_byte = most_frequent()
    print 'Most frequent byte: 0x%X' % most_frequent_byte
    target.sendline(str(most_frequent_byte))
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
