variable "prefix" {
  description = "The prefix used for all resources in this environment"
}

variable "location" {
  description = "The Azure location where all resources in this deployment should be created"
  default     = "uksouth"
}

variable "resource_group_name" {
  description = "The name of the resource group to use"
  default     = "SoftwirePilot_JoannaCheng_ProjectExercise"
}
