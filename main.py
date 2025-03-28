#Python imports
import os
import argparse
import sys
import json

#My imports
from tree import makeTree
from macros import MAIN,CFG,OBJECTS_DIR
from commit import commit_tree
from log import showLog, readObj
from clone import clone_repo
from sync import pull_from_master

#Macros
MAIN = '.ila'
CFG = 'config.json'
OBJECTS_DIR = os.path.join(MAIN, 'objects')


sys.tracebacklimit=None
parser = argparse.ArgumentParser()

#Commands
parser.add_argument('--init',type=str,help="Used to initialize a connection")
parser.add_argument('--snapshot', action='store_true', help="Snapshot current working directory")
parser.add_argument('--commit', type=str, help="Commit snapshot with message")
parser.add_argument('--log', action='store_true', help="Show commit history")
parser.add_argument('--clone', type=str, help="Clone the repo to a given path")
parser.add_argument('--pull', action='store_true', help="Update from master")


#config
parser.add_argument('-r', '--remote', action='store_true', help="Used to initialize a connection")

args = parser.parse_args()





if(args.init):
    if(not os.path.exists(MAIN) or not os.path.exists(f'/{MAIN}/{CFG}')):
        config={"name":args.init,"remote":args.remote}
        try:
            os.mkdir(MAIN)
        except:
            pass
        with open(f'{MAIN}/{CFG}', 'w') as f:
            json.dump(config,f)
        raise SystemExit("Connection created")
        
    else:
        raise SystemExit("Connection already created")

if(args.snapshot):
    if not os.path.exists(f'{MAIN}/{CFG}'):
        raise SystemExit("Repo not initialized. Run with --init first.")
    
    if not os.path.exists(OBJECTS_DIR):
        os.mkdir(OBJECTS_DIR)

    tree_hash = makeTree('.')
    print("Snapshot created. Tree hash:", tree_hash)
    raise SystemExit()

if args.commit:
    if not os.path.exists(f'{MAIN}/{CFG}'):
        raise SystemExit("Repo not initialized. Run with --init first.")
    
    if not os.path.exists(OBJECTS_DIR):
        os.mkdir(OBJECTS_DIR)

    tree_hash = makeTree('.')

    # Get last commit hash if exists
    head_path = os.path.join(MAIN, 'HEAD')
    parent = None
    if os.path.exists(head_path):
        with open(head_path) as f:
            parent = f.read().strip()

        # Read last commit and check tree hash
        last_commit_data = readObj(parent).decode()
        try:
            meta, _ = last_commit_data.split('\msg')
        except ValueError:
            meta = last_commit_data
        for line in meta.split('\n'):
            if line.startswith('tree '):
                last_tree_hash = line[5:]
                if last_tree_hash == tree_hash:
                    raise SystemExit("No changes to commit. Latest version already committed.")

    commit_hash = commit_tree(tree_hash, args.commit, parent)

    # Save new HEAD
    with open(head_path, 'w') as f:
        f.write(commit_hash)

    print("Commit created:", commit_hash)
    raise SystemExit()

if args.log:
    showLog()
    raise SystemExit()

if args.clone:
    clone_repo(args.clone)
    raise SystemExit()

if args.pull:
    pull_from_master()
    raise SystemExit()