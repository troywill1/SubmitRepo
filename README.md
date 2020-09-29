# Azure Infrastructure Operations Project: Deploying a scalable IaaS web server in Azure

### Introduction
For this project, you will write a Packer template and a Terraform template to deploy a customizable, scalable web server in Azure.

### Getting Started
1. Clone this repository

2. Create your infrastructure as code

3. Update this README to reflect how someone would use your code.

### Dependencies
1. Create an [Azure Account](https://portal.azure.com) 
2. Install the [Azure command line interface](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
3. Install [Packer](https://www.packer.io/downloads)
4. Install [Terraform](https://www.terraform.io/downloads.html)

### Instructions
There are three main steps to deploying this infrastructure in Azure:
- Define and assign an Azure tagging policy
- Build a Packer image to use in the infrastructure deployment
- Deploy the scalable IaaS web server in Azure with Terraform

#### Define and Assign Azure Policy
The file `azuretagpolicy.json` defines an Azure policy that requires all resources to contain at least one tag. When the infrastructure is deployed in Terraform, the user will be asked to define a tag to use with resource creation.

To define and assign the Azure policy, use the Azure Command Line Interface (CLI). From the directory where the `azuretagpolicy.json` file resides, execute the following commands:

	az policy definition create --name TaggingPolicy --rules azuretagpolicy.json
	az policy assignment create --policy TaggingPolicy

#### Build Packer Image
Packer uses a service principal to authenticate with Azure. Create a service principle and capture the credentials that Packer needs by using the Azure CLI:

	az ad sp create-for-rbac --query "{ client_id: appId, client_secret: password, tenant_id: tenant }"

Packer will also need the Azure subscription ID:

	az account show --query "{ subscription_id: id }"

With the captured credentials, create the following environment variables. The method in which environment variables are created and exported will vary by operating system. Reference operating system specific documentation, as needed.

Environment variables:

	ARM_CLIENT_ID
	ARM_CLIENT_SECRET
	ARM_SUBSCRIPTION_ID
	ARM_TENANT_ID

Note: A service principal and environment variables have already been created on this local system.

If one does not already exist, create an Azure resource group using the Azure CLI:

	az group create -n myPackerRG -l southcentralus

Edit the file `server.json` and modify it with the appropriate resource group name:

	"managed_image_resource_group_name": "myPackerRG"

The file `server.json` defines a template that Packer will use to create an image. This template creates a "Standard_DS2_v2" Azure virtual machine running "Ubuntu Server 18.04" and located in the "South Central US". The "Ubuntu Server 18.04" packages are updated, "nginx" is installed and an "index.html" is created for the application "busybox".

To build the Packer image, execute the following command from the directory where the file `server.json` exists:

	packer build server.json

When complete, Azure CLI can be used to list the images:

	az image list

#### Deploy the Infrastructure with Terraform
The scripts `main.tf`, `variables.tf` and `output.tf` comprise the Terraform template that will be used to deploy the web server infrastructure.

During execution, via the `variables.tf` script, the user will be prompted to provide the following details:

	Prefix - The prefix which should be used for all resources in this deployment.
	Location - The Azure Region in which all resources in this deployment should be created.
	Tag - The environment tag to use in this depoloyment.
	Machines - The number of virtual machines to create in this deployment.
	Username - The username for the Admin user.
	Password - The password for the Admin user.

Also, the `variables.tf` script contains a default port (80) to expose to the external load balancer. Edit this file directly to change the default port and/or add any other variables that may be needed.

The script `output.tf` will print to the screen the public IP assigned during deployment.

To deploy this infrastructure template with Terraform, execute the following command from the directory where the where the `*.tf` files are located:

	terraform init

This command ensures that Terraform has all of the prerequisites installed in this location to build the template.

Next, execute the following command to have Terraform review and validate the template, and output the planned execution. Azure resources are not created at this point:

	terraform plan -out solution.out

If the validation is successful, it's time to deploy the resources:

	terraform apply "solution.out"

Once Terraform completes, the web server infrastructure is ready.

### Output

#### Define and Assign Azure Policy Output

To view all policy definitions associated with your Azure subscription, execute the following Azure CLI command and note that each policy is returned in JSON format (example below):

	az policy definition list
	
	{
		"description": "This policy enables you to restrict the locations your organization can specify when deploying resources. Use to enforce your geo-compliance requirements.",
		"displayName": "Allowed locations",
		"id": "/providers/Microsoft.Authorization/policyDefinitions/e56962a6-4747-49cd-b67b-bf8b01975c4c",
		"name": "e56962a6-4747-49cd-b67b-bf8b01975c4c",
		"policyRule": {
			"if": {
				"not": {
					"field": "location",
					"in": "[parameters('listOfAllowedLocations')]"
				}
			},
			"then": {
				"effect": "Deny"
			}
		},
		"policyType": "BuiltIn"
	}

#### Build Packer Image Output

The Packer image build will result in output similar to below:

	packer build server.json
	
	azure-arm output will be in this color.
	
	==> azure-arm: Running builder ...
		azure-arm: Creating Azure Resource Manager (ARM) client ...
	==> azure-arm: Creating resource group ...
	==> azure-arm:  -> ResourceGroupName : ‘packer-Resource-Group-swtxmqm7ly’
	==> azure-arm:  -> Location          : ‘East US’
	==> azure-arm:  -> Tags              :
	==> azure-arm:  ->> dept : Engineering
	==> azure-arm:  ->> task : Image deployment
	==> azure-arm: Validating deployment template ...
	==> azure-arm:  -> ResourceGroupName : ‘packer-Resource-Group-swtxmqm7ly’
	==> azure-arm:  -> DeploymentName    : ‘pkrdpswtxmqm7ly’
	==> azure-arm: Deploying deployment template ...
	==> azure-arm:  -> ResourceGroupName : ‘packer-Resource-Group-swtxmqm7ly’
	==> azure-arm:  -> DeploymentName    : ‘pkrdpswtxmqm7ly’
	==> azure-arm: Getting the VM’s IP address ...
	==> azure-arm:  -> ResourceGroupName   : ‘packer-Resource-Group-swtxmqm7ly’
	==> azure-arm:  -> PublicIPAddressName : ‘packerPublicIP’
	==> azure-arm:  -> NicName             : ‘packerNic’
	==> azure-arm:  -> Network Connection  : ‘PublicEndpoint’
	==> azure-arm:  -> IP Address          : ‘40.76.218.147’
	==> azure-arm: Waiting for SSH to become available...
	==> azure-arm: Connected to SSH!
	==> azure-arm: Provisioning with shell script: /var/folders/h1/ymh5bdx15wgdn5hvgj1wc0zh0000gn/T/packer-shell868574263
		azure-arm: WARNING! The waagent service will be stopped.
		azure-arm: WARNING! Cached DHCP leases will be deleted.
		azure-arm: WARNING! root password will be disabled. You will not be able to login as root.
		azure-arm: WARNING! /etc/resolvconf/resolv.conf.d/tail and /etc/resolvconf/resolv.conf.d/original will be deleted.
		azure-arm: WARNING! packer account and entire home directory will be deleted.
	==> azure-arm: Querying the machine’s properties ...
	==> azure-arm:  -> ResourceGroupName : ‘packer-Resource-Group-swtxmqm7ly’
	==> azure-arm:  -> ComputeName       : ‘pkrvmswtxmqm7ly’
	==> azure-arm:  -> Managed OS Disk   : ‘/subscriptions/guid/resourceGroups/packer-Resource-Group-swtxmqm7ly/providers/Microsoft.Compute/disks/osdisk’
	==> azure-arm: Powering off machine ...
	==> azure-arm:  -> ResourceGroupName : ‘packer-Resource-Group-swtxmqm7ly’
	==> azure-arm:  -> ComputeName       : ‘pkrvmswtxmqm7ly’
	==> azure-arm: Capturing image ...
	==> azure-arm:  -> Compute ResourceGroupName : ‘packer-Resource-Group-swtxmqm7ly’
	==> azure-arm:  -> Compute Name              : ‘pkrvmswtxmqm7ly’
	==> azure-arm:  -> Compute Location          : ‘East US’
	==> azure-arm:  -> Image ResourceGroupName   : ‘myResourceGroup’
	==> azure-arm:  -> Image Name                : ‘myPackerImage’
	==> azure-arm:  -> Image Location            : ‘eastus’
	==> azure-arm: Deleting resource group ...
	==> azure-arm:  -> ResourceGroupName : ‘packer-Resource-Group-swtxmqm7ly’
	==> azure-arm: Deleting the temporary OS disk ...
	==> azure-arm:  -> OS Disk : skipping, managed disk was used...
	Build ‘azure-arm’ finished.
	
	==> Builds finished. The artifacts of successful builds are:
	--> azure-arm: Azure.ResourceManagement.VMImage:
	
	ManagedImageResourceGroupName: myResourceGroup
	ManagedImageName: myPackerImage
	ManagedImageLocation: eastus

#### Deploy the Infrastructure with Terraform Output

The Terraform plan command will return output similar to the following:

	terraform plan -out solution.out
	
	+ guid                = (known after apply)
		  + id                  = (known after apply)
		  + location            = "southcentralus"
		  + name                = "jumbo-network"
		  + resource_group_name = "jumbo-resources"
		  + subnet              = (known after apply)
		  + tags                = {
			  + "environment" = "webproject"
			}
		}
	
	Plan: 14 to add, 0 to change, 0 to destroy.
	
	Changes to Outputs:
	  + main_public_ip = (known after apply)
	
	------------------------------------------------------------------------
	
	This plan was saved to: solution.out
	
	To perform exactly these actions, run the following command to apply:
		terraform apply "solution.out"

The Terraform apply command will resemble the output below:

	terraform apply "solution.out"
	
	azurerm_linux_virtual_machine.main[0]: Still creating... [1m0s elapsed]
	azurerm_linux_virtual_machine.main[0]: Still creating... [1m10s elapsed]
	azurerm_linux_virtual_machine.main[1]: Still creating... [1m10s elapsed]
	azurerm_linux_virtual_machine.main[0]: Still creating... [1m20s elapsed]
	azurerm_linux_virtual_machine.main[1]: Still creating... [1m20s elapsed]
	azurerm_linux_virtual_machine.main[1]: Still creating... [1m30s elapsed]
	azurerm_linux_virtual_machine.main[0]: Still creating... [1m30s elapsed]
	azurerm_linux_virtual_machine.main[1]: Creation complete after 1m40s [id=/subscriptions/b2460104-2c2c-4cdd-a39d-622e30043911/resourceGroups/jumbo-resources/providers/Microsoft.Compute/virtualMachines/jumbo-vm-1]
	azurerm_linux_virtual_machine.main[0]: Still creating... [1m40s elapsed]
	azurerm_linux_virtual_machine.main[0]: Creation complete after 1m40s [id=/subscriptions/b2460104-2c2c-4cdd-a39d-622e30043911/resourceGroups/jumbo-resources/providers/Microsoft.Compute/virtualMachines/jumbo-vm-0]
	
	Apply complete! Resources: 14 added, 0 changed, 0 destroyed.
	
	The state of your infrastructure has been saved to the path
	below. This state is required to modify and destroy your
	infrastructure, so keep it safe. To inspect the complete state
	use the `terraform show` command.
	
	State path: terraform.tfstate

