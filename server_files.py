#!/usr/bin/env python
# -*- coding=utf-8 -*-


"""
file: recv.py
socket service
"""


import socket
import threading
import time
import sys
import os, shutil
import struct
from time import sleep


def build_struct(struct_list):
    print 'Start to build directory struction. '
    root = os.getcwd()
    print root
    for path in struct_list:
        path_dir = path.split('/')
        os.chdir(root)
        for i in path_dir[1:-1]:
            if not os.path.isdir(i):
                os.mkdir(i)
            os.chdir(os.path.join(os.getcwd(), i))
    os.chdir(root)
    

def move_files(struct_list):
    print 'Start to move files. '
    root = os.getcwd()
    for path in struct_list:
        current_path = os.path.join(root, path.split('/')[-1][:-1])
        shutil.move(current_path, path[:-1])


def deal_data(conn, addr):
    print 'Accept new connection from {0}'.format(addr)
    #conn.settimeout(500)
    conn.send('Hi, Welcome to the server!')

    while 1:
        fileinfo_size = struct.calcsize('128sl')
        buf = conn.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128sl', buf)
            fn = filename.strip('\00')
            new_filename = os.path.join('./', '' + fn)
            print 'file new name is {0}, filesize if {1}'.format(new_filename,
                                                                 filesize)

            recvd_size = 0  # 定义已接收文件的大小
            fp = open(new_filename, 'wb')
            print 'start receiving...'

            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = conn.recv(1024)
                    recvd_size += len(data)
                else:
                    data = conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            print 'end receive...'
            print ''
        conn.close()
        break

def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', 6666))
        # s.bind(('127.0.0.1', 6666))
        s.listen(10)
    except socket.error as msg:
        print msg
        sys.exit(1)
    print 'Waiting connection...'

    conn, addr = s.accept()
    deal_data(conn, addr)
    
    struct_list = []
    with open('struct.txt', 'r') as f:
        for i in f:
            if i == '': break
            struct_list.append(i)

    print struct_list

    for i in range(len(struct_list)-1):
    # while 1:
        # if os.path.isfile('over.txt'): 
        #     break
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()

    build_struct(struct_list)  
    move_files(struct_list)

    print 'start to delete cache. '  
    os.remove('./struct.txt')
    # os.remove('./over.txt')

if __name__ == '__main__':
    socket_service()