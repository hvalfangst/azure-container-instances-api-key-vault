# Flask API with Azure Key Vault deployed to Azure Container Instances

Flask API deployed to Azure Container Instances. Secrets
are fetched from Azure Key Vault and mounted as environment variables in the container.
A CI/CD pipeline has been implemented which enables automatic deployment to ACI.
All resources are provisioned with Terraform.

## Requirements

* x86-64
* Linux/Unix
* [Python](https://www.python.org/downloads/)
* [Docker](https://www.docker.com/products/docker-desktop/)

## Creating resources

The shell script 'up' allocates Azure resources with Terraform.

## Deleting resources

The shell script 'down' deallocates Azure resources.

## Guide

### 1. Provision Azure Resources

- Run the 'up' script to provision Azure resources.

### 2. Access Azure Portal

- Open your browser and navigate to the Azure Portal.

### 3. Container Registry Setup

- Go to the newly provisioned Container Registry named 'hvalfangstcontainerregistry'.
- Click on 'Access keys' under the 'Settings' section.
- Store the registry name and password for future use.

### 4. Get storage account access key

Run the following command to retrieve the keys associated with your storage account. Store the first key.
We will be pushing a secret containing the first key to Azure Key Vault later.
~~~
az storage account keys list --resource-group hvalfangstresourcegroup --account-name hvalfangststorageaccount --output json
~~~

### 4. Create service principal

We will utilize a service principle as identification.

Run the following command to create SP with display name 'hvalfangst'. Make sure to store the JSON response for later use.
~~~
az ad sp create-for-rbac --name hvalfangst
~~~

### 5. Grant subscription contributor role to our SP

Our Service Principal needs access to our resources, role assignment and will be responsible for provision resources.
As such, it needs the 'Contributor' role. 

Execute the following command to give our SP Contributor access to our subscription.
~~~
az role assignment create --assignee {SP_ID} --role Contributor --scope /subscriptions/{YOUR_SUBSCRIPTION}
~~~


### 6: Grant key vault secrets reader role to our SP
In order for applications to read secrets from Key Vault on behalf of our SP we need a specific role.
Execute the following to give our SP the 'get secrets' role. The ID of our SP was obtained in step #4.
~~~
az keyvault set-policy --name hvalfangstkeyvault --resource-group hvalfangstresourcegroup --secret-permissions get --spn {SP_ID}
~~~

### 7: Set new secret containing storage account key
In order for our container to be able to communicate with Azure Table Storage, it needs an access key.
Since we are mounting environment variables onto the container from Azure Key Vault, we
need to first store the desired secret.

Execute the following command to create a new secret in Azure Key Vault with name set to 'storage-account-key' and value set to our 
storage account access key retrieved in step #4.
~~~
az keyvault secret set --name storage-account-key --value {ACCESS_KEY} --vault-name hvalfangstkeyvault
~~~

### 8. GitHub Repository Secrets

- Open the 'Settings' tab of your GitHub repository.
- Click on 'Actions' under 'Security' -> 'Secrets and variables'.
- Create the following repository secrets:
    - ACR_USERNAME: Value stored in step #3
    - ACR_PASSWORD: Value stored in step #3
    - AZURE_CLIENT_ID: Value stored in step #4
    - AZURE_TENANT_ID: Value stored in step #4
    - AZURE_CLIENT_SECRET: Value stored in step #4

### CI/CD Pipeline

A GitHub Actions Workflow has been integrated with this repository. Once triggered, it will: 
1. Login to Azure utilizing our Service Principal.
2. Get secret 'storage-account-key' from Azure Key Vault.
3. Login to Azure Container Registry with our basic credentials.
4. Build our docker image with the 'storage-account-key' key mounted as environment variable.
5. Deploy the image to Azure Container Instances.