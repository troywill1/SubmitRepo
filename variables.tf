variable "prefix" {
  description = "The prefix which should be used for all resources in this deployment."
}

variable "location" {
  description = "The Azure Region in which all resources in this deployment should be created."
}

variable "tag" {
  description = "The environment tag to use in this depoloyment."
}

variable "machines" {
  description = "The number of virtual machines to create in this deployment."
}

variable "username" {
    description = "The username for the Admin user."
}

variable "password" {
    description = "The password for the Admin user."
}

variable "application_port" {
    description = "The port that you want to expose to the external load balancer."
    default     = 80
}

variable "project_name" {
    description = "The project name tag to be applied to the virtual machines."
    default     = "webproject"
}