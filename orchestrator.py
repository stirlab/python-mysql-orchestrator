#!/usr/bin/env python3

import os
import yaml
import requests
import logging
import pprint

logging.basicConfig(level=logging.INFO)
pp = pprint.PrettyPrinter(indent=4)

DEFAULT_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_CONFIG_FILE = "%s/config.yaml" % DEFAULT_SCRIPT_DIR
DEFAULT_API_ENDPOINT = "clusters"

class Orchestrator(object):

    def __init__(self, config_file=None, args={}):
        self.config = self.parse_config(config_file or DEFAULT_CONFIG_FILE)
        self.config.update(args)
        self.defaults = self.config['defaults']
        self.quiet = 'quiet' in self.config and self.config['quiet']
        self.debug = 'debug' in self.config and self.config['debug']
        self.logger = logging.getLogger(self.__class__.__name__)
        self.log_level = self.logger.level
        if self.quiet:
            self.enable_quiet()
        if self.debug:
            self.enable_debug()
            self.logger.debug('Config:')
            pp.pprint(self.config)

    def default_loglevel(self):
        self.logger.setLevel(self.log_level)

    def enable_debug(self):
        self.logger.setLevel(logging.DEBUG)

    def enable_quiet(self):
        self.logger.setLevel(logging.ERROR)

    def parse_config(self, config_file):
        with open(config_file, 'r') as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as err:
                raise RuntimeError("Could not load config file %s: %s" % (config_file, err))
            return config

    def make_url(self, path=None):
        path = path or self.config['path']
        return "http://%s:%s/api/%s" % (self.config['orchestrator']['host'], self.config['orchestrator']['port'], path)

    def parse_action_response(self, data):
        success = data['Code'] == 'OK'
        return success, data['Message']

    def get(self, path):
        self.logger.debug("Retrieving JSON data from : %s" % path)
        try:
            response = requests.get(self.make_url(path), auth=(self.config['orchestrator']['username'], self.config['orchestrator']['password']))
            response.raise_for_status()
            data = response.json()
            if self.debug:
                pp.pprint(data)
            return data
        except Exception as err:
            self.logger.error('Error occurred: %s' % err)
            return False

    def set_instance_read_only(self, hostname, port=3306):
        self.logger.debug("Setting %s:%d writable" % (hostname, port))
        return self.instance_action('set-read-only', hostname, port)

    def set_instance_writeable(self, hostname, port=3306):
        self.logger.debug("Setting %s:%d writable" % (hostname, port))
        return self.instance_action('set-writeable', hostname, port)

    def get_cluster_master(self, cluster=None):
        cluster = cluster or self.defaults['cluster']
        return self.get('master/%s' % cluster)


    def instance_action(self, path, hostname, port=3306):
        data = self.get('%s/%s/%d' % (path, hostname, port))
        if data:
            success, message = self.parse_action_response(data)
            self.logger.debug("Instance action message: %s" % message)
            return success
        return False
