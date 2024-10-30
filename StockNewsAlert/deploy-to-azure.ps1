# (Warning) Manual action needed for Steps 10-11 (creating identity and assigning role)
# (Warning) If you don't have a dedicated Azure Log Analytics Workspace, please create it beforehand.

# code assumes you're using Azure CLI and Powershell and are already logged in
# az login

# Variables
$RESOURCE_GROUP="StockAlertApp"
$LOCATION="westeurope"
$CONTAINER_REGISTRY_NAME="stockalertappregistry"
$CONTAINER_REGISTRY_SKU="basic"
$DOCKER_IMAGE_NAME="stock-alert-app"
$DOCKER_IMAGE_TAG="latest"
$KEY_VAULT_NAME="StockAlertAppKeyVault"
$LOGIC_APP_NAME="StockAlertAppLogicApp"
$ACI_NAME="news-alert-app-container"
$LOG_ANALYTICS_WORKSPACE_NAME="LogAnalyticsWorkspace"
$LOG_ANALYTICS_RESOURCE_GROUP="LogAnalytics"

# Look up variables from the currently active subscription
$SUBSCRIPTION_ID =$(az account show --query "id" -o tsv)

$LOG_ANALYTICS_KEY = $(az monitor log-analytics workspace get-shared-keys `
    --resource-group $LOG_ANALYTICS_RESOURCE_GROUP `
    --workspace-name $LOG_ANALYTICS_WORKSPACE_NAME `
    --query primarySharedKey `
    -o tsv)

$LOG_ANALYTICS_WORKSPACE_ID = $(az monitor log-analytics workspace show `
  --resource-group $LOG_ANALYTICS_RESOURCE_GROUP `
  --workspace-name $LOG_ANALYTICS_WORKSPACE_NAME `
  --query customerId -o tsv)

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

# Get secrets from Key Vault to pass into the container
$AlphaVantageApiKey = az keyvault secret show --vault-name $KEY_VAULT_NAME --name "ALPHA-VANTAGE-API-KEY" --query "value" -o tsv
$NewsApiKey = az keyvault secret show --vault-name $KEY_VAULT_NAME --name "NEWS-API-KEY" --query "value" -o tsv
$TwilioAccountSID = az keyvault secret show --vault-name $KEY_VAULT_NAME --name "TWILIO-ACCOUNT-SID" --query "value" -o tsv
$TwilioAuthToken = az keyvault secret show --vault-name $KEY_VAULT_NAME --name "TWILIO-AUTH-TOKEN" --query "value" -o tsv

# Deploy the container with ACI and with a System-Assigned Managed Identity
$acrImageUrl = "${CONTAINER_REGISTRY_NAME}.azurecr.io/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
az container create `
  --resource-group $RESOURCE_GROUP `
  --name $ACI_NAME `
  --image $acrImageUrl `
  --cpu 1 --memory 1.5 `
  --assign-identity `
  --registry-login-server "$CONTAINER_REGISTRY_NAME.azurecr.io" `
  --registry-username $(az acr credential show --name $CONTAINER_REGISTRY_NAME --query "username" -o tsv) `
  --registry-password $(az acr credential show --name $CONTAINER_REGISTRY_NAME --query "passwords[0].value" -o tsv) `
  --restart-policy Never `
  --log-analytics-workspace $LOG_ANALYTICS_WORKSPACE_ID `
  --log-analytics-workspace-key $LOG_ANALYTICS_KEY `
#   --secure-environment-variables ALPHA_VANTAGE_API_KEY=$AlphaVantageApiKey NEWS_API_KEY=$NewsApiKey TWILIO_ACCOUNT_SID=$TwilioAccountSID TWILIO_AUTH_TOKEN=$TwilioAuthToken `

# # Step 8: Grant ACI access to Azure Key Vault
$ACI_PRINCIPAL_ID = $(az container show --name $ACI_NAME --resource-group $RESOURCE_GROUP --query "identity.principalId" -o tsv)
az keyvault set-policy --name $KEY_VAULT_NAME --secret-permissions get --object-id $ACI_PRINCIPAL_ID


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
    --definition @$LOGIC_APP_DEFINITION_PATH `
    --mi-system-assigned true

# Step 10: Create system-assigned identity for the Logic App
# ref: https://learn.microsoft.com/en-us/cli/azure/logic/workflow/identity?view=azure-cli-latest#az-logic-workflow-identity-assign
# Do this manually

# Step 11: Create/assign the "Contributor" role to the logic app (within the context of the Resource Group)
# ref: https://learn.microsoft.com/en-us/cli/azure/role/assignment?view=azure-cli-latest#az-role-assignment-create
# Do this manually



# Optional: Enable log analytics for Azure Container Instances
# Get the resource ID for Log Analytics workspace


# # Enable diagnostics on the container to send logs to Log Analytics
# # Need to pass settings via JSON files to prevent shell from incorrectly parsing JSON
# $LOGS_SETTING_PATH = ".\analyticsLogsSetting.json"
# $METRICS_SETTING_PATH = ".\analyticsMetricsSetting.json"
#
# $LogsSettingsJson = @"
# [{
#     "category": "ContainerInstanceLog",
#     "categoryGroup": "Logs",
#     "enabled": true
# }]
# "@
# $MetricsSettingJson = @"
# [{
#     "category": "AllMetrics",
#     "enabled": true
# }]
# "@
#
# Set-Content -Path $LOGS_SETTING_PATH -Value $LogsSettingsJson
# Set-Content -Path $METRICS_SETTING_PATH -Value $MetricsSettingJson
#
# az monitor diagnostic-settings create `
#   --name "ACILoggingSettings" `
#   --resource-group $RESOURCE_GROUP `
#   --resource $ACI_NAME `
#   --resource-type "Microsoft.ContainerInstance/containerGroups" `
#   --workspace $LOG_ANALYTICS_WORKSPACE_ID `
#   --logs @$LOGS_SETTING_PATH `
#   --metrics @$METRICS_SETTING_PATH
#
# # Assign the "Log Analytics Contributor" role to the ACI principal ID
# az role assignment create `
#   --assignee $ACI_PRINCIPAL_ID `
#   --role "Log Analytics Contributor" `
#   --scope "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$LOG_ANALYTICS_RESOURCE_GROUP/providers/Microsoft.OperationalInsights/workspaces/$LOG_ANALYTICS_WORKSPACE_NAME"

# Step 12: Remove the auto-generated JSON config files after deployment
Remove-Item -Path $LOGIC_APP_DEFINITION_PATH -Force
# Remove-Item -Path $LOGS_SETTING_PATH -Force
# Remove-Item -Path $METRICS_SETTING_PATH -Force

# manually check logs from ACI (even if Logs Analytics is not configured)
# az container logs --resource-group $RESOURCE_GROUP --name $ACI_NAME