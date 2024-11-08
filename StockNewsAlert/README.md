# Stock News SMS Alert

Sends me a text if the stock price of Tesla (TSLA) increased or decreased by at least five percent. 

### My learnings from this project

* If you're running a Python application from a Docker image then you can use the same code that you'd run to run the app locally (no Azure decorators are needed). However, if want to deploy it with Azure App Services, you'd need to make some changes.
* You can check the latest log from your Azure Container instance with this command:
```powershell
$RESOURCE_GROUP="StockAlertApp"
$ACI_NAME="news-alert-app-container"
az container logs --resource-group $RESOURCE_GROUP --name $ACI_NAME

```
*  

### Architecture 

#### APIs

* **Twilio API** for sending text messages
* **Alpha Vantage API** for checking the stock prices
* **News API** for checking news

#### Deployment 

* **Azure Key Vault** for storing and retrieving API secrets
* **Azure Container Registry** for storing Docker images
* **Azure Container Instance** for running Docker images
* **Azure Logic App** for job scheduling


### #TODO

* 