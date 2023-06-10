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

from .utils import *

def purge_directory(folder, accepted_file_types, secure):
    """traverse a directory and purge all selected files"""
    
    threads = []
    
    for root, dirs, files in os.walk(folder):
        thread = threading.Thread(
                target=purge_file,
                args=(files,secure,root,accepted_file_types)
                )

        thread.start()

        threads.append(thread)
        
    for thread in threads:
        thread.join()
        
def decrypt_directory(folder,delete,secure,seperate,key):
    """traverse a directory and decrypt files"""
    
    threads = []
    
    for root, dirs, files in os.walk(folder):
        if (not os.path.exists(root+"/raw") and seperate and root[-3:] != "raw" and len(files) != 0):
            os.mkdir(root+"/raw")
        if not seperate and os.path.exists(os.path.join(root+"/raw")):
            os.rmdir(os.path.join(root+"/raw"))
        thread = threading.Thread(
                target=decrypt_batch,
                args=(files, delete, seperate, secure, root, key)
                )
        thread.start()

        threads.append(thread)

    for thread in threads:
        thread.join()
        
def encrypt_directory(folder,delete,secure,backup,key):
    """encrypt all files in a directory"""
    
    threads = []
    
    for root, dirs, files in os.walk(folder):
        thread = threading.Thread(
                target=encrypt_batch,
                args=(files, root, backup, delete, secure, key)
                )
        thread.start()

        threads.append(thread)

    for thread in threads:
        thread.join()
        
def obscure_directory(folder):
    """randomises file names in a dir"""

    threads = []
    
    for root, dirs, files in os.walk(folder):
        files = sorted(files) 
        thread = threading.Thread(
                target=obscure_file,
                args=(root,files)
                )

        thread.start()

        threads.append(thread)
        
    for thread in threads:
        thread.join()

def swap_file_extensions(folder,swap_from,swap_to):
    """traverses a dir, swapping selected file names"""
    files_swapped = 0
    for root, dirs, files in os.walk(folder):
        for file in files:
            name, ext = os.path.splitext(file)

            if (ext not in [swap_from,".aes"]):
                continue

            if (ext == ".aes" and name.split(".")[1] == swap_from[1:]):
                newname = name[:-4] + swap_to + ".aes"

            elif (ext == swap_from):
                newname = name + swap_to

            else:
                continue

            os.rename(os.path.join(root, file), os.path.join(root, newname))
            
