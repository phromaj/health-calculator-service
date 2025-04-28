#!/bin/bash

# Exit script on error
set -e
# Treat unset variables as an error
set -u
# Prevent errors in pipelines
set -o pipefail

# --- Configuration ---
# IMPORTANT: Replace placeholders with your desired values.
# ACR names and Web App names must be globally unique.
RESOURCE_GROUP="rg-health-calculator-prod" # Name for the new resource group
LOCATION="westeurope"                      # Azure region (e.g., westus, eastus, westeurope)
ACR_NAME="acrhealthcalc$(openssl rand -hex 4)" # Unique name for Azure Container Registry
APPSERVICE_PLAN="plan-health-calculator-prod"  # Name for the App Service Plan
WEBAPP_NAME="app-health-calculator-$(openssl rand -hex 4)" # Unique name for the Web App
ACR_SKU="Basic"                            # ACR SKU (e.g., Basic, Standard, Premium)
APPSERVICE_PLAN_SKU="B1"                   # App Service Plan SKU (e.g., B1, S1, P1V2)
WEBAPP_PORT="5001"                         # Port your application listens on inside the container

# --- Script Logic ---

echo "Starting Azure resource deployment..."

# 1. Create Resource Group
echo "Creating resource group '$RESOURCE_GROUP' in location '$LOCATION'..."
az group create --name "$RESOURCE_GROUP" --location "$LOCATION" --output table

# 2. Create Azure Container Registry (ACR)
echo "Creating ACR '$ACR_NAME' with SKU '$ACR_SKU'..."
az acr create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$ACR_NAME" \
  --sku "$ACR_SKU" \
  --admin-enabled true \
  --output table

# 3. Create App Service Plan
echo "Creating App Service Plan '$APPSERVICE_PLAN' with SKU '$APPSERVICE_PLAN_SKU'..."
az appservice plan create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$APPSERVICE_PLAN" \
  --sku "$APPSERVICE_PLAN_SKU" \
  --is-linux \
  --output table

# 4. Create Web App for Containers
# Using a placeholder image initially; the CI/CD pipeline will deploy the correct one.
echo "Creating Web App '$WEBAPP_NAME'..."
az webapp create \
  --resource-group "$RESOURCE_GROUP" \
  --plan "$APPSERVICE_PLAN" \
  --name "$WEBAPP_NAME" \
  --deployment-container-image-name "mcr.microsoft.com/appsvc/staticsite:latest" \
  --output table
  # Note: We don't configure the ACR integration here,
  # as the GitHub Action's webapps-deploy handles pushing the image info.

# 5. Configure Web App Port Setting
echo "Configuring WEBSITES_PORT setting to '$WEBAPP_PORT' for '$WEBAPP_NAME'..."
az webapp config appsettings set \
  --resource-group "$RESOURCE_GROUP" \
  --name "$WEBAPP_NAME" \
  --settings WEBSITES_PORT="$WEBAPP_PORT" \
  --output table

# --- Output Secrets ---
echo "-----------------------------------------------------------------------"
echo "Deployment complete. Use the following values for your GitHub Secrets:"
echo "-----------------------------------------------------------------------"

# 6. Get ACR Credentials
echo "Retrieving ACR credentials for '$ACR_NAME'..."
ACR_CREDENTIALS=$(az acr credential show --name "$ACR_NAME" --resource-group "$RESOURCE_GROUP" --query "{username:username, password:passwords[0].value}" --output json)
ACR_USERNAME=$(echo "$ACR_CREDENTIALS" | jq -r .username)
ACR_PASSWORD=$(echo "$ACR_CREDENTIALS" | jq -r .password)
ACR_LOGIN_SERVER=$(az acr show --name "$ACR_NAME" --resource-group "$RESOURCE_GROUP" --query "loginServer" --output tsv)

echo ""
echo "ACR_LOGIN_SERVER:"
echo "$ACR_LOGIN_SERVER"
echo ""
echo "ACR_USERNAME:"
echo "$ACR_USERNAME"
echo ""
echo "ACR_PASSWORD:"
echo "$ACR_PASSWORD"
echo ""

# 7. Get Web App Publish Profile
echo "Retrieving Publish Profile for Web App '$WEBAPP_NAME'..."
PUBLISH_PROFILE=$(az webapp deployment list-publishing-profiles --name "$WEBAPP_NAME" --resource-group "$RESOURCE_GROUP" --xml)

echo "AZURE_WEBAPP_PUBLISH_PROFILE:"
echo "$PUBLISH_PROFILE"
echo ""
echo "-----------------------------------------------------------------------"
echo "Script finished."

# Note: jq (command-line JSON processor) is required to parse ACR credentials.
# Install it if you don't have it (e.g., 'sudo apt-get install jq' on Debian/Ubuntu).
