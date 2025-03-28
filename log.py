from macros import MAIN,OBJECTS_DIR
import os
from datetime import datetime


def readObj(oID):
    path = os.path.join(OBJECTS_DIR, oID)
    with open(path, 'rb') as f:
        data = f.read()

    nullIdx = data.find(b'\0')
    return data[nullIdx + 1:]

def showLog():
    head_path=os.path.join(MAIN,'HEAD')
    if not os.path.exists(head_path):
        raise SystemExit("No commits found.")
    oID = open(head_path).read().strip()
    while oID:
        commitData = readObj(oID).decode()
        # lines = commitData.split('\n')
        try:
            meta, message = commitData.split('\msg')
        except ValueError:
            meta = commitData
            message = "(no message)"
        tree=''
        parent=''
        author=''        
        i=0;
        for line in meta.split('\n'):
            # print(line)
            if line.startswith('tree '):
                tree = line[5:]
            elif line.startswith('parent '):
                parent = line[7:]
            elif line.startswith('author '):
                parts = line[7:].split()
                timestamp = int(parts[-1])
                author = ' '.join(parts[:-1])
                time_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        print(f'Commit: {oID}')
        print(f'Tree: {tree}')
        if parent:
            print(f'Parent: {parent}')
        print(f'Author: {author}')
        print(f'Date: {time_str}')
        print(f'Message:  {message.strip()}')
        print('-' * 40)


        oID = parent
