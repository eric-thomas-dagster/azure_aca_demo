import dagster as dg
from typing import Optional


class AzureDataPipeline(dg.Component, dg.Model, dg.Resolvable):
    """Azure Data Pipeline Component.

    A component that creates a complete data pipeline for Azure environments,
    including data ingestion from Azure Blob Storage, transformation, analytics,
    and export. Supports a demo_mode for local development without Azure credentials.
    """

    storage_account: str
    container_name: str
    demo_mode: bool = False
    input_path: Optional[str] = "raw-data/"
    output_path: Optional[str] = "processed-data/"

    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        @dg.asset(
            kinds={"azure", "blob-storage", "ingestion"},
            description="Ingests raw data from Azure Blob Storage",
        )
        def ingest_raw_data():
            """Ingest raw customer transaction data from Azure Blob Storage."""
            pass

        @dg.asset(
            kinds={"python", "data-cleaning"},
            description="Cleanses and validates ingested data",
            deps=[ingest_raw_data],
        )
        def cleanse_data():
            """Remove duplicates, handle missing values, and validate data quality."""
            pass

        @dg.asset(
            kinds={"python", "transformation"},
            description="Applies business logic transformations to cleansed data",
            deps=[cleanse_data],
        )
        def transform_data():
            """Apply business rules: calculate metrics, aggregate by customer, enrich with metadata."""
            pass

        @dg.asset(
            kinds={"python", "analytics"},
            description="Performs analytics and generates insights",
            deps=[transform_data],
        )
        def analyze_data():
            """Generate customer segmentation, trend analysis, and key performance indicators."""
            pass

        @dg.asset(
            kinds={"azure", "blob-storage", "export"},
            description="Exports processed results to Azure Blob Storage",
            deps=[analyze_data],
        )
        def export_results():
            """Export analytics results and processed data back to Azure Blob Storage."""
            pass

        # Create resource for Azure Blob Storage
        if self.demo_mode:
            # In demo mode, use a mock resource
            from dagster import ConfigurableResource

            class MockAzureBlobStorage(ConfigurableResource):
                storage_account: str
                container_name: str

                def get_client(self):
                    return None

            azure_resource = MockAzureBlobStorage(
                storage_account=self.storage_account,
                container_name=self.container_name,
            )
        else:
            # In production mode, use actual Azure resources
            from dagster_azure.adls2 import ADLS2Resource

            azure_resource = ADLS2Resource(
                storage_account=self.storage_account,
            )

        return dg.Definitions(
            assets=[
                ingest_raw_data,
                cleanse_data,
                transform_data,
                analyze_data,
                export_results,
            ],
            resources={
                "azure_blob": azure_resource,
            },
        )
