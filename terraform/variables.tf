# ----------------------------
# Variáveis de configuração
# ----------------------------

variable "project_id" {
  description = "O ID do projeto na GCP."
  type        = string
}

variable "region" {
  description = "A região onde os recursos serão criados."
  type        = string
  default     = "us-central1"
}

variable "bucket_name" {
  description = "Nome único global para o bucket de Cloud Storage."
  type        = string
}

variable "artifact_repo_id" {
  description = "O ID para o repositório no Artifact Registry."
  type        = string
  default     = "repo-api-ons"
}

variable "cloud_run_service_name" {
  description = "Nome para o serviço no Cloud Run (apenas letras minúsculas e hífens)."
  type        = string
  default     = "api-cloud-run"
}

variable "bigquery_dataset_id" {
  description = "O ID do dataset do BigQuery."
  type        = string
  default     = "ons_dataset"
}

variable "bigquery_location" {
  description = "Localização do BigQuery (ex.: US, EU, us-central1)."
  type        = string
  default     = "US"
}

variable "bigquery_dataset_dashboard_id" {
  description = "ID do Dataset do BigQuery para o dashboard."
  type        = string
  default     = "bq_dataset_dashboard"
}
