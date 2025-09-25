# ----------------------------
# Outputs para facilitar integração
# ----------------------------

output "bucket_name" {
  description = "Nome do bucket criado."
  value       = google_storage_bucket.bucket_ons_dataset.name
}

output "artifact_registry_repo" {
  description = "Repositório do Artifact Registry."
  value       = google_artifact_registry_repository.repo_api_ons.repository_id
}

output "cloud_run_service_name" {
  description = "Nome do serviço Cloud Run."
  value       = google_cloud_run_v2_service.cloud_run_api.name
}

output "cloud_run_url" {
  description = "URL pública do Cloud Run."
  value       = google_cloud_run_v2_service.cloud_run_api.uri
}

output "bigquery_dataset_id" {
  description = "Dataset do BigQuery criado."
  value       = google_bigquery_dataset.bigquery_datawarehouse_ons.dataset_id
}
