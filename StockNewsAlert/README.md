# Stock News SMS Alert

Sends me a text if the stock price of Tesla (TSLA) increased or decreased by at least five percent. 

### My learnings from this project

* I'm using several Resources for this project but the most expensive one is Azure Container Registry at £0.13 per day. 
* If you run a Python application from a Docker image then you can use the same code that you'd use to run the app locally (no Azure decorators are needed). However, if you want to deploy it with Azure App Services, you'd need to make some changes.
* You can check the latest log from your Azure Container instance with this command even without a Log Analytics workspace:
```powershell
$RESOURCE_GROUP="StockAlertApp"
$ACI_NAME="news-alert-app-container"
az container logs --resource-group $RESOURCE_GROUP --name $ACI_NAME

```
* API secrets can be passed to your app running inside an Azure Container Instance as `--environment-variables` but this will make the secrets easily visible in Azure Portal for anyone (with access to your portal) to see. There are two solutions: (a) use `--secure-environment-variables`; or (b) skip environment variables and have your Python app retrieve the secrets directly from your Azure Key Vault.  
* Azure Key Vaults need to be purged to be permanently deleted. Deleting the Resource Group which contains the Azure Key Vault instance will delete it, but it will still exist and if you try to recreate it you'll get an error.
```powershell
az keyvault purge --name StockAlertAppKeyVault --location westeurope
```
* Your Resources must often be assigned explicit privileges before being able to talk to each other, even if they're in the same Resource Group. Assigning Resource privileges can be done in several ways including: (a) creating resource identity which creates an ID and assigning specific privileges from another Resource to that ID; (b) creating and assigning roles to resources (e.g. "Contributor"); ... . 

### Architecture 

#### APIs

* **[Twilio API](https://www.twilio.com/docs)** for sending text messages
* **[Alpha Vantage API](https://www.alphavantage.co/documentation/)** for checking the stock prices
* **[News API](https://newsapi.org/)** for checking news

#### Deployment 

* **Azure Key Vault** for storing and retrieving API secrets
* **Azure Container Registry** for storing Docker images
* **Azure Container Instance** for running Docker images
* **Azure Logic App** for job scheduling


### #TODO

* 