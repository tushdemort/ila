import os
import json
import shutil
import subprocess
from macros import MAIN, CFG, OBJECTS_DIR
from log import readObj
from tree import restoreTree

VC_DIR = os.path.dirname(__file__)

def pull_from_master():
    cfg_path = os.path.join(MAIN, CFG)
    if not os.path.exists(cfg_path):
        raise SystemExit("No config found.")

    with open(cfg_path) as f:
        config = json.load(f)

    if config.get("remote", False):
        raise SystemExit("This is a master repo. Pull not allowed.")

    master_path = config.get("master_path")
    if not master_path:
        raise SystemExit("No master_path set in config.")

    is_ssh = False

    # Detect SSH format
    if master_path.startswith("ssh://"):
        is_ssh = True
        user_host, remote_path = master_path[6:].split(":", 1)

    elif ":" in master_path:
        # Format: alias:/remote/path
        alias, remote_path = master_path.split(":", 1)
        hosts_path = os.path.join(VC_DIR, 'ila_hosts.json')

        if not os.path.exists(hosts_path):
            raise SystemExit("ila_hosts.json not found.")

        with open(hosts_path) as f:
            host_map = json.load(f)

        if alias not in host_map:
            raise SystemExit(f"Alias '{alias}' not found in ila_hosts.json.")

        user_host = host_map[alias]
        is_ssh = True

    if is_ssh:
        remote_ila = os.path.join(remote_path, MAIN).replace('\\', '/')

        # Ensure .ila/objects exists locally
        os.makedirs(OBJECTS_DIR, exist_ok=True)

        # Pull updated HEAD
        subprocess.run(['scp', f'{user_host}:{remote_ila}/HEAD', os.path.join(MAIN, 'HEAD')], check=True)

        # Pull any new objects (you can optimize this later)
        subprocess.run(['scp', f'{user_host}:{remote_ila}/objects/*', os.path.join(OBJECTS_DIR)], check=True)

    else:
        # Local master
        master_ila = os.path.join(master_path, MAIN)
        if not os.path.exists(master_ila):
            raise SystemExit("Master repo not found.")

        # Copy HEAD
        shutil.copy(os.path.join(master_ila, 'HEAD'), os.path.join(MAIN, 'HEAD'))

        # Copy new objects
        for oid in os.listdir(os.path.join(master_ila, 'objects')):
            src = os.path.join(master_ila, 'objects', oid)
            dst = os.path.join(OBJECTS_DIR, oid)
            if not os.path.exists(dst):
                shutil.copy(src, dst)

    # Restore latest snapshot
    with open(os.path.join(MAIN, 'HEAD')) as f:
        commit_hash = f.read().strip()

    commit_data = readObj(commit_hash).decode()
    meta, _ = commit_data.split('\msg')
    tree_hash = ''
    for line in meta.split('\n'):
        if line.startswith('tree '):
            tree_hash = line[5:]

    restoreTree(tree_hash, '.')
    print("Pulled latest snapshot from master.")
