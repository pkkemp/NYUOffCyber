import base64

def woah(s1,s2): #part of pass 3
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

def solvePass3():
    flag = b'HxEMBxUAURg6I0QILT4UVRolMQFRHzokRBcmAygNXhkqWBw='
    key = "meownyameownyameownyameownyameownya"
    a = base64.b64decode(flag, altchars=None)
    b = a.decode()
    print(woah(key, b))

def main():
    solvePass3()

main()


