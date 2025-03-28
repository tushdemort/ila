import os
import shutil
import json
from log import readObj
from macros import MAIN, CFG
from tree import restoreTree
import subprocess

VC_DIR = os.path.dirname(__file__)


def clone_repo(source):
    is_ssh = False

    if source.startswith("ssh://"):
        is_ssh = True
        user_host, remote_path = source[6:].split(":", 1)

    elif ":" in source:
        # Format: alias:/remote/path
        alias, remote_path = source.split(":", 1)
        hosts_path = os.path.join(VC_DIR, 'ila_hosts.json')

        if not os.path.exists(hosts_path):
            raise SystemExit("ila_hosts.json not found in VC folder.")

        with open(hosts_path) as f:
            host_map = json.load(f)

        if alias not in host_map:
            raise SystemExit(f"Alias '{alias}' not found in ila_hosts.json.")

        user_host = host_map[alias]
        is_ssh = True


    if is_ssh:
        # Parse ssh://user@host:/path/to/repo
        remote_ila = os.path.join(remote_path, MAIN)
        print(user_host)
        # Create local .ila folder
        if os.path.exists(MAIN):
            raise SystemExit("This folder is already a repo.")

        os.makedirs(MAIN)
        os.makedirs(os.path.join(MAIN, 'objects'))
        remote_ila = os.path.join(remote_path, MAIN).replace('\\', '/')
        # Copy config.json and HEAD from remote
        subprocess.run(['scp', f'{user_host}:{remote_ila}/{CFG}', os.path.join(MAIN, CFG)], check=True)
        subprocess.run(['scp', f'{user_host}:{remote_ila}/HEAD', os.path.join(MAIN, 'HEAD')], check=True)

        # Copy all objects
        remote_objects = f'{user_host}:{remote_ila}/objects/*'
        local_objects = os.path.join(MAIN, 'objects')
        subprocess.run(['scp', remote_objects, local_objects], check=True)

        # Set master_path to remote
        with open(os.path.join(MAIN, CFG), 'r+') as f:
            cfg = json.load(f)
            cfg['remote'] = False
            cfg['master_path'] = source
            f.seek(0)
            json.dump(cfg, f)
            f.truncate()

    else:
        # Local clone (as before)
        source_ila = os.path.join(source, MAIN)
        if not os.path.exists(os.path.join(source_ila, CFG)):
            raise SystemExit("Invalid source repo.")

        if os.path.exists(MAIN):
            raise SystemExit("This folder is already a repo.")

        shutil.copytree(source_ila, MAIN)

        # Overwrite config
        with open(os.path.join(MAIN, CFG), 'r+') as f:
            cfg = json.load(f)
            cfg['remote'] = False
            cfg['master_path'] = os.path.abspath(source)
            f.seek(0)
            json.dump(cfg, f)
            f.truncate()

    # Restore working directory from latest commit
    with open(os.path.join(MAIN, 'HEAD')) as f:
        commit_hash = f.read().strip()

    commit_data = readObj(commit_hash).decode()
    meta, _ = commit_data.split('\msg')
    tree_hash = ''
    for line in meta.split('\n'):
        if line.startswith('tree '):
            tree_hash = line[5:]

    restoreTree(tree_hash, '.')

    print(f"Cloned from {'remote' if is_ssh else 'local'} repo: {source}")
