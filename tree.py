#make sync redundant
import os
from fileHash import hashObj
from log import readObj

def makeTree(path='.'):
    entries=[]
    for entry in sorted(os.listdir(path)):
        entryPath = os.path.join(path,entry)

        if '.ila' in entryPath or '__pycache__' in entryPath:
            continue
        
        if os.path.isfile(entryPath):
            with open(entryPath, 'rb') as f:
                data = f.read()
            oid = hashObj(data)
            mode = '100644'
        elif os.path.isdir(entryPath):
            oid = makeTree(entryPath) 
            mode = '40000'
        else:
            continue

        entries.append(f'{mode} {entry}\0'.encode() + bytes.fromhex(oid))

    tree_data = b''.join(entries)
    return hashObj(tree_data, 'tree')



def restoreTree(tree_hash, target_path):
    tree_data = readObj(tree_hash)
    i = 0
    expected_paths = []

    # Parse all entries in the tree
    while i < len(tree_data):
        space_idx = tree_data.find(b' ', i)
        null_idx = tree_data.find(b'\0', space_idx)
        mode = tree_data[i:space_idx].decode()
        name = tree_data[space_idx + 1:null_idx].decode()
        oid = tree_data[null_idx + 1:null_idx + 21].hex()
        i = null_idx + 21

        full_path = os.path.join(target_path, name)
        expected_paths.append(full_path)

        if mode == '100644':
            blob = readObj(oid)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'wb') as f:
                f.write(blob)
        elif mode == '40000':
            os.makedirs(full_path, exist_ok=True)
            restoreTree(oid, full_path)

    # Delete any unexpected files/directories
    for path, dirs, files in os.walk(target_path, topdown=False):
        for name in files:
            file_path = os.path.join(path, name)
            if file_path not in expected_paths:
                if '.ila' not in file_path:
                    os.remove(file_path)
        for name in dirs:
            dir_path = os.path.join(path, name)
            if dir_path not in expected_paths and not os.listdir(dir_path):
                if '.ila' not in dir_path:
                    os.rmdir(dir_path)
