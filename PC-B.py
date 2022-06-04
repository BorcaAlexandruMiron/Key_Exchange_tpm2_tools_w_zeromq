#!/usr/bin/env python3

import time
import zmq
import subprocess,sys
import os

context = zmq.Context()
r = input("Ip Adress of the other device:")
#  Socket to talk to server
socket = context.socket(zmq.REQ)
connection="tcp://{}:5555".format(r)
socket.connect(connection)
try:
    result=subprocess.run(["tpm2_createprimary","-c","primary.ctx"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
except Exception as e:
    print("duck")

try:
    result=subprocess.run(["tpm2_readpublic", "-c","primary.ctx", "-o", "primary.pub"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
except Exception as e:
    print("duck")

target=open('primary.pub','rb')
size=os.stat('primary.pub').st_size

file=target.read(size)

if file:
    socket.send(file)

message = socket.recv()
if message:
    f = open('rsa.pub', 'wb')
    f.write(message)
    f.close()
socket.send(b'1')
message = socket.recv()
if message:
    f = open('rsa.dpriv', 'wb')
    f.write(message)
    f.close()
socket.send(b'1')
message = socket.recv()
if message:
    f = open('rsa.seed', 'wb')
    f.write(message)
    f.close()
socket.send(b'1')   
try:
    result=subprocess.run(["tpm2_import","-C","primary.ctx","-G","rsa","-i","rsa.dpriv","-s","rsa.seed","-u","rsa.pub","-r","rsa.priv"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
except Exception as e:
    print("duck")
try:
    result=subprocess.run(["tpm2_load","-C", "primary.ctx", "-c", "rsa.ctx", "-u", "rsa.pub", "-r", "rsa.priv"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
except Exception as e:
    print("duck")    
 
message = socket.recv()
if message:
    f = open('msg.enc', 'wb')
    f.write(message)
    f.close()
try:
    result=subprocess.run(["tpm2_load", "-C", "primary.ctx", "-u", "rsa.pub", "-r","rsa.priv","-c","rsa.ctx"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
except Exception as e:
    print("duck")   
try:
    result=subprocess.run(["tpm2_rsadecrypt", "-c", "rsa.ctx", "-o", "msg.ptext", "msg.enc"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
except Exception as e:
    print("duck")   
with open('msg.ptext', 'r') as f:
    print("Plain text:")
    print(f.read())