import time
from fileHash import hashObj

def commit_tree(tree_hash,message,parent=None):
    lines=[]
    # print(message)
    lines.append(f'tree {tree_hash}')
    if parent:
        lines.append(f'parent {parent}')
    lines.append(f'author you {int(time.time())}')
    lines.append("\msg")
    lines.append(message)
    

    commit_data = '\n'.join(lines).encode()
    a= hashObj(commit_data,'commit')
    return a