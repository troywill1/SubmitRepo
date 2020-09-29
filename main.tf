provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "main" {
  name     = "${var.prefix}-resources"
  location = var.location
  
  tags = {
    environment = var.tag
  }
}

resource "azurerm_public_ip" "main" {
  name                = "${var.prefix}-PublicIp1"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  allocation_method   = "Dynamic"
  
  tags = {
    environment = var.tag
  }
}

resource "azurerm_virtual_network" "main" {
  name                = "${var.prefix}-network"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  
  tags = {
    environment = var.tag
  }
}

resource "azurerm_subnet" "main" {
  name                 = "${var.prefix}-internal-net"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.2.0/24"]
}

resource "azurerm_network_security_group" "main" {
    name                = "${var.prefix}-NetworkSecurityGroup"
    location            = azurerm_resource_group.main.location
    resource_group_name = azurerm_resource_group.main.name
    
    security_rule {
        name                       = "Internet"
        priority                   = 200
        direction                  = "Inbound"
        access                     = "Deny"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "*"
        source_address_prefix      = "Internet"
        destination_address_prefix = "10.0.2.0/24"
    }
    
    security_rule {
        name                       = "VMs"
        priority                   = 500
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "*"
        source_address_prefix      = "10.0.2.0/24"
        destination_address_prefix = "10.0.2.0/24"
    }

    tags = {
        environment = var.tag
    }
}

resource "azurerm_network_interface" "main" {
  count               = var.machines
  name                = "${var.prefix}-nic-${count.index}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Dynamic"
  }
  
  tags = {
    environment = var.tag
  }
}

resource "azurerm_lb" "main" {
  name                = "${var.prefix}-main-lb"
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name

  frontend_ip_configuration {
    name                 = "PublicIPAddress"
    public_ip_address_id = azurerm_public_ip.main.id
  }

  tags = {
    environment = var.tag
  }
}

resource "azurerm_lb_backend_address_pool" "bpepool" {
  resource_group_name = azurerm_resource_group.main.name
  loadbalancer_id     = azurerm_lb.main.id
  name                = "BackEndAddressPool"
}

resource "azurerm_lb_probe" "main" {
  resource_group_name = azurerm_resource_group.main.name
  loadbalancer_id     = azurerm_lb.main.id
  name                = "ssh-running-probe"
  port                = var.application_port
}

resource "azurerm_lb_rule" "lbnatrule" {
  resource_group_name            = azurerm_resource_group.main.name
  loadbalancer_id                = azurerm_lb.main.id
  name                           = "http"
  protocol                       = "Tcp"
  frontend_port                  = var.application_port
  backend_port                   = var.application_port
  backend_address_pool_id        = azurerm_lb_backend_address_pool.bpepool.id
  frontend_ip_configuration_name = "PublicIPAddress"
  probe_id                       = azurerm_lb_probe.main.id
}

resource "azurerm_availability_set" "main" {
  name                = "${var.prefix}-availability-set"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  tags = {
    environment = var.tag
  }
}

data "azurerm_resource_group" "image" {
  name = "myPackerRG"
}

data "azurerm_image" "image" {
  name                = "myPackerImage3"
  resource_group_name = data.azurerm_resource_group.image.name
}

resource "azurerm_linux_virtual_machine" "main" {
  count                           = var.machines
  name                            = "${var.prefix}-vm-${count.index}"
  resource_group_name             = azurerm_resource_group.main.name
  location                        = azurerm_resource_group.main.location
  size                            = "Standard_D2S_v3"
  
  admin_username                  = var.username
  admin_password                  = var.password
  disable_password_authentication = false
  
  network_interface_ids = [
  "${element(azurerm_network_interface.main.*.id, count.index)}",
  ]
  
  os_disk {
    name                    = "${var.prefix}-vm-${count.index}-os-disk"
    caching                 = "ReadWrite"
    storage_account_type    = "Standard_LRS"
  }

  source_image_id = data.azurerm_image.image.id
  
  availability_set_id = azurerm_availability_set.main.id
  
  tags = {
    environment = var.tag
  }
}