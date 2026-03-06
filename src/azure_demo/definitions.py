from pathlib import Path

import dagster as dg
from dagster import definitions, load_from_defs_folder


class EnvDebugResource(dg.ConfigurableResource):
    elt_repo_branch: str
    azure_storage_account: str
    azure_storage_key: str

    def setup_for_execution(self, context):
        context.log.info(f"ELT_REPO_BRANCH via dg.EnvVar: {self.elt_repo_branch}")
        context.log.info(f"AZURE_STORAGE_ACCOUNT via dg.EnvVar: {self.azure_storage_account}")
        context.log.info(f"AZURE_STORAGE_KEY via dg.EnvVar: {'SET' if self.azure_storage_key else 'EMPTY'}")
        return self


@dg.asset
def env_check(context: dg.AssetExecutionContext, env_debug: EnvDebugResource):
    context.log.info(f"ELT_REPO_BRANCH via dg.EnvVar resource: {env_debug.elt_repo_branch}")
    context.log.info(f"AZURE_STORAGE_ACCOUNT via dg.EnvVar resource: {env_debug.azure_storage_account}")
    context.log.info(f"AZURE_STORAGE_KEY via dg.EnvVar resource: {'SET' if env_debug.azure_storage_key else 'EMPTY'}")


@definitions
def defs():
    return dg.Definitions.merge(
        load_from_defs_folder(path_within_project=Path(__file__).parent),
        dg.Definitions(
            assets=[env_check],
            resources={
                "env_debug": EnvDebugResource(
                    elt_repo_branch=dg.EnvVar("ELT_REPO_BRANCH"),
                    azure_storage_account=dg.EnvVar("AZURE_STORAGE_ACCOUNT"),
                    azure_storage_key=dg.EnvVar("AZURE_STORAGE_KEY"),
                )
            },
        ),
    )
