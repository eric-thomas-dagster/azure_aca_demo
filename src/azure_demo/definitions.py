from pathlib import Path
import os

import dagster as dg
from dagster import definitions, load_from_defs_folder


class EnvDebugResource(dg.ConfigurableResource):
    def setup_for_execution(self, context):
        # os.environ.get() is correct here — setup_for_execution runs in the run worker,
        # which has Dagster+ UI deployment env vars injected. dg.EnvVar() cannot be used
        # in resource configs because it is resolved at ExecutionPlanSnapshot time on the
        # code server, which does not have Dagster+ UI env vars in its environment.
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
