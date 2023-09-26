#! /bin/bash

RESOURCE_GROUP=<resource_group>

# Create App Service 
az appservice plan create \
--name haystacktestplan \
--is-linux \
--resource-group $RESOURCE_GROUP \
--sku P2V3 


