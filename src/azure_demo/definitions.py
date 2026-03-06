from pathlib import Path

import dagster as dg
from dagster import definitions, load_from_defs_folder

from azure_demo.components.azure_data_pipeline import EnvDebugResource


@definitions
def defs():
    return dg.Definitions.merge(
        load_from_defs_folder(path_within_project=Path(__file__).parent),
        dg.Definitions(resources={"env_debug": EnvDebugResource()}),
    )
