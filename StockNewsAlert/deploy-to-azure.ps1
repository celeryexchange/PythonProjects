# (Warning) Manual action needed for Steps 10-11 (creating identity and assigning role)

# code assumes you're using Azure CLI and Powershell and are already logged in
# az login

# Variables
$RESOURCE_GROUP="StockAlertApp"
$LOCATION="westeurope"
$APP_NAME="StockAlertApp"
$CONTAINER_REGISTRY_NAME="stockalertappregistry"
$CONTAINER_REGISTRY_SKU="basic"
$DOCKER_IMAGE_NAME="stock-alert-app"
$DOCKER_IMAGE_TAG="latest"
$PLAN_NAME="StockAlertAppServicePlan"
$PLAN_SKU="F1"  # F1: free 60 minutes/day; B1: basic £12/month
$KEY_VAULT_NAME="StockAlertAppKeyVault"
$WEBAPP_NAME="stock-alert--web-app"
$LOGIC_APP_NAME="StockAlertAppLogicApp"
$ACI_NAME="news-alert-app-container"

# Look up this variable from the currently active subscription
$SUBSCRIPTION_ID =$(az account show --query "id" -o tsv)

# Step 1: Create a Resource Group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Step 2: Create an Azure Container Registry (for Docker image)
az acr create --resource-group $RESOURCE_GROUP --name $CONTAINER_REGISTRY_NAME --sku $CONTAINER_REGISTRY_SKU --admin-enabled true

# Step 3: Create an Azure Key Vault for secret management
az keyvault create --resource-group $RESOURCE_GROUP --name $KEY_VAULT_NAME --location $LOCATION

# Step 4: Load secrets from .env into local scope before sending them to Azure Key Vault
# This helps me not expose the secrets in this code

# Define the path to the .env file
$envFilePath = ".\.env"

# Check if the file exists
if (Test-Path $envFilePath) {

    # Read the content of the .env file line by line
    $envContent = Get-Content $envFilePath

    # Loop through each line
    foreach ($line in $envContent) {

        # Skip empty lines or lines that start with a comment (e.g., '#')
        if ($line -match "^\s*$" -or $line -match "^\s*#") {
            continue
        }

        # Split the line by '=' into a key-value pair
        $splitLine = $line -split '=', 2

        if ($splitLine.Length -eq 2) {
            $key = $splitLine[0].Trim()
            $value = $splitLine[1].Trim()

            # Set the environment variable in the current session
            [System.Environment]::SetEnvironmentVariable($key, $value, [System.EnvironmentVariableTarget]::Process)

            Write-Host "Loaded $key into environment variables."
        }
    }

    Write-Host "Environment variables loaded successfully."
} else {
    Write-Host "Error: .env file not found at path $envFilePath"
}

# Step 5: Add secrets to Azure Key Vault
az keyvault secret set --vault-name $KEY_VAULT_NAME --name "ALPHA-VANTAGE-API-KEY" --value $Env:ALPHA_VANTAGE_API_KEY
az keyvault secret set --vault-name $KEY_VAULT_NAME --name "NEWS-API-KEY" --value $Env:NEWS_API_KEY
az keyvault secret set --vault-name $KEY_VAULT_NAME --name "TWILIO-ACCOUNT-SID" --value $Env:TWILIO_ACCOUNT_SID
az keyvault secret set --vault-name $KEY_VAULT_NAME --name "TWILIO-AUTH-TOKEN" --value $Env:TWILIO_AUTH_TOKEN

# Step 6: Build a Docker image and push it to Azure Container Registry
az acr build --registry $CONTAINER_REGISTRY_NAME --resource-group $RESOURCE_GROUP --image $DOCKER_IMAGE_NAME .

# Step 7: Deploy the container with Azure Container Instances, injecting secrets from Key Vault as environment variables
# Get secrets from Key Vault to pass into the container
$AlphaVantageApiKey = az keyvault secret show --vault-name $KEY_VAULT_NAME --name "ALPHA-VANTAGE-API-KEY" --query "value" -o tsv
$NewsApiKey = az keyvault secret show --vault-name $KEY_VAULT_NAME --name "NEWS-API-KEY" --query "value" -o tsv
$TwilioAccountSID = az keyvault secret show --vault-name $KEY_VAULT_NAME --name "TWILIO-ACCOUNT-SID" --query "value" -o tsv
$TwilioAuthToken = az keyvault secret show --vault-name $KEY_VAULT_NAME --name "TWILIO-AUTH-TOKEN" --query "value" -o tsv

# Get the Docker image URL
$acrImageUrl = "${CONTAINER_REGISTRY_NAME}.azurecr.io/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"

# Deploy the container with ACI
az container create --resource-group $RESOURCE_GROUP --name $ACI_NAME --image $acrImageUrl `
  --cpu 1 --memory 1.5 `
  --registry-username $(az acr credential show --name $CONTAINER_REGISTRY_NAME --query "username" -o tsv) `
  --registry-password $(az acr credential show --name $CONTAINER_REGISTRY_NAME --query "passwords[0].value" -o tsv) `
  --registry-login-server "$CONTAINER_REGISTRY_NAME.azurecr.io" `
  --environment-variables ALPHA_VANTAGE_API_KEY=$AlphaVantageApiKey NEWS_API_KEY=$NewsApiKey TWILIO_ACCOUNT_SID=$TwilioAccountSID TWILIO_AUTH_TOKEN=$TwilioAuthToken `
  --restart-policy Never

# Step 8: Create a JSON file to configure triggering the Azure Container Instances daily at 8pm
$LOGIC_APP_DEFINITION_PATH = ".\logicAppDefinition.json"
$LOGIC_APP_DEFINITION = @"
{
    "definition": {
        "`$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowDefinition.json#",
        "actions": {
            "RunContainer": {
                "type": "Http",
                "inputs": {
                    "method": "POST",
                    "uri": "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.ContainerInstance/containerGroups/$ACI_NAME/start?api-version=2018-10-01",
                    "authentication": {
                        "type": "ManagedServiceIdentity"
                    }
                }
            }
        },
        "triggers": {
            "Recurrence": {
                "type": "Recurrence",
                "recurrence": {
                    "frequency": "Day",
                    "interval": 1,
                    "timeZone": "UTC",
                    "startTime": "2024-10-28T17:00:00Z"
                }
            }
        }
    }
}
"@

# create the JSON definitions file
Set-Content -Path $LOGIC_APP_DEFINITION_PATH -Value $LOGIC_APP_DEFINITION

# Step 9: Schedule the script to run daily using Logic Apps
az logic workflow create `
    --resource-group $RESOURCE_GROUP `
    --name $LOGIC_APP_NAME `
    --location $LOCATION `
    --definition @$LOGIC_APP_DEFINITION_PATH

# Step 10: Create system-assigned identity for the Logic App
# ref: https://learn.microsoft.com/en-us/cli/azure/logic/workflow/identity?view=azure-cli-latest#az-logic-workflow-identity-assign
# Do this manually

# Step 11: Create/assign the "Contributor" role to the logic app (within the context of the Resource Group)
# ref: https://learn.microsoft.com/en-us/cli/azure/role/assignment?view=azure-cli-latest#az-role-assignment-create
# Do this manually

# Step 12: Remove the JSON definitions file after deployment
Remove-Item -Path $LOGIC_APP_DEFINITION_PATH -Force