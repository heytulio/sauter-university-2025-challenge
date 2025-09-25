# ----------------------------
# Storage Bucket
# ----------------------------
resource "google_storage_bucket" "bucket_ons_dataset" {
  name          = var.bucket_name
  location      = var.region
  force_destroy = false
}

# ----------------------------
# Artifact Registry
# ----------------------------
resource "google_artifact_registry_repository" "repo_api_ons" {
  location      = var.region
  repository_id = var.artifact_repo_id
  description   = "Docker repository for CI/CD pipeline"
  format        = "DOCKER"

  cleanup_policies {
    id     = "keep-minimum-versions"
    action = "KEEP"
    most_recent_versions {
      keep_count            = 3
    }
  }

}

# ----------------------------
# Cloud Run Service
# ----------------------------
resource "google_cloud_run_v2_service" "cloud_run_api" {
  name     = var.cloud_run_service_name
  location = var.region

  template {
    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.repo_api_ons.repository_id}/my-app:latest"
    }
  }
}

# Permitir acesso público à API
resource "google_cloud_run_v2_service_iam_member" "public_access" {
  project  = var.project_id
  location = var.region
  service  = google_cloud_run_v2_service.cloud_run_api.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# ----------------------------
# BigQuery Dataset
# ----------------------------
resource "google_bigquery_dataset" "bigquery_datawarehouse_ons" {
  dataset_id    = var.bigquery_dataset_id
  friendly_name = "My Application Dataset"
  description   = "Dataset for application data and logs."
  location      = var.bigquery_location
}