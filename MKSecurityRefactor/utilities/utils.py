import subprocess 
import os
import time
import random
import math
import sys
import threading
import json
import tkinter as tk
import hashlib

def count_files(directory):
    """count files in a directory"""
    count = 0
    for root, dirs, files in os.walk(directory):
        count += len(files)
    return count

def count_folders(directory):
    """count folders in a directory"""
    count = 0
    for root, dirs, files in os.walk(directory):
        count += 1
    return count

def count_size(directory):
    """get file size of folder"""
    size = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            size += os.path.getsize(os.path.join(root,file))
    return size

def size_to_rational(size):
    """get size in understandable terms to gb"""
    gb_size = 1000000000
    mb_size = 1000000
    kb_size = 1000
    b_size = 1
    if (size > gb_size):
        return str(int(size / gb_size)) + "gb"
    elif (size > mb_size):
        return str(int(size / mb_size)) + "mb"
    elif (size > kb_size):
        return str(int(size / kb_size)) + "kb"
    elif (size > b_size):
        return str(int(size / b_size)) + "b"
    

def hash_md5(to_hash):
    """return hash to md5 standard"""
    res = hashlib.md5(to_hash.encode('utf-8'))
    return res.hexdigest()

def copy_file_to(source,destination):
    """copy the bytemap of a file elsewhere"""
    with open(source, 'rb') as read_file:
        with open(destination, 'wb') as write_file:
            for line in read_file:
                write_file.write(line)
                
            write_file.close()
            
        read_file.close()
        
def get_all_dirs(directory):
    """traverse current dir and return all dirs (folders)"""
    return  [file for file in os.listdir(directory) if os.path.isdir(file)]

def overwrite_data(file):
    """write a file with random bytemaps to prevent data recovery"""
    with open(file, 'wb') as f:
        f.write(os.urandom(os.path.getsize(file)))

        f.close()



def purge_file(files,secure,root,accepted_file_types):
    """purge a file and overwrite its contents before hand if selected"""
    for file in files:
        if (os.path.splitext(file)[1] not in accepted_file_types):
            continue
        
        try:
            if (secure):
                overwrite_data(os.path.join(root, file))

            os.remove(os.path.join(root, file))
            
        except:
            continue

def decrypt_batch(files, delete,seperate, secure, root, key):
    """call aes to decrypt files and delete plus overwrite afterwards if selected"""
    aescrypt_path = os.path.join(os.getenv('PROGRAMFILES'), 'AESCrypt', 'aescrypt.exe')
    for file in files:
        try:
            if (os.path.splitext(file)[1] != ".aes"):
                continue
            
            try:
                subprocess.run([aescrypt_path, '-d', '-p', key, os.path.join(root, file)])
            except Exception as E:
                print(f"failed to decrypt {file}.aes {E}")
                continue
            
            if (seperate and os.path.exists(os.path.join(root, file[:-4]))):
                copy_file_to(os.path.join(root, file[:-4]),os.path.join(root+"/raw",file[:-4]))
            
                if (secure):
                    overwrite_data(os.path.join(root, file[:-4]))

                os.remove(os.path.join(root, file[:-4]))

            if delete and (os.path.exists(os.path.join(root+"/raw",file[:-4])) or os.path.exists(os.path.join(root,file[:-4]))):
                if (secure):
                    overwrite_data(os.path.join(root,file))

                os.remove(os.path.join(root,file))
                
        except:
            continue
        
def encrypt_batch(files,root,backup,delete,secure,key):
    """encrypts a file and securely deletes original file if selected, also makes an encrypted backup"""
    aescrypt_path = os.path.join(os.getenv('PROGRAMFILES'), 'AESCrypt', 'aescrypt.exe')
    for file in files:
        if (os.path.splitext(file)[1] == ".aes"):
            continue
        
        try:
            subprocess.run([aescrypt_path, '-e', '-p', key, os.path.join(root, file)])
        except Exception as E:
            print(f"failed to create {file}.aes {E}")
            continue
        if 'raw' in root:
            copy_file_to(os.path.join(root, file) + ".aes",os.path.join(root[:-4],file) + ".aes")
            overwrite_data(os.path.join(root, file) + ".aes")
            os.remove(os.path.join(root, file) + ".aes")
            
        if backup:
            copy_file_to(os.path.join(root, file) + ".aes",os.path.join(appdata_directory,file) + ".aes")

        if delete and os.path.exists(os.path.join(root, file + ".aes")):
            if (secure):
                overwrite_data(os.path.join(root, file))

            os.remove(os.path.join(root, file))

def obscure_file(root,files):
    """randomises a file name"""
    for file in files:
        name, ext = os.path.splitext(file)

        _newname = ''.join(chr(random.randint(128, 512)) for _ in range(7))

        if len(name.split('.')) > 1:
            _newname += '.' + name.split('.')[1]

        _newname += ext

        newname = f"{files.index(file)}-{_newname}"
        
        os.rename(os.path.join(root, file), os.path.join(root, newname))
        
