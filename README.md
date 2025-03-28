# ILA - Lightweight Version Control

ILA is a lightweight version control system written in Python, designed for seamless synchronization between your local machine and a remote SSH server. Unlike traditional version control systems like Git, ILA is designed to work completely offline without the need for a public central repository server. It enables peer-to-peer synchronization, making it ideal for private projects that do not require a centralized public server.

## Key Features
- **Initialize a Repository**: Set up a new repository and configure the connection.
- **Commit Changes**: Create and commit changes with messages.
- **Log History**: View commit history to track changes over time.
- **Clone Repository**: Clone a repository from a remote server.
- **Pull Updates**: Sync and update your local repo with the latest changes from the master.
- **Offline**: No need for a public server. Everything stays within your control.

## Upcoming Features
**1. Push**: Ability to push code from local instances to remote server.
**2. Branching**: Creating and working on mulitple branches.
**3. Conflit Resolution**: Solving merging conflicts.

## Installation
To get started with ILA, follow these steps:

1. Clone this repository or download the source code.
```bash
$ git clone https://github.com/your-username/ila.git
$ cd ila
```

2. Install the required dependencies (if any). 
```bash
$ pip install -r requirements.txt
```

3. Run the ILA commands using Python.
```bash
$ python main.py [command]
```

## Using ILA as a Command
To use `ila` as a command instead of running `python main.py`, follow these steps:

### Windows
1. Create a `ila.bat` file with the following content:
```batch
@echo off
python path\to\main.py %*
```
2. Add the directory containing `ila.bat` to your system `PATH` variable.

### Linux/Mac
1. Create a `ila.sh` file with the following content:
```bash
#!/bin/bash
python /path/to/main.py "$@"
```
2. Make the script executable:
```bash
$ chmod +x /path/to/ila.sh
```
3. Add the script to your `~/.bashrc` or `~/.bash_profile`:
```bash
export PATH=$PATH:/path/to/ila.sh
```
4. Reload the shell configuration:
```bash
$ source ~/.bashrc
```

## Usage

### 1. Initialize a Repository
```bash
$ ila --init [repo_name]
```
This creates a `.ila` directory to manage the repository.

- To initialize with a remote server:
```bash
$ ila --init [repo_name] -r
```

### 2. Commit Changes
```bash
$ ila --commit "Commit message"
```
Commits the current state with a message and updates the `HEAD`.

### 3. View Commit History
```bash
$ ila --log
```
Displays a list of previous commits.

### 4. Clone a Repository
```bash
$ ila --clone [path/to/remote]
```
Clones the repository to the specified path.

### 5. Pull Updates from Master
```bash
$ ila --pull
```
Updates your local repository with the latest changes from the master instance.

## Configuration
ILA uses a `config.json` file located in the `.ila` directory to store the repository configuration.

## Contributing
If you'd like to contribute to ILA, feel free to fork the repository, submit pull requests, or report issues.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact
For any questions or issues, feel free to reach out to [anand.tushar2010@gmail.com](mailto:anand.tushar2010@gmail.com).

