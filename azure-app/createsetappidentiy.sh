#! /bin/bash

VAULT_NAME=<key_vault_name>
PRINCIPAL_ID=<principal_id_from_createwebapppush.sh>

# Grant app access to vault - note: key access policy instead of RBAC must be set
az keyvault set-policy \
    --secret-permissions get list \
    --name $VAULT_NAME \
    --object-id $PRINCIPAL_ID
