from pathlib import Path

import dagster as dg
from dagster import definitions, load_from_defs_folder


class EltConfig(dg.ConfigurableResource):
    """Fake ELT resource — validates that env vars are forwarded to code servers."""

    elt_repo_branch: str
    azure_storage_account: str


@definitions
def defs():
    elt_resource = EltConfig(
        elt_repo_branch=dg.EnvVar("ELT_REPO_BRANCH"),
        azure_storage_account=dg.EnvVar("AZURE_STORAGE_ACCOUNT"),
    )

    return dg.Definitions.merge(
        load_from_defs_folder(path_within_project=Path(__file__).parent),
        dg.Definitions(resources={"elt_config": elt_resource}),
    )
