from pathlib import Path
import logging
import os

import dagster as dg
from dagster import definitions, load_from_defs_folder

_logger = logging.getLogger("dagster")


class EnvDebugResource(dg.ConfigurableResource):
    # No config fields that reference env vars — dg.EnvVar() is resolved at
    # config validation time on the code server, but deployment-level env vars
    # (set in the Dagster+ UI) are only injected into the run worker process.
    # Reading from os.environ inside methods works correctly in the run worker.

    def setup_for_execution(self, _context):
        _logger.info(f"Resource initializing in container: {os.environ.get('HOSTNAME', 'unknown')}")
        _logger.info(f"ELT_REPO_BRANCH at resource init: {os.environ.get('ELT_REPO_BRANCH', 'NOT SET')}")
        return self


@dg.asset
def env_check(context: dg.AssetExecutionContext, env_debug: EnvDebugResource):
    context.log.info(f"Asset running in container: {os.environ.get('HOSTNAME', 'unknown')}")
    context.log.info(f"ELT_REPO_BRANCH in asset: {os.getenv('ELT_REPO_BRANCH', 'NOT SET')}")


@definitions
def defs():
    return dg.Definitions.merge(
        load_from_defs_folder(path_within_project=Path(__file__).parent),
        dg.Definitions(
            assets=[env_check],
            resources={"env_debug": EnvDebugResource()},
        ),
    )
