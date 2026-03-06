from pathlib import Path
import logging
import os

import dagster as dg
from dagster import definitions, load_from_defs_folder

_logger = logging.getLogger("dagster")


class EnvDebugResource(dg.ConfigurableResource):
    # dg.EnvVar resolves from Dagster Cloud platform API — works even in
    # multiprocess executor subprocesses where os.environ may not be propagated.
    branch: str = dg.EnvVar("ELT_REPO_BRANCH")

    def setup_for_execution(self, _context):
        _logger.info(f"Resource initializing in container: {os.environ.get('HOSTNAME', 'unknown')}")
        _logger.info(f"ELT_REPO_BRANCH via os.environ at resource init: {os.environ.get('ELT_REPO_BRANCH', 'NOT SET')}")
        _logger.info(f"ELT_REPO_BRANCH via dg.EnvVar at resource init: {self.branch}")
        return self


@dg.asset
def env_check(context: dg.AssetExecutionContext, env_debug: EnvDebugResource):
    context.log.info(f"Asset running in container: {os.environ.get('HOSTNAME', 'unknown')}")
    context.log.info(f"ELT_REPO_BRANCH via os.environ in asset: {os.getenv('ELT_REPO_BRANCH', 'NOT SET')}")
    context.log.info(f"ELT_REPO_BRANCH via resource in asset: {env_debug.branch}")


@definitions
def defs():
    return dg.Definitions.merge(
        load_from_defs_folder(path_within_project=Path(__file__).parent),
        dg.Definitions(
            assets=[env_check],
            resources={"env_debug": EnvDebugResource()},
        ),
    )
