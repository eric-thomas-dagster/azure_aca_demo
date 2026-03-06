from pathlib import Path
import logging
import os

import dagster as dg
from dagster import definitions, load_from_defs_folder

_logger = logging.getLogger("dagster")


class EnvDebugResource(dg.ConfigurableResource):
    # NOTE: dg.EnvVar() as a field default is resolved at ExecutionPlanSnapshot time
    # on the code server — it requires the var to be a real container env var at
    # startup, not just a Dagster+ UI deployment env var (those only reach run workers).
    # We read from os.environ inside methods instead, which runs in the run worker
    # where all deployment-level env vars are available.

    def setup_for_execution(self, _context):
        _logger.info(f"Resource initializing in container: {os.environ.get('HOSTNAME', 'unknown')}")
        _logger.info(f"ELT_REPO_BRANCH at resource init: {os.environ.get('ELT_REPO_BRANCH', 'NOT SET')}")
        return self


@dg.asset
def env_check(context: dg.AssetExecutionContext, env_debug: EnvDebugResource):
    context.log.info(f"Asset running in container: {os.environ.get('HOSTNAME', 'unknown')}")
    context.log.info(f"ELT_REPO_BRANCH in run worker: {os.getenv('ELT_REPO_BRANCH', 'NOT SET')}")


@definitions
def defs():
    return dg.Definitions.merge(
        load_from_defs_folder(path_within_project=Path(__file__).parent),
        dg.Definitions(
            assets=[env_check],
            resources={"env_debug": EnvDebugResource()},
        ),
    )
