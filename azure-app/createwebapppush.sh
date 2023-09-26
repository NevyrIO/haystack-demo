#! /bin/bash

RESOURCE_GROUP=<resource_group>

APP_NAME=haystacktestapp
ACR_NAME=haystackacrtest

# Save creds for acr image
ACR_PASSWORD=$(az acr credential show \
--resource-group $RESOURCE_GROUP \
--name $ACR_NAME \
--query "passwords[?name == 'password'].value" \
--output tsv)

# Create and push webapp
az webapp create \
--resource-group $RESOURCE_GROUP \
--plan haystacktestplan --name $APP_NAME \
--docker-registry-server-password $ACR_PASSWORD \
--docker-registry-server-user $ACR_NAME \
--role acrpull \
--deployment-container-image-name $ACR_NAME.azurecr.io/haystacktestapp:latest

# Configure key vault for app
az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP \
    --name $APP_NAME \
    --settings VaultName='<key_vault_name>'
# Assign identity to app
az webapp identity assign \
    --resource-group $RESOURCE_GROUP \
    --name $APP_NAME


