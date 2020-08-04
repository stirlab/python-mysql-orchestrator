# python-mysql-orchestrator

Simple wrapper class for the
[MySQL Orchestrator](https://github.com/openark/orchestrator) API, and some convenience scripts.

## Overview

MySQL Orchestrator has a robust
[REST API](https://github.com/openark/orchestrator/blob/master/docs/using-the-web-api.md).

This humble library provides the following:

 * A base ```Orchestrator``` class
 * ```orchestrator-run.py```: Wraps the base class for calling from CLI
 * ```auto-master-writer.py```: Detects a healthy cluster with a master that has
   ```read_only = true```, and sets ```read_only = false``` (this allows
   configuring all cluster nodes to start in read-only mode, and still provide
   an automated way to set the master as writeable.

### Setup

 * Copy ```config.sample.yaml``` to ```config.yaml```
 * Edit to taste
 * Execute ```orchestrator-run.py --help``` for help.

# Using/extending the base class

See [auto-master-writer.py](auto-master-writer.py) for an example of how to
extend the base ```Orchestrator``` class.
