#!/usr/bin/env python
# -*- coding=utf-8 -*-


"""
file: send.py
socket client
"""

import socket
import os
import sys
import struct
from time import sleep
import args

server_dir = "127.0.0.1"
server_dir = "123.206.83.254"
port = 6666

def socket_client(filepath):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_dir, port))
    except socket.error as msg:
        print msg
        sys.exit(1)

    print s.recv(1024)

    while 1:
        # filepath = raw_input('please input file path: ')
        if os.path.isfile(filepath):
            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            fileinfo_size = struct.calcsize('128sl')
            # 定义文件头信息，包含文件名和文件大小
            fhead = struct.pack('128sl', os.path.basename(filepath),
                                os.stat(filepath).st_size)
            s.send(fhead)
            print 'client filepath: {0}'.format(filepath)

            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(1024)
                if not data:
                    print '{0} file send over...'.format(filepath)
                    break
                s.send(data)
        s.close()
        break

def dir_struct(current_dir):
    with open('struct.txt', 'w') as f:
        f.write('')
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file[0] == '.': continue
            file_dir = os.path.join(root, file)
            with open('struct.txt', 'a') as f:
                f.write(file_dir + '\n')
    try:
        socket_client('./struct.txt')
    except Exception as e:
        print e


def sent_over():
    with open('over.txt', 'w') as f:
        f.write('')
    try:
        socket_client('./over.txt')
    except Exception as e:
        print e
    os.remove('over.txt')
    

if __name__ == '__main__':
    current_dir = "./"
    dir_struct(current_dir)
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file == 'struct.txt': continue
            if file[0] == '.': continue
            imagesDir = []
            imagesDir.append(os.path.join(root, file))
            print(imagesDir)
            print ''

            for filepath in imagesDir:
                try:
                    socket_client(filepath)
                except Exception as e:
                    print(e)
                    continue
    sleep(1)
    # sent_over()
    os.remove('struct.txt')