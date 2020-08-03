#!/usr/bin/env python3

import argparse
from orchestrator import Orchestrator, DEFAULT_CONFIG_FILE

class AutoUpdater(Orchestrator):

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

    def run(self):
        data = self.get_cluster_master()
        if data:
            needs_update, hostname, port, slave_hosts = self.master_needs_update(data)
            if needs_update:
                self.logger.info("Master %s:%d exists, needs update, with slaves: %s" % (hostname, port, slave_hosts))
                self.set_instance_writeable(hostname, port)

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
