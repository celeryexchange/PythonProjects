az group delete --name StockAlertApp --yes
# az keyvault list-deleted
az keyvault purge --name StockAlertAppKeyVault --location westeurope
