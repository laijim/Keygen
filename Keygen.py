#! /usr/bin/python3
import os
import socket
import hashlib
import struct
import sys
from pathlib import Path

hostid=os.popen("hostid").read().strip()
hostname = socket.gethostname()
ioukey=int(hostid,16)
for x in hostname:
 ioukey = ioukey + ord(x)

maxInt = 2 ** (struct.calcsize("i") * 8 - 1) - 1
if(ioukey > maxInt):
  print("\033[31m Your hostid " + hostid + " is too max. You can use sethostid command change to a smaller one.(less than 4 byte int) \033[0m")
  sys.exit(1)

print("This is your machine info hostid=" + hostid +", hostname="+ hostname + ", ioukey=" + hex(ioukey)[2:])

iouPad1 = b'\x4B\x58\x21\x81\x56\x7B\x0D\xF3\x21\x43\x9B\x7E\xAC\x1D\xE6\x8A'
iouPad2 = b'\x80' + 39*b'\0'
md5input=iouPad1 + iouPad2 + struct.pack('!i', ioukey) + iouPad1
iouLicense=hashlib.md5(md5input).hexdigest()[:16]

home = str(Path.home())
rcFile = home + "/.iourc"
iourc = "[license]\n" + hostname + " = " + iouLicense + ";\n"

fd = None
try:
    fd = open(rcFile, "wt")
    fd.write(iourc)

    print("\033[32m License info: \033[0m")
    print("\033[32m " + iourc + " \033[0m")
    print("\033[32m Writed to : " + rcFile +  " \033[0m")
except:
    print("\033[31m Write licence info fail, You can set it by your self \033[0m")
    print("\033[31m " + iourc + " \033[0m")

finally:
    if fd != None:
      fd.close()


