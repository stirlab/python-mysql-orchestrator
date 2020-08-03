#!/usr/bin/env python3

import os
import argparse
from manager import Manager, DEFAULT_CONFIG_FILE, DEFAULT_API_ENDPOINT

DEFAULT_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

def main():
    parser = argparse.ArgumentParser(description="Manage nftables sets")
    parser.add_argument("--debug", action='store_true', help="Enable debugging")
    parser.add_argument("--quiet", action='store_true', help="Silence output except for errors")
    parser.add_argument("--config-file", type=str, metavar="FILE", default=DEFAULT_CONFIG_FILE, help="Configuration filepath, default: %s" % DEFAULT_CONFIG_FILE)
    parser.add_argument("-p", "--path", type=str, metavar="PATH", default=DEFAULT_API_ENDPOINT, help="API endpoint, default: %s" % DEFAULT_API_ENDPOINT)
    #parser.add_argument("--berserk", action='store_true', help="Add all berserker_ips config to the resolver")
    #parser.add_argument("--sets", action='store', metavar="SET", type=str, nargs='+', help="Sets to update. Default is to update all sets in the configuration file")
    args = vars(parser.parse_args())
    config_file = args.pop('config_file')
    manager = Manager(config_file, args)
    manager.get(args['path'])

if __name__ == "__main__":
    main()
