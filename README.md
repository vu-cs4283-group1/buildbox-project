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
Run the Server first then the Client

### Server
```
python buildbox.py server
```

### Client
```
python buildbox.py client 127.0.0.1 --root buildtest
```

## Arguments
### Server
* -q OR --quiet
⋅⋅⋅Suppress output information
* -f OR --file XXX.json
⋅⋅⋅the JSON config file to use (default buildbox.json)

### Client
* -r OR --root XXX
⋅⋅⋅The directory to synchronize (default .)
* -q OR --quiet
⋅⋅⋅Suppress output information
* -d OR --dry-run
⋅⋅⋅Do not alter the server's state
* -n OR --no-build
⋅⋅⋅Synchronize files but do not run commands

## Authors
* Josh Wilson
* Bumsu(Jerry) Jung
* Caleb Proffitt

