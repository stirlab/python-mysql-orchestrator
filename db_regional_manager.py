#!/usr/bin/env python3

import os
import argparse
import yaml
import requests
import logging
import pprint

logging.basicConfig(level=logging.INFO)
pp = pprint.PrettyPrinter(indent=4)

DEFAULT_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_CONFIG_FILE = "%s/config.yaml" % DEFAULT_SCRIPT_DIR
DEFAULT_API_ENDPOINT = "clusters"

class Manager(object):

    def __init__(self, args, config):
        self.args = args
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        if self.args.quiet:
            self.logger.setLevel(logging.ERROR)
        if self.args.debug:
            self.logger.setLevel(logging.DEBUG)

    def make_url(self):
        return "http://%s:%s/api/%s" % (self.config['orchestrator']['host'], self.config['orchestrator']['port'], self.args.path)

    def get(self):
        self.logger.debug("Retrieving JSON data from : %s" % self.args.path)
        pp.pprint(self.config)
        try:
            response = requests.get(self.make_url(), auth=(self.config['orchestrator']['username'], self.config['orchestrator']['password']))
            response.raise_for_status()
            data = response.json()
            pp.pprint(data)
        except Exception as err:
            self.logger.error('Error occurred: %s' % err)
            return False

def main():
    parser = argparse.ArgumentParser(description="Manage nftables sets")
    parser.add_argument("--debug", action='store_true', help="Enable debugging")
    parser.add_argument("--quiet", action='store_true', help="Silence output except for errors")
    parser.add_argument("--config-file", type=str, metavar="FILE", default=DEFAULT_CONFIG_FILE, help="Configuration filepath, default: %s" % DEFAULT_CONFIG_FILE)
    parser.add_argument("-p", "--path", type=str, metavar="PATH", default=DEFAULT_API_ENDPOINT, help="API endpoint, default: %s" % DEFAULT_API_ENDPOINT)
    #parser.add_argument("--berserk", action='store_true', help="Add all berserker_ips config to the resolver")
    #parser.add_argument("--sets", action='store', metavar="SET", type=str, nargs='+', help="Sets to update. Default is to update all sets in the configuration file")
    args = parser.parse_args()
    with open(args.config_file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as err:
            raise RuntimeError("Could not load config file %s: %s" % (args.config_file, err))
        manager = Manager(args, config)
        manager.get()

if __name__ == "__main__":
    main()
