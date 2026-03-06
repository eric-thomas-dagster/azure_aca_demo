from pathlib import Path
import logging
import os

import dagster as dg
from dagster import definitions, load_from_defs_folder

# Runs at code server import time — visible in code server startup logs.
# This tells us definitively what env vars the code server container has.
logging.getLogger("dagster").info(
    f"[code-server-init] HOSTNAME={os.environ.get('HOSTNAME', 'unknown')} "
    f"ELT_REPO_BRANCH={os.environ.get('ELT_REPO_BRANCH', 'NOT SET')}"
)


class EnvDebugResource(dg.ConfigurableResource):
    def setup_for_execution(self, context):
        context.log.info(f"Resource initializing in container: {os.environ.get('HOSTNAME', 'unknown')}")
        context.log.info(f"ELT_REPO_BRANCH via resource: {os.environ.get('ELT_REPO_BRANCH', 'NOT SET')}")
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
