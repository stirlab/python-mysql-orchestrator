#!/usr/bin/env python3

import argparse
from orchestrator import Orchestrator, DEFAULT_CONFIG_FILE, DEFAULT_API_ENDPOINT

def main():
    parser = argparse.ArgumentParser(description="Run orchestrator API commands from CLI")
    parser.add_argument("--debug", action='store_true', help="Enable debugging")
    parser.add_argument("--quiet", action='store_true', help="Silence output except for errors")
    parser.add_argument("--config-file", type=str, metavar="FILE", default=DEFAULT_CONFIG_FILE, help="Configuration filepath, default: %s" % DEFAULT_CONFIG_FILE)
    parser.add_argument("-p", "--path", type=str, metavar="PATH", default=DEFAULT_API_ENDPOINT, help="API endpoint, default: %s" % DEFAULT_API_ENDPOINT)
    args = vars(parser.parse_args())
    config_file = args.pop('config_file')
    orchestrator = Orchestrator(config_file, args)
    orchestrator.get(args['path'])

if __name__ == "__main__":
    main()
