# Snort Docker Image

This image is mainly for testing purposes. It has not been designed
for running Snort in a production/live environment.

## Building

This Docker image is pushed to `hub.docker.com` so the `run.py` tool
can be used without building, however the image can be rebuilt by
running `make`.

## Usage

```
usage: run.py [-h] [-l DIR] [-i IFACE] [-r FILE] [-S FILE] [--shell]
              [-v VOL [VOL ...]]

optional arguments:
  -h, --help            show this help message and exit
  -l DIR                Log directory (default=.)
  -i IFACE              Interface to listen on
  -r FILE               PCAP file to read
  -S FILE, --rules FILE
                        Rule file to load (default empty)
  --shell               Drop to a shell inside the container instead of
                        running Snort
  -v VOL [VOL ...]      Additional volumes

To provide additional command line options to Snort specify them
after --

For example:

    ./run.py -r input.pcap -- -k none
```

These options will run Snort with the following command line
arguments:

    -c /etc/snort/snort.conf
    -i <interface>
    -r <filename.pcap>

The log directory and rule file options are provided as volumes like:
- --volume=/path/to/local.rules:/etc/snort/rules/local.rules
- --volume=/path/to/logdir:/var/log/snort

## Example

To run Snort over a pcap file `/tmp/test.pcap` using the rules
`/tmp/test.rules` logging to the directory `./log`, run:

    ./run.py -r /tmp/test.pcap -S /tmp/test.rules -l ./log
    
## Custom Configuration

A custom configuration can be provided by adding a volume for
/etc/snort. The directory provided will be populated with the
configuration from the container on first run, and can then be
modified for subsequent runs. For example:

    ./run.py -v ./etc:/etc/snort -r /tmp/test.pcap -S /tmp/test.rules -l ./log
