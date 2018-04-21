HTTPSync
========

## Usage
```
usage: httpsync [-h] --url URL [--mirrors [MIRRORS [MIRRORS ...]]]
                [--exclude [EXCLUDE [EXCLUDE ...]]] --directory DIRECTORY
                [--delete] [--verbose] [--daemon]
                [--daemon-delay DAEMON_DELAY] [--cache-file CACHE_FILE]
                [--version]

HTTP Based Mirroring Tool

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     URL of site to mirror
  --mirrors [MIRRORS [MIRRORS ...]], -m [MIRRORS [MIRRORS ...]]
                        List of mirrors to attempt the download
  --exclude [EXCLUDE [EXCLUDE ...]], -e [EXCLUDE [EXCLUDE ...]]
                        String to exclude
  --directory DIRECTORY, -d DIRECTORY
                        Directory to store files
  --delete              Delete files no longer in the server
  --verbose, -v         Verbose output
  --daemon, -D          Run as a daemon
  --daemon-delay DAEMON_DELAY
                        Seconds of delay between each run
  --cache-file CACHE_FILE, -c CACHE_FILE
                        Path to job cache file
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
