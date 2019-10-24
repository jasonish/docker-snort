#! /usr/bin/env python3

import sys
import os.path
import argparse
import subprocess

def ferror(msg):
    print("error: {}".format(msg), file=sys.stderr)
    sys.exit(1)

EPILOG = """To provide additional command line options to Snort specify them
after --

For example:

    ./run.py -r input.pcap -- -k none

"""

def main():

    docker_args = [
        "docker",
        "run",
        "--rm",
        "-it",
        "-e", "PUID=%d" % os.getuid(),
        "-e", "PGID=%d" % os.getgid(),
    ]

    command_args = [
        "snort",
        "-u", "snort",
        "-c", "/etc/snort/snort.conf",
    ]

    parser = argparse.ArgumentParser(
        epilog=EPILOG, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        "-l", metavar="DIR", default=".", dest="logdir",
        help="Log directory (default=.)")

    parser.add_argument(
        "-i", metavar="IFACE", default=None, dest="iface",
        help="Interface to listen on")

    parser.add_argument(
        "-r", metavar="FILE", default=None, dest="pcap",
        help="PCAP file to read")

    parser.add_argument(
        "-S", "--rules", metavar="FILE", default=None, dest="rules",
        help="Rule file to load (default empty)")

    parser.add_argument(
        "--shell", action="store_true", default=False,
        help="Drop to a shell inside the container instead of running Snort")

    parser.add_argument(
        "--etc", metavar="DIR", default=None,
        help="Directory to use for /etc/snort (will be populated on first run)")

    (args, rem) = parser.parse_known_args()

    if not args.shell and args.iface is None and args.pcap is None:
        print("error: either pcap or interface must be specified",
              file=sys.stderr)
        return 1
    if args.iface and args.pcap:
        print("error: pcap and file cannot be provided together",
              file=sys.stderr)
        return 1
    if args.iface:
        docker_args.append("--net=host")
        command_args += ["-i", args.iface]
    if args.pcap:
        abs_pcap = os.path.abspath(args.pcap)
        if not os.path.exists(abs_pcap):
            ferror("file does not exist: %s" % (args.pcap))
        docker_args.append(
            "--volume=%s:/tmp/test.pcap" % (abs_pcap))
        command_args += ["-r", "/tmp/test.pcap"]

    if args.rules:
        abs_rulefile = os.path.abspath(args.rules)
        if not os.path.exists(abs_rulefile):
            ferror("rule file does not exist: %s" % (args.rules))
        else:
            docker_args.append(
                "--volume=%s:/etc/snort/rules/local.rules" % (abs_rulefile))

    if args.etc:
        abs_etcpath = os.path.abspath(args.etc)
        docker_args.append(
            "--volume=%s:/etc/snort" % (abs_etcpath))

    abs_logdir = os.path.abspath(args.logdir)
    print("Logging to directory: %s" % (abs_logdir))
    if not os.path.exists(abs_logdir):
        os.makedirs(abs_logdir)
    docker_args.append(
        "--volume=%s:/var/log/snort" % (abs_logdir))
        
    # Append the image name to run...
    docker_args.append("jasonish/snort:latest")

    if args.shell:
        docker_args.append("bash")
    else:
        docker_args += command_args + rem[1:]

    # Run...
    print("Running: %s" % str(docker_args))
    subprocess.call(docker_args)

if __name__ == "__main__":
    sys.exit(main())
