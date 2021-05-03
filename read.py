#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyaes

# Encrypted
def Read(filename):
    key = b'\x03jN\x10\xed\xac\xfb\x92\xe2\xf1\x8a^\x15~\x98\xe0'
    aes = pyaes.AESModeOfOperationCTR(key)

    f2 = open(filename, "rb")

    data=[]

    lines = f2.readlines()
    decrypted=''
    for line in lines:
        #print(line)
        decrypted = decrypted + (aes.decrypt(line)).decode('utf8')
        print(decrypted)
    f2.close()

    data=decrypted.split(";\n")
    n=len(data)
    for i in range(n):

        print(data[i])
        data[i] = data[i].split(":")
        print(data[i])
        #data[i]=data[i].encode('ansi','ignore').decode('utf8','strict').split(":")

    return data


