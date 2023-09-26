#! /bin/bash

RESOURCE_GROUP=<resource_group>

# Use this in your own setting if you do not already have a resource group
## az group create --name <your-resource-group-rg> --location <location>

# Create container registry 
ACR_NAME=haystackacrtest
az acr create --resource-group $RESOURCE_GROUP \
--name $ACR_NAME --sku Standard --admin-enabled true  # Basic (10G), Standard (100G), Premium 

# Save creds for acr image
ACR_PASSWORD=$(az acr credential show \
--resource-group $RESOURCE_GROUP \
--name $ACR_NAME \
--query "passwords[?name == 'password'].value" \
--output tsv)

# Build and push to ACR
az acr build \
  --resource-group $RESOURCE_GROUP \
  --registry $ACR_NAME \
  --image haystacktestapp:latest .



