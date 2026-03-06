from pathlib import Path
import os

import dagster as dg
from dagster import definitions, load_from_defs_folder


class EnvDebugResource(dg.ConfigurableResource):
    elt_repo_branch: str

    def setup_for_execution(self, context):
        context.log.info(f"Resource initializing in container: {os.environ.get('HOSTNAME', 'unknown')}")
        context.log.info(f"ELT_REPO_BRANCH via dg.EnvVar resource field: {self.elt_repo_branch}")
        return self


@dg.asset
def env_check(context: dg.AssetExecutionContext, env_debug: EnvDebugResource):
    context.log.info(f"Asset running in container: {os.environ.get('HOSTNAME', 'unknown')}")
    context.log.info(f"ELT_REPO_BRANCH via os.environ: {os.getenv('ELT_REPO_BRANCH', 'NOT SET')}")
    context.log.info(f"ELT_REPO_BRANCH via resource field: {env_debug.elt_repo_branch}")


@definitions
def defs():
    return dg.Definitions.merge(
        load_from_defs_folder(path_within_project=Path(__file__).parent),
        dg.Definitions(
            assets=[env_check],
            resources={"env_debug": EnvDebugResource(elt_repo_branch=dg.EnvVar("ELT_REPO_BRANCH"))},
        ),
    )
