terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 2.49"
    }
  }

  backend "azurerm" {
    resource_group_name  = "SoftwirePilot_JoannaCheng_ProjectExercise"
    storage_account_name = "joachetstate"
    container_name       = "joachetstate"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "main" {
  name = var.resource_group_name
}

resource "azurerm_app_service_plan" "main" {
  name                = "${var.prefix}-terraformed-asp"
  location            = var.location
  resource_group_name = data.azurerm_resource_group.main.name
  kind                = "Linux"
  reserved            = true

  sku {
    tier = "Basic"
    size = "B1"
  }
}

resource "azurerm_app_service" "main" {
  name                = "${var.prefix}-terraformed-todo-app-joache"
  location            = var.location
  resource_group_name = data.azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.main.id

  site_config {
    app_command_line = ""
    linux_fx_version = "DOCKER|chengjoanna1729/todo-app:latest"
  }

  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "DB_CONNECTION_STRING"       = "mongodb://${azurerm_cosmosdb_account.main.name}:${azurerm_cosmosdb_account.main.primary_key}@${azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255/DefaultDatabase?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000"
    "COLLECTION_NAME"            = azurerm_cosmosdb_mongo_database.main.name
  }
}

resource "azurerm_cosmosdb_account" "main" {
  name                = "${var.prefix}-terraformed-cosmosdb-account"
  resource_group_name = data.azurerm_resource_group.main.name
  location            = var.location
  offer_type          = "Standard"
  kind                = "MongoDB"

  geo_location {
    failover_priority = 0
    location          = var.location
  }

  consistency_policy {
    consistency_level = "Session"
  }

  capabilities {
    name = "EnableServerless"
  }


  capabilities {
    name = "EnableMongo"
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "${var.prefix}-todos"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
}
