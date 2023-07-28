# Prisma Cloud Policy-as-Code

This repository contains a simple Python script to help enable Policy-as-code use cases for Prisma Cloud's posture management policy library

## Getting Started
Simply installing the Python dependencies from either Poetry or requirements.txt with pip
```bash
pip install -r requirements.txt

# With poetry
pip install poetry
poetry install
```

## Running the sync
#### With Python
```bash
python app.py --access-key <PRISMA_ACCESS_KEY> --secret-key <PRISMA_SECRET_KEY> update ./policies
```
#### With Poetry
```bash
poetry run python app.py --access-key <PRISMA_ACCESS_KEY> --secret-key <PRISMA_SECRET_KEY> update ./policies
```

### Example output
```bash
python app.py --access-key $TWISTLOCK_USER --secret-key $TWISTLOCK_PASSWORD update ./policies
Skipping existing policy 'Deprecated accounts with owner permissions with role assignment on a subscription'
Skipping existing policy 'Advanced data security should be enabled on SQL Managed Instance'
Skipping existing policy 'Azure for PostgreSQL server doesn't have private endpoint enabled'
Policy 'Audit Storage accounts that do not have 'Advanced Threat Protection' enabled created successfully'
Skipping existing policy 'Azure Network Interface doesn't have a Network Security Group attached'
Skipping existing policy 'App Service apps should have resource logs enabled'
Skipping existing policy 'Resource logs in Search services should be enabled'
Policy 'Disk encryption is not enabled on Azure Data Explorer created successfully'
Skipping existing policy 'Resource logs in Event Hub should be enabled'
Policy 'External account has Owner role assignment created successfully'
Skipping existing policy 'Azure for MySQL server doesn't have private endpoint enabled'
Policy 'External account has read permissions created successfully'
Policy 'Geo-redundant backup should be enabled for Azure Database for MariaDB created successfully'
Policy 'Geo-redundant backup should be enabled for Azure Database for PostgreSQL created successfully'
Skipping existing policy 'Resource logs in Batch accounts should be enabled'
Skipping existing policy 'Azure for MariaDB server doesn't have private endpoint enabled'
Policy 'External account has wildcard permissions created successfully'
Skipping existing policy 'Resource logs in Logic Apps should be enabled'
Policy 'Double encryption is not enabled on Azure Data Explorer created successfully'
Skipping existing policy 'Resource logs in Azure Data Lake Analytics should be enabled'
Skipping existing policy 'Deploy diagnostic settings for Virtual Networks.'
Skipping existing policy 'Resource logs in Service Bus should be enabled'
Skipping existing policy 'Azure SQL server does not have private endpoints'
Policy 'Geo-redundant backup should be enabled for Azure Database for MySQL created successfully'
Skipping existing policy 'Only secure connections to your Redis Cache should be enabled'
Skipping existing policy 'Resource logs in Azure Stream Analytics should be enabled'
Skipping existing policy 'Geo-redundant storage should be enabled for Storage Accounts'
==> 27 policies evaluated
```
