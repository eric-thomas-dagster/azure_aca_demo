from pathlib import Path
import logging
import os

import dagster as dg
from dagster import definitions, load_from_defs_folder

_logger = logging.getLogger("dagster")


class EnvDebugResource(dg.ConfigurableResource):
    # dg.EnvVar() is resolved on the code server at ExecutionPlanSnapshot time.
    # This requires ELT_REPO_BRANCH to be set as a real container env var on the
    # code server — which happens when the ACA launcher includes it in cloud_context_env
    # (requires UserCodeDeploymentType.ECS so Dagster Cloud sends user-defined
    # deployment env vars to the launcher). Reload the code location after setting
    # the env var in Dagster+ UI to restart the code server with the updated env.
    branch: str = dg.EnvVar("ELT_REPO_BRANCH")

    def setup_for_execution(self, _context):
        _logger.info(f"Resource initializing in container: {os.environ.get('HOSTNAME', 'unknown')}")
        _logger.info(f"ELT_REPO_BRANCH at resource init: {self.branch}")
        return self


@dg.asset
def env_check(context: dg.AssetExecutionContext, env_debug: EnvDebugResource):
    context.log.info(f"Asset running in container: {os.environ.get('HOSTNAME', 'unknown')}")
    context.log.info(f"ELT_REPO_BRANCH via resource: {env_debug.branch}")
    context.log.info(f"ELT_REPO_BRANCH via os.environ: {os.getenv('ELT_REPO_BRANCH', 'NOT SET')}")


@definitions
def defs():
    return dg.Definitions.merge(
        load_from_defs_folder(path_within_project=Path(__file__).parent),
        dg.Definitions(
            assets=[env_check],
            resources={"env_debug": EnvDebugResource()},
        ),
    )
