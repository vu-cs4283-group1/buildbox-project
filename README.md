# buildbox-project
This is very similar to Travis-CI, except it is hosted on computers of one’s choice instead of the cloud. 
Since much of the work is done by running utility programs, we attempted to implement our own remote syncing of files and directories over TCP, much like the Unix utility rsync except cross-platform.

## Dependencies
* Python3.6
* socket
* textwrap
* threading
* json
* os
* shlex
* subprocess
* time
* hashlib
* argparse

## Quick start
Run the Server first then the Client.
Also, this is assuming you are running on the same machine

### Server
```
python buildbox.py server
```

### Client
```
python buildbox.py client 127.0.0.1 --root buildtest
```

## Important Tips
* buildbox.py is the wrapper class, so both the server and client runs on buildbox.py.
* As you can see in the Quick Start section, you can simply add the word server/client as the first argument to run the server/client.
* The second argument when running the client represents the host running buildbox in server mode (ex. 127.0.0.1)

## Server arguments
```
python buildbox.py server -q
```
Suppress output information. Identical to --quiet
```
python buildbox.py server -f buildbox.json
```
The JSON config file to use (default buildbox.json). Identical to --file

## Client arguments
```
python buildbox.py client 127.0.0.1 -r buildtest
```
The directory to synchronize (default .). Identical to --root
```
python buildbox.py client 127.0.0.1 -q
```
Suppress output information. Identical to --quiet
```
python buildbox.py client 127.0.0.1 -d
```
Do not alter the server's state. Identical to --dry-run
```
python buildbox.py client 127.0.0.1 -n
```
Synchronize files but do not run commands. Identical to --no-build

## Authors
* Josh Wilson
* Bumsu(Jerry) Jung
* Caleb Proffitt

