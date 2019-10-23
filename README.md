# Snort Docker Image

This image is mainly for testing purposes. It has not been designed
for running Snort in a production/live environment.

## Building

This Docker image is currently not pushed to any registry, so it must
be built before use:

    make

## Usage

```
usage: run.py [-h] [-l DIR] [-i IFACE] [-r FILE] [-S FILE]

optional arguments:
  -h, --help            show this help message and exit
  -l DIR                Log directory (default=.)
  -i IFACE              Interface to listen on
  -r FILE               PCAP file to read
  -S FILE, --rules FILE
                        Rule file to load (default empty)
```

## Example

To run Snort over a pcap file `/tmp/test.pcap` using the rules
`/tmp/test.rules` logging to the directory `./log`, run:

    ./run.py -r /tmp/test.pcap -S /tmp/test.rules -l ./log
    
