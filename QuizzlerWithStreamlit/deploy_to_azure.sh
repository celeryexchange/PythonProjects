# source: https://towardsdatascience.com/deploying-a-streamlit-web-app-with-azure-app-service-1f09a2159743

# code assumes you're using Azure CLI and Powershell and are already logged in 
# az login

# Variables
$RESOURCE_GROUP="QuizzlerApp"
$LOCATION="westeurope"
$APP_NAME="QuizzlerApp"
$CONTAINER_REGISTRY_NAME="quizzlerappregistry"
$CONTAINER_REGISTRY_SKU="basic"
$DOCKER_IMAGE_NAME="quizzler-app"
$PLAN_NAME="QuizzlerAppServicePlan"
$PLAN_SKU="F1" # F1: free 60 mins/day
$WEBAPP_NAME="quizzler-web-app"

# Step 1: Create a Resource Group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Step 2: Create an Azure Container Registry (for Docker image)
az acr create --name $CONTAINER_REGISTRY_NAME --resource-group $RESOURCE_GROUP --sku $CONTAINER_REGISTRY_SKU --admin-enabled true 

# Step 3: Build a Docker image and save it to Azure Container Registry
az acr build --registry $CONTAINER_REGISTRY_NAME --resource-group $RESOURCE_GROUP --image $DOCKER_IMAGE_NAME

# Step 4: Create an App Service Plan for your web app
az appservice plan create -n $PLAN_NAME -g $RESOURCE_GROUP -l $LOCATION --is-linux --sku $PLAN_SKU

# Step 5: Deploy a Web App from a Docker image 
az webapp create -g $RESOURCE_GROUP -p $PLAN_NAME -n $WEBAPP_NAME -i $CONTAINER_REGISTRY_NAME.azurecr.io/$DOCKER_IMAGE_NAME:latest

# Step 6: Output Web App URL
$WEBAPP_URL=$(az webapp show --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP --query defaultHostName --output tsv)
echo "Web App is deployed to: http://$WEBAPP_URL"