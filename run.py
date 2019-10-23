#! /usr/bin/env python3

import sys
import os.path
import argparse
import subprocess

def ferror(msg):
    print("error: %s" % (msg), file=sys.stderr)
    sys.exit(1)

def main():

    docker_args = [
        "docker",
        "run",
        "--rm",
        "-it",
    ]

    command_args = [
        "snort",
        "-c",
        "/etc/snort/snort.conf",
    ]

    parser = argparse.ArgumentParser()

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

    args = parser.parse_args()

    if args.iface is None and args.pcap is None:
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

    abs_logdir = os.path.abspath(args.logdir)
    print("Logging to directory: %s" % (abs_logdir))
    docker_args.append(
        "--volume=%s:/var/log/snort" % (abs_logdir))
        
    # Append the image name to run...
    docker_args.append("jasonish/snort:latest")

    # Run...
    subprocess.call(docker_args + command_args)

if __name__ == "__main__":
    sys.exit(main())
