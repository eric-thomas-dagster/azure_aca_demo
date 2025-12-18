# Azure Demo - Dagster Hybrid Deployment

A demonstration Dagster project showcasing a data pipeline for Azure environments with hybrid deployment using Azure Container Registry (ACR).

## Project Overview

This project demonstrates:
- **Azure Integration**: Pipeline that processes data from Azure Blob Storage
- **Hybrid Deployment**: Deployed on Dagster+ Hybrid with ACR as the container registry
- **Demo Mode**: Run locally without Azure credentials for demonstrations
- **5 Assets**: Complete data pipeline from ingestion to export

### Pipeline Assets

1. **ingest_raw_data** - Ingests raw customer transaction data from Azure Blob Storage
2. **cleanse_data** - Removes duplicates, handles missing values, and validates data quality
3. **transform_data** - Applies business rules and aggregations
4. **analyze_data** - Generates customer segmentation and analytics
5. **export_results** - Exports results back to Azure Blob Storage

## Getting started

### Installing dependencies

**Option 1: uv**

Ensure [`uv`](https://docs.astral.sh/uv/) is installed following their [official documentation](https://docs.astral.sh/uv/getting-started/installation/).

Create a virtual environment, and install the required dependencies using _sync_:

```bash
uv sync
```

Then, activate the virtual environment:

| OS | Command |
| --- | --- |
| MacOS | ```source .venv/bin/activate``` |
| Windows | ```.venv\Scripts\activate``` |

**Option 2: pip**

Install the python dependencies with [pip](https://pypi.org/project/pip/):

```bash
python3 -m venv .venv
```

Then activate the virtual environment:

| OS | Command |
| --- | --- |
| MacOS | ```source .venv/bin/activate``` |
| Windows | ```.venv\Scripts\activate``` |

Install the required dependencies:

```bash
pip install -e ".[dev]"
```

### Running Dagster

Start the Dagster UI web server:

```bash
dg dev
```

Open http://localhost:3000 in your browser to see the project.

## Deployment to Dagster+ Hybrid

### Prerequisites

1. **Azure Container Registry (ACR)**
   - Create an ACR instance in Azure
   - Note the registry name (e.g., `myregistry`)
   - Create service principal credentials for authentication

2. **GitHub Secrets**

   Configure the following secrets in your GitHub repository:
   - `DAGSTER_CLOUD_ORGANIZATION` - Your Dagster+ organization ID
   - `DAGSTER_CLOUD_API_TOKEN` - Dagster+ API token
   - `ACR_REGISTRY_NAME` - ACR registry name (without .azurecr.io)
   - `ACR_USERNAME` - ACR service principal ID
   - `ACR_PASSWORD` - ACR service principal password

3. **Dagster+ Hybrid Agent**

   Ensure you have a Dagster+ Hybrid agent running that can:
   - Pull images from your ACR registry
   - Has network access to your Azure resources

### Deployment Process

The GitHub Actions workflow (`.github/workflows/deploy-hybrid.yml`) will:

1. Initialize a Dagster Cloud build session
2. Validate the `dagster_cloud.yaml` configuration
3. Build a Docker image with your Dagster code
4. Push the image to Azure Container Registry
5. Update the build session with the Docker image tag
6. Deploy to Dagster+ Hybrid using the ACR image

Deployment is triggered on:
- Push to `main`/`master` branch (deploys to `prod`)
- Pull requests (creates branch deployments for testing)

### Configuration Files

**dagster_cloud.yaml** - Defines the code location for Dagster+:
```yaml
locations:
  - location_name: azure-pipeline
    code_source:
      package_name: azure_demo.definitions
    build:
      directory: .
      registry: ${IMAGE_REGISTRY}
```

**Component Configuration** - To switch from demo mode to production mode:

Edit `src/azure_demo/defs/azure_pipeline/defs.yaml`:

```yaml
attributes:
  storage_account: "your-storage-account"
  container_name: "your-container"
  demo_mode: false  # Set to false for production
  input_path: "raw-data/transactions/"
  output_path: "processed-data/analytics/"
```

Ensure your Dagster+ Hybrid agent has access to Azure credentials:
- Configure Azure service principal credentials
- Set up proper IAM roles for Blob Storage access

## Learn more

To learn more about this template and Dagster in general:

- [Dagster Documentation](https://docs.dagster.io/)
- [Dagster University](https://courses.dagster.io/)
- [Dagster Slack Community](https://dagster.io/slack)
