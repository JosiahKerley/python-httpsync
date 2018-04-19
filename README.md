HTTPSync
========

## Usage
```
usage: httpsync [-h] --url URL [--mirrors [MIRRORS [MIRRORS ...]]] --directory
                DIRECTORY [--max-depth MAX_DEPTH] [--delete] [--verbose]
                [--daemon] [--daemon-delay DAEMON_DELAY] [--version]

HTTP Based Mirroring Tool

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     URL of site to mirror
  --mirrors [MIRRORS [MIRRORS ...]], -m [MIRRORS [MIRRORS ...]]
                        List of mirrors to attempt the download
  --directory DIRECTORY, -d DIRECTORY
                        Directory to store files
  --max-depth MAX_DEPTH, -M MAX_DEPTH
                        Maximum depth to traverse
  --delete              Delete files no longer in the server
  --verbose, -v         Verbose output
  --daemon, -D          Run as a daemon
  --daemon-delay DAEMON_DELAY
                        Seconds of delay between each run
  --version             show program's version number and exit
```


## Examples
### Mirroring a yum repo
```
httpsync -d /tmp/repo -u http://centos.unixheads.org/7/os/x86_64/
```

### Mirroring a yum repo and deleting older files
```
httpsync -d /tmp/repo -u http://centos.unixheads.org/7/os/x86_64/ --delete
```

### Balanced mirroring across multiple sources
```
httpsync -d /tmp/repo -u http://centos.unixheads.org/7/os/x86_64/ -m http://centos.host-engine.com http://centos.den.host-engine.com
```
