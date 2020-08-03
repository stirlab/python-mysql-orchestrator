#!/usr/bin/env python3

import argparse
import time
from orchestrator import Orchestrator, DEFAULT_CONFIG_FILE

MASTER_AUTO_UPDATE_CHECK_THRESHOLD_DEFAULT = 3
MASTER_AUTO_UPDATE_INTERVAL_SECONDS_DEFAULT = 5

class AutoUpdater(Orchestrator):

    def __init__(self, config_file=None, args={}):
        super().__init__(config_file, args)
        self.checks = 0
        self.check_result = None
        try:
            self.auto_update_check_threshold = self.config['auto_master_writer' ]['check_threshold']
        except KeyError:
            self.auto_update_check_threshold = MASTER_AUTO_UPDATE_CHECK_THRESHOLD_DEFAULT
        try:
            self.auto_update_interval_seconds = self.config['auto_master_writer' ]['interval_seconds']
        except KeyError:
            self.auto_update_interval_seconds = MASTER_AUTO_UPDATE_INTERVAL_SECONDS_DEFAULT

    def master_needs_update(self, data):
        # Master info.
        hostname_info = data['Key']
        hostname = hostname_info['Hostname']
        port = hostname_info['Port']
        # Checks for master needs update.
        up_to_date = data['IsUpToDate']
        last_check_valid = data['IsLastCheckValid']
        recently_checked = data['IsRecentlyChecked']
        downtimed = data['IsDowntimed']
        problems = len(data['Problems']) > 0
        read_only = data['ReadOnly']
        # Slave info.
        slave_hosts = ', '.join([ "%s:%d" % (info['Hostname'], info['Port']) for info in data['SlaveHosts'] ])

        needs_update = up_to_date and last_check_valid and recently_checked and not downtimed and not problems and read_only

        self.logger.debug("IsUpToDate: %s" % up_to_date)
        self.logger.debug("IsLastCheckValid: %s" % last_check_valid)
        self.logger.debug("IsRecentlyChecked: %s" % recently_checked)
        self.logger.debug("IsDowntimed: %s" % downtimed)
        self.logger.debug("Problems: %s" % problems)
        self.logger.debug("ReadOnly: %s" % read_only)
        self.logger.debug("SlaveHosts: %s" % slave_hosts)
        self.logger.debug("Needs update: %s" % needs_update)
        return needs_update, hostname, port, slave_hosts

    def execute_check(self):
        data = self.get_cluster_master()
        if data:
            needs_update, hostname, port, slave_hosts = self.master_needs_update(data)
            if needs_update:
                self.logger.info("Master %s:%d exists, needs update, with slaves: %s" % (hostname, port, slave_hosts))
            return needs_update, hostname, port, slave_hosts
        return False, None, None, None

    def increment_checks(self):
        self.checks += 1
        self.logger.debug("Incremented checks to: %d" % self.checks)

    def reset_checks(self):
        self.checks = 0
        self.logger.debug("Reset checks")

    def verify_result(self, needs_update, hostname, port, slave_hosts):
        previous_result = self.check_result
        self.check_result = "%s:%s:%d:%s" % (needs_update, hostname, port, slave_hosts)
        self.logger.debug("Set check result to: %s" % self.check_result)
        if needs_update and previous_result == self.check_result:
            self.increment_checks()
        else:
            self.reset_checks()

    def next_action(self, needs_update, hostname, port):
        sleep_seconds = self.auto_update_interval_seconds
        if needs_update and self.checks >= self.auto_update_check_threshold:
            self.logger.info("Master needs update and passed check_threshold %d, setting writable" % self.auto_update_check_threshold)
            self.set_instance_writeable(hostname, port)
            sleep_seconds *= self.auto_update_check_threshold
        self.logger.debug("Waiting %d seconds before next check" % sleep_seconds)
        time.sleep(sleep_seconds)

    def run(self):
        self.logger.info("Starting master auto update checking with check_threshold: %d, interval_seconds: %d" % (self.auto_update_check_threshold, self.auto_update_interval_seconds))
        try:
            while True:
                needs_update, hostname, port, slave_hosts = self.execute_check()
                self.verify_result(needs_update, hostname, port, slave_hosts)
                self.next_action(needs_update, hostname, port)
        except KeyboardInterrupt:
            self.logger.warning('Process interrupted')

def main():
    parser = argparse.ArgumentParser(description="Manage nftables sets")
    parser.add_argument("--debug", action='store_true', help="Enable debugging")
    parser.add_argument("--quiet", action='store_true', help="Silence output except for errors")
    parser.add_argument("--config-file", type=str, metavar="FILE", default=DEFAULT_CONFIG_FILE, help="Configuration filepath, default: %s" % DEFAULT_CONFIG_FILE)
    args = vars(parser.parse_args())
    config_file = args.pop('config_file')
    auto_updater = AutoUpdater(config_file, args)
    auto_updater.run()


if __name__ == "__main__":
    main()
