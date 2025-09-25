# Configura o provedor (provider) do Google Cloud,
# que é a "ponte" entre o Terraform e a sua conta GCP.
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.0" # Usamos uma versão recente do provedor
    }
  }
}

# Define as configurações de autenticação e do projeto
# que serão usadas para todos os recursos.
provider "google" {
  project     = var.project_id
  region      = var.region
}
