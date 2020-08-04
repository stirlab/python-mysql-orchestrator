#!/usr/bin/env python3

import argparse
from orchestrator import Orchestrator, DEFAULT_CONFIG_FILE, DEFAULT_API_ENDPOINT
import pprint

pp = pprint.PrettyPrinter(indent=4)

def main():
    parser = argparse.ArgumentParser(description="Run orchestrator API commands from CLI")
    parser.add_argument("--debug", action='store_true', help="Enable debugging")
    parser.add_argument("--quiet", action='store_true', help="Silence output except for errors")
    parser.add_argument("--config-file", type=str, metavar="FILE", default=DEFAULT_CONFIG_FILE, help="Configuration filepath, default: %s" % DEFAULT_CONFIG_FILE)
    parser.add_argument("path", type=str, default=DEFAULT_API_ENDPOINT, help="API endpoint, e.g. %s" % DEFAULT_API_ENDPOINT)
    args = vars(parser.parse_args())
    config_file = args.pop('config_file')
    orchestrator = Orchestrator(config_file, args)
    path = args['path']
    print("Executing API command: %s" % path)
    data = orchestrator.get(path)
    pp.pprint(data)

if __name__ == "__main__":
    main()
