# Employee Roster

This is a simple website that shows employee office availablily by week and by location. 

## Services used 

* Microsoft Form  
* Microsoft Power Automate 
* [Sheety.co](https://sheety.co/)
* Generative AI (ChatGPT) to create the website in Javascript

## Learnings 

* Flowcharts can be created from code easily using the `mermaid` language they can be even rendered in a markdown document such as this one. There's also a powerful web-based editor called [**Mermaid Playground**](https://www.mermaidchart.com/play). 
* **Azure Storage Account** (blob) supports web hosting of static websites for very little cost (less than £1 per month)
* **Visual Studio Code** can be used to deploy the website directly to Azure using the free [**Azure Storage** extension](https://github.com/microsoft/vscode-azurestorage). 

## Flowchart

This flowchart illustrates the data flow through various tools and services. 

```mermaid
flowchart TB
    A(("Start")) --> B["User Submits<br>Microsoft Form"]
    B --> C["Microsoft Power Automate<br>Flow Triggered"]
    C --> D["Save Data<br>to SharePoint"] & E["Post HTTP<br>Request to Sheety"]
    G["Sheety Saves Data<br>to Google Sheets"] <--> n3["Website"]
    E --> G
    n5["Azure"] --- n6["Azure Storage Account<br>+ Enable Static Website"]
    n6 --> n3
    n9["GitHub"] <--> n7["Visual Studio Code <br>+ Azure Storage Extension"]
    n7 --> n6
    n10["Google <br>Drive"] --- G
    n5@{ shape: cyl}
    n7@{ shape: rect}
    n10@{ shape: cyl}
```
