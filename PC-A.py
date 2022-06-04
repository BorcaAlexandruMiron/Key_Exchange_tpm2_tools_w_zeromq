#!/usr/bin/env python3

import time
import zmq
import subprocess,sys
import os


filename = 'primary.pub'
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
message = socket.recv()
if message:
    f = open(filename, 'wb')
    f.write(message)
    f.close()
try:
    result=subprocess.run(["openssl", "genrsa", "-out", "rsa.pem"])
except Exception as e:
    print("duck")
try:
    result=subprocess.run(["tpm2_duplicate", "-U", "primary.pub", "-G", "rsa", "-k","rsa.pem", "-u", "rsa.pub", "-r", "rsa.dpriv", "-s", "rsa.seed"])
except Exception as e:
    print("duck")

target=open('rsa.pub','rb')
size=os.stat('rsa.pub').st_size
file=target.read(size)

if file:
    socket.send(file)
socket.recv()
target1=open('rsa.dpriv','rb')
size1=os.stat('rsa.dpriv').st_size

file1=target1.read(size1)

if file:
    socket.send(file1)
socket.recv()
target1=open('rsa.seed','rb')
size1=os.stat('rsa.seed').st_size

file1=target1.read(size1)

if file:
    socket.send(file1)
socket.recv()
try:
    result=subprocess.run(["tpm2_createprimary", "-G", "rsa", "-C", "o", "-c", "parent.ctx"])
except Exception as e:
    print("duck")
try:
    result=subprocess.run(["tpm2_import", "-C", "parent.ctx", "-G", "rsa", "-i", "rsa.pem", "-u", "imported.pub", "-r", "imported.priv"])
except Exception as e:
    print("duck")
try:
    result=subprocess.run(["tpm2_load", "-C", "parent.ctx", "-u", "imported.pub", "-r", "imported.priv", "-c", "imported.ctx"])
except Exception as e:
    print("duck")
os.system('cls' if os.name == 'nt' else 'clear')
encMsg=input("Encript this message:")
f=open('msg.dat','w')
f.write(encMsg)
f.close()
try:
    result=subprocess.run(["tpm2_rsaencrypt", "-c", "imported.ctx", "-o", "msg.enc", "msg.dat"])
except Exception as e:
    print("duck")
target=open('msg.enc','rb')
size=os.stat('msg.enc').st_size
file=target.read(size)
if file:
    socket.send(file)