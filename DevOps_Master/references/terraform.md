# Terraform Reference Guide

Comprehensive guide for Infrastructure as Code using Terraform across AWS, GCP, and Azure with best practices for multi-cloud deployments.

## Table of Contents
1. [Module Design](#module-design)
2. [State Management](#state-management)
3. [Multi-Cloud Modules](#multi-cloud-modules)
4. [AWS Resources](#aws-resources)
5. [GCP Resources](#gcp-resources)
6. [Azure Resources](#azure-resources)
7. [Variables and Outputs](#variables-and-outputs)
8. [Cost Optimization](#cost-optimization)
9. [Security Best Practices](#security-best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Module Design

### Module Structure

```
terraform-modules/
├── vpc/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── versions.tf
│   └── README.md
├── eks/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── versions.tf
└── rds/
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    └── versions.tf
```

### Basic Module Pattern

```hcl
# modules/vpc/main.tf
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = var.enable_dns_hostnames
  enable_dns_support   = var.enable_dns_support

  tags = merge(
    var.tags,
    {
      Name = var.vpc_name
    }
  )
}

resource "aws_subnet" "public" {
  count                   = length(var.public_subnet_cidrs)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = merge(
    var.tags,
    {
      Name = "${var.vpc_name}-public-${count.index + 1}"
      Type = "public"
    }
  )
}

resource "aws_subnet" "private" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = merge(
    var.tags,
    {
      Name = "${var.vpc_name}-private-${count.index + 1}"
      Type = "private"
    }
  )
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    var.tags,
    {
      Name = "${var.vpc_name}-igw"
    }
  )
}

resource "aws_eip" "nat" {
  count  = var.enable_nat_gateway ? length(var.public_subnet_cidrs) : 0
  domain = "vpc"

  tags = merge(
    var.tags,
    {
      Name = "${var.vpc_name}-nat-eip-${count.index + 1}"
    }
  )
}

resource "aws_nat_gateway" "main" {
  count         = var.enable_nat_gateway ? length(var.public_subnet_cidrs) : 0
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = merge(
    var.tags,
    {
      Name = "${var.vpc_name}-nat-${count.index + 1}"
    }
  )

  depends_on = [aws_internet_gateway.main]
}
```

```hcl
# modules/vpc/variables.tf
variable "vpc_name" {
  description = "Name of the VPC"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "Must be a valid CIDR block."
  }
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
}

variable "enable_nat_gateway" {
  description = "Enable NAT Gateway for private subnets"
  type        = bool
  default     = true
}

variable "enable_dns_hostnames" {
  description = "Enable DNS hostnames in VPC"
  type        = bool
  default     = true
}

variable "enable_dns_support" {
  description = "Enable DNS support in VPC"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
```

```hcl
# modules/vpc/outputs.tf
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs of private subnets"
  value       = aws_subnet.private[*].id
}

output "nat_gateway_ids" {
  description = "IDs of NAT Gateways"
  value       = aws_nat_gateway.main[*].id
}
```

### Using Modules

```hcl
# main.tf
module "vpc" {
  source = "./modules/vpc"

  vpc_name             = "production-vpc"
  vpc_cidr             = "10.0.0.0/16"
  availability_zones   = ["us-east-1a", "us-east-1b", "us-east-1c"]
  public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnet_cidrs = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]
  enable_nat_gateway   = true

  tags = {
    Environment = "production"
    Project     = "myapp"
    ManagedBy   = "terraform"
  }
}

# Use module outputs
resource "aws_security_group" "app" {
  vpc_id = module.vpc.vpc_id
  # ...
}
```

---

## State Management

### Local Backend (Development Only)

```hcl
# terraform.tf
terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}
```

### Remote Backend - S3 (Recommended for AWS)

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-locks"
    
    # Use IAM role for authentication
    # role_arn = "arn:aws:iam::123456789012:role/TerraformStateRole"
  }
}
```

**Setup S3 Backend:**
```hcl
# bootstrap/main.tf
resource "aws_s3_bucket" "terraform_state" {
  bucket = "my-terraform-state-bucket"

  lifecycle {
    prevent_destroy = true
  }

  tags = {
    Name        = "Terraform State"
    Environment = "production"
  }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-state-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name        = "Terraform State Locks"
    Environment = "production"
  }
}
```

### Remote Backend - GCS (For GCP)

```hcl
terraform {
  backend "gcs" {
    bucket = "my-terraform-state-bucket"
    prefix = "production/terraform.tfstate"
  }
}
```

### Remote Backend - Azure Storage

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfstateaccount"
    container_name       = "tfstate"
    key                  = "production.terraform.tfstate"
  }
}
```

### Workspaces

```bash
# Create workspace
terraform workspace new staging

# List workspaces
terraform workspace list

# Switch workspace
terraform workspace select production

# Show current workspace
terraform workspace show

# Delete workspace
terraform workspace delete staging
```

**Using Workspaces in Code:**
```hcl
locals {
  environment = terraform.workspace
  
  instance_counts = {
    default    = 1
    staging    = 2
    production = 5
  }
  
  instance_count = lookup(local.instance_counts, local.environment, 1)
}

resource "aws_instance" "app" {
  count         = local.instance_count
  instance_type = local.environment == "production" ? "t3.large" : "t3.micro"
  # ...
}
```

---

## Multi-Cloud Modules

### Cloud-Agnostic VPC Module

```hcl
# modules/network/variables.tf
variable "cloud_provider" {
  description = "Cloud provider (aws, gcp, azure)"
  type        = string
  validation {
    condition     = contains(["aws", "gcp", "azure"], var.cloud_provider)
    error_message = "Must be aws, gcp, or azure."
  }
}

variable "network_cidr" {
  description = "CIDR block for network"
  type        = string
}

variable "region" {
  description = "Cloud region"
  type        = string
}

# modules/network/main.tf
# AWS VPC
resource "aws_vpc" "main" {
  count      = var.cloud_provider == "aws" ? 1 : 0
  cidr_block = var.network_cidr

  tags = {
    Name = "${var.network_name}-vpc"
  }
}

# GCP VPC
resource "google_compute_network" "main" {
  count                   = var.cloud_provider == "gcp" ? 1 : 0
  name                    = "${var.network_name}-vpc"
  auto_create_subnetworks = false
}

# Azure VNet
resource "azurerm_virtual_network" "main" {
  count               = var.cloud_provider == "azure" ? 1 : 0
  name                = "${var.network_name}-vnet"
  address_space       = [var.network_cidr]
  location            = var.region
  resource_group_name = var.resource_group_name
}

# modules/network/outputs.tf
output "network_id" {
  description = "Network ID"
  value = var.cloud_provider == "aws" ? aws_vpc.main[0].id : (
    var.cloud_provider == "gcp" ? google_compute_network.main[0].id : (
      azurerm_virtual_network.main[0].id
    )
  )
}
```

### Cloud-Agnostic Kubernetes Cluster

```hcl
# modules/kubernetes/main.tf
# AWS EKS
module "eks" {
  count   = var.cloud_provider == "aws" ? 1 : 0
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = var.cluster_name
  cluster_version = var.kubernetes_version

  vpc_id     = var.vpc_id
  subnet_ids = var.subnet_ids

  eks_managed_node_groups = {
    default = {
      desired_size = var.node_count
      min_size     = var.min_node_count
      max_size     = var.max_node_count

      instance_types = [var.node_instance_type]
    }
  }
}

# GCP GKE
resource "google_container_cluster" "main" {
  count    = var.cloud_provider == "gcp" ? 1 : 0
  name     = var.cluster_name
  location = var.region

  remove_default_node_pool = true
  initial_node_count       = 1
}

resource "google_container_node_pool" "main" {
  count      = var.cloud_provider == "gcp" ? 1 : 0
  name       = "${var.cluster_name}-node-pool"
  cluster    = google_container_cluster.main[0].name
  location   = var.region
  node_count = var.node_count

  node_config {
    machine_type = var.node_instance_type
  }
}

# Azure AKS
resource "azurerm_kubernetes_cluster" "main" {
  count               = var.cloud_provider == "azure" ? 1 : 0
  name                = var.cluster_name
  location            = var.region
  resource_group_name = var.resource_group_name
  dns_prefix          = var.cluster_name

  default_node_pool {
    name       = "default"
    node_count = var.node_count
    vm_size    = var.node_instance_type
  }

  identity {
    type = "SystemAssigned"
  }
}
```

---

## AWS Resources

### EKS Cluster

```hcl
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "production-cluster"
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids

  # Cluster endpoint access
  cluster_endpoint_public_access  = true
  cluster_endpoint_private_access = true

  # Cluster addons
  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
    aws-ebs-csi-driver = {
      most_recent = true
    }
  }

  # Managed node groups
  eks_managed_node_groups = {
    general = {
      desired_size = 3
      min_size     = 2
      max_size     = 10

      instance_types = ["t3.large"]
      capacity_type  = "ON_DEMAND"

      labels = {
        role = "general"
      }

      tags = {
        Environment = "production"
      }
    }

    spot = {
      desired_size = 2
      min_size     = 0
      max_size     = 5

      instance_types = ["t3.large", "t3a.large"]
      capacity_type  = "SPOT"

      labels = {
        role = "spot"
      }

      taints = [{
        key    = "spot"
        value  = "true"
        effect = "NoSchedule"
      }]
    }
  }

  # Cluster security group rules
  cluster_security_group_additional_rules = {
    ingress_nodes_ephemeral_ports_tcp = {
      description                = "Nodes on ephemeral ports"
      protocol                   = "tcp"
      from_port                  = 1025
      to_port                    = 65535
      type                       = "ingress"
      source_node_security_group = true
    }
  }

  # Node security group rules
  node_security_group_additional_rules = {
    ingress_self_all = {
      description = "Node to node all ports/protocols"
      protocol    = "-1"
      from_port   = 0
      to_port     = 0
      type        = "ingress"
      self        = true
    }
  }

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
  }
}
```

### RDS Database

```hcl
resource "aws_db_instance" "main" {
  identifier     = "production-db"
  engine         = "postgres"
  engine_version = "15.3"

  instance_class    = "db.t3.large"
  allocated_storage = 100
  storage_type      = "gp3"
  storage_encrypted = true
  kms_key_id        = aws_kms_key.rds.arn

  db_name  = "myapp"
  username = "admin"
  password = random_password.db_password.result

  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  multi_az               = true
  publicly_accessible    = false
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  deletion_protection = true
  skip_final_snapshot = false
  final_snapshot_identifier = "production-db-final-snapshot"

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
  }
}

resource "random_password" "db_password" {
  length  = 32
  special = true
}

resource "aws_secretsmanager_secret" "db_password" {
  name = "production/db/password"
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = random_password.db_password.result
}
```

### ElastiCache Redis

```hcl
resource "aws_elasticache_replication_group" "main" {
  replication_group_id       = "production-redis"
  replication_group_description = "Production Redis cluster"

  engine               = "redis"
  engine_version       = "7.0"
  node_type            = "cache.t3.medium"
  num_cache_clusters   = 2
  parameter_group_name = "default.redis7"

  port                       = 6379
  subnet_group_name          = aws_elasticache_subnet_group.main.name
  security_group_ids         = [aws_security_group.redis.id]
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  auth_token                 = random_password.redis_auth.result

  automatic_failover_enabled = true
  multi_az_enabled           = true

  snapshot_retention_limit = 5
  snapshot_window          = "03:00-05:00"
  maintenance_window       = "sun:05:00-sun:07:00"

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
  }
}
```

### S3 Bucket

```hcl
resource "aws_s3_bucket" "app_data" {
  bucket = "myapp-production-data"

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
  }
}

resource "aws_s3_bucket_versioning" "app_data" {
  bucket = aws_s3_bucket.app_data.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "app_data" {
  bucket = aws_s3_bucket.app_data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.s3.arn
    }
  }
}

resource "aws_s3_bucket_public_access_block" "app_data" {
  bucket = aws_s3_bucket.app_data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "app_data" {
  bucket = aws_s3_bucket.app_data.id

  rule {
    id     = "transition-to-ia"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }
  }
}
```

---

## GCP Resources

### GKE Cluster

```hcl
resource "google_container_cluster" "main" {
  name     = "production-cluster"
  location = "us-central1"

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count       = 1

  network    = google_compute_network.main.id
  subnetwork = google_compute_subnetwork.main.id

  # Enable Workload Identity
  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  # Enable network policy
  network_policy {
    enabled = true
  }

  # Enable binary authorization
  binary_authorization {
    evaluation_mode = "PROJECT_SINGLETON_POLICY_ENFORCE"
  }

  # Maintenance window
  maintenance_policy {
    daily_maintenance_window {
      start_time = "03:00"
    }
  }

  # Monitoring and logging
  logging_config {
    enable_components = ["SYSTEM_COMPONENTS", "WORKLOADS"]
  }

  monitoring_config {
    enable_components = ["SYSTEM_COMPONENTS"]
    managed_prometheus {
      enabled = true
    }
  }
}

resource "google_container_node_pool" "primary" {
  name       = "primary-pool"
  location   = "us-central1"
  cluster    = google_container_cluster.main.name
  node_count = 3

  autoscaling {
    min_node_count = 2
    max_node_count = 10
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }

  node_config {
    preemptible  = false
    machine_type = "n1-standard-2"

    # Google recommends custom service accounts
    service_account = google_service_account.gke_nodes.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    labels = {
      env = "production"
    }

    tags = ["gke-node", "production"]

    metadata = {
      disable-legacy-endpoints = "true"
    }
  }
}
```

### Cloud SQL

```hcl
resource "google_sql_database_instance" "main" {
  name             = "production-db"
  database_version = "POSTGRES_15"
  region           = "us-central1"

  settings {
    tier              = "db-custom-2-7680"
    availability_type = "REGIONAL"
    disk_type         = "PD_SSD"
    disk_size         = 100
    disk_autoresize   = true

    backup_configuration {
      enabled                        = true
      start_time                     = "03:00"
      point_in_time_recovery_enabled = true
      transaction_log_retention_days = 7
      backup_retention_settings {
        retained_backups = 7
      }
    }

    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.main.id
      require_ssl     = true
    }

    maintenance_window {
      day          = 7
      hour         = 3
      update_track = "stable"
    }

    database_flags {
      name  = "max_connections"
      value = "100"
    }
  }

  deletion_protection = true
}

resource "google_sql_database" "main" {
  name     = "myapp"
  instance = google_sql_database_instance.main.name
}

resource "google_sql_user" "main" {
  name     = "admin"
  instance = google_sql_database_instance.main.name
  password = random_password.db_password.result
}
```

### Cloud Storage

```hcl
resource "google_storage_bucket" "app_data" {
  name          = "myapp-production-data"
  location      = "US"
  storage_class = "STANDARD"

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
  }

  encryption {
    default_kms_key_name = google_kms_crypto_key.bucket.id
  }
}
```

---

## Azure Resources

### AKS Cluster

```hcl
resource "azurerm_kubernetes_cluster" "main" {
  name                = "production-cluster"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "production"
  kubernetes_version  = "1.28"

  default_node_pool {
    name                = "default"
    node_count          = 3
    vm_size             = "Standard_D2s_v3"
    enable_auto_scaling = true
    min_count           = 2
    max_count           = 10
    vnet_subnet_id      = azurerm_subnet.aks.id
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    network_policy    = "calico"
    load_balancer_sku = "standard"
  }

  azure_policy_enabled = true

  oms_agent {
    log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
  }

  maintenance_window {
    allowed {
      day   = "Sunday"
      hours = [3, 4]
    }
  }

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
  }
}

resource "azurerm_kubernetes_cluster_node_pool" "spot" {
  name                  = "spot"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.main.id
  vm_size               = "Standard_D2s_v3"
  enable_auto_scaling   = true
  min_count             = 0
  max_count             = 5
  priority              = "Spot"
  eviction_policy       = "Delete"
  spot_max_price        = -1

  node_labels = {
    "kubernetes.azure.com/scalesetpriority" = "spot"
  }

  node_taints = [
    "kubernetes.azure.com/scalesetpriority=spot:NoSchedule"
  ]
}
```

### Azure Database for PostgreSQL

```hcl
resource "azurerm_postgresql_flexible_server" "main" {
  name                   = "production-db"
  resource_group_name    = azurerm_resource_group.main.name
  location               = azurerm_resource_group.main.location
  version                = "15"
  administrator_login    = "adminuser"
  administrator_password = random_password.db_password.result

  storage_mb   = 32768
  sku_name     = "GP_Standard_D2s_v3"
  zone         = "1"

  backup_retention_days        = 7
  geo_redundant_backup_enabled = true

  high_availability {
    mode                      = "ZoneRedundant"
    standby_availability_zone = "2"
  }

  maintenance_window {
    day_of_week  = 0
    start_hour   = 3
    start_minute = 0
  }

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
  }
}

resource "azurerm_postgresql_flexible_server_database" "main" {
  name      = "myapp"
  server_id = azurerm_postgresql_flexible_server.main.id
  collation = "en_US.utf8"
  charset   = "utf8"
}
```

### Azure Storage Account

```hcl
resource "azurerm_storage_account" "main" {
  name                     = "myappproddata"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
  account_kind             = "StorageV2"

  enable_https_traffic_only       = true
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false

  blob_properties {
    versioning_enabled = true

    delete_retention_policy {
      days = 7
    }

    container_delete_retention_policy {
      days = 7
    }
  }

  network_rules {
    default_action             = "Deny"
    ip_rules                   = ["203.0.113.0/24"]
    virtual_network_subnet_ids = [azurerm_subnet.main.id]
  }

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
  }
}

resource "azurerm_storage_container" "app_data" {
  name                  = "app-data"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}
```

---

## Variables and Outputs

### Complex Variable Types

```hcl
# variables.tf

# Simple variables
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "instance_count" {
  description = "Number of instances"
  type        = number
  default     = 3

  validation {
    condition     = var.instance_count >= 1 && var.instance_count <= 10
    error_message = "Instance count must be between 1 and 10."
  }
}

# List variable
variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

# Map variable
variable "instance_types" {
  description = "Instance types by environment"
  type        = map(string)
  default = {
    dev        = "t3.micro"
    staging    = "t3.small"
    production = "t3.large"
  }
}

# Object variable
variable "database_config" {
  description = "Database configuration"
  type = object({
    engine         = string
    engine_version = string
    instance_class = string
    allocated_storage = number
    multi_az       = bool
  })
  default = {
    engine            = "postgres"
    engine_version    = "15.3"
    instance_class    = "db.t3.large"
    allocated_storage = 100
    multi_az          = true
  }
}

# List of objects
variable "node_groups" {
  description = "EKS node group configurations"
  type = list(object({
    name           = string
    instance_types = list(string)
    desired_size   = number
    min_size       = number
    max_size       = number
    capacity_type  = string
  }))
  default = [
    {
      name           = "general"
      instance_types = ["t3.large"]
      desired_size   = 3
      min_size       = 2
      max_size       = 10
      capacity_type  = "ON_DEMAND"
    },
    {
      name           = "spot"
      instance_types = ["t3.large", "t3a.large"]
      desired_size   = 2
      min_size       = 0
      max_size       = 5
      capacity_type  = "SPOT"
    }
  ]
}
```

### Conditional Outputs

```hcl
# outputs.tf

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "eks_cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = module.eks.cluster_endpoint
  sensitive   = true
}

output "database_endpoint" {
  description = "Database endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}

# Conditional output
output "nat_gateway_ips" {
  description = "NAT Gateway public IPs"
  value       = var.enable_nat_gateway ? aws_eip.nat[*].public_ip : []
}

# Complex output
output "cluster_info" {
  description = "Cluster information"
  value = {
    cluster_name     = module.eks.cluster_name
    cluster_endpoint = module.eks.cluster_endpoint
    cluster_version  = module.eks.cluster_version
    oidc_provider    = module.eks.oidc_provider
    security_group_id = module.eks.cluster_security_group_id
  }
  sensitive = true
}
```

---

## Cost Optimization

### Right-Sizing Instances

```hcl
locals {
  # Environment-specific instance types
  instance_types = {
    dev = {
      app = "t3.micro"
      db  = "db.t3.micro"
    }
    staging = {
      app = "t3.small"
      db  = "db.t3.small"
    }
    production = {
      app = "t3.large"
      db  = "db.t3.large"
    }
  }
  
  selected_instance_types = local.instance_types[var.environment]
}

resource "aws_instance" "app" {
  instance_type = local.selected_instance_types.app
  # ...
}
```

### Spot Instances

```hcl
# EKS with Spot instances
eks_managed_node_groups = {
  spot = {
    desired_size = 2
    min_size     = 0
    max_size     = 10

    instance_types = ["t3.large", "t3a.large", "t2.large"]
    capacity_type  = "SPOT"

    # Spot instances can save up to 90% vs on-demand
  }
}
```

### Auto-Scaling Schedules

```hcl
# Scale down non-production environments at night
resource "aws_autoscaling_schedule" "scale_down" {
  count                  = var.environment != "production" ? 1 : 0
  scheduled_action_name  = "scale-down-night"
  min_size               = 0
  max_size               = 0
  desired_capacity       = 0
  recurrence             = "0 22 * * *"  # 10 PM daily
  autoscaling_group_name = aws_autoscaling_group.main.name
}

resource "aws_autoscaling_schedule" "scale_up" {
  count                  = var.environment != "production" ? 1 : 0
  scheduled_action_name  = "scale-up-morning"
  min_size               = 2
  max_size               = 10
  desired_capacity       = 3
  recurrence             = "0 8 * * *"  # 8 AM daily
  autoscaling_group_name = aws_autoscaling_group.main.name
}
```

### Storage Lifecycle

```hcl
# S3 lifecycle rules
resource "aws_s3_bucket_lifecycle_configuration" "app_data" {
  bucket = aws_s3_bucket.app_data.id

  rule {
    id     = "cost-optimization"
    status = "Enabled"

    # Move to Infrequent Access after 30 days (50% cost savings)
    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    # Move to Glacier after 90 days (90% cost savings)
    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    # Delete after 365 days
    expiration {
      days = 365
    }
  }
}
```

### Resource Tagging for Cost Tracking

```hcl
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
    CostCenter  = var.cost_center
    Owner       = var.owner_email
  }
}

resource "aws_instance" "app" {
  # ...
  tags = merge(
    local.common_tags,
    {
      Name = "${var.project_name}-app-${count.index + 1}"
      Role = "application"
    }
  )
}
```

---

## Security Best Practices

### Encrypted Storage

```hcl
# KMS key for encryption
resource "aws_kms_key" "main" {
  description             = "KMS key for ${var.environment}"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  tags = local.common_tags
}

resource "aws_kms_alias" "main" {
  name          = "alias/${var.project_name}-${var.environment}"
  target_key_id = aws_kms_key.main.key_id
}

# Encrypted EBS volumes
resource "aws_ebs_volume" "data" {
  availability_zone = var.availability_zone
  size              = 100
  encrypted         = true
  kms_key_id        = aws_kms_key.main.arn
}

# Encrypted RDS
resource "aws_db_instance" "main" {
  storage_encrypted = true
  kms_key_id        = aws_kms_key.main.arn
  # ...
}
```

### Network Isolation

```hcl
# Private subnets only
resource "aws_instance" "app" {
  subnet_id              = module.vpc.private_subnet_ids[0]
  associate_public_ip_address = false
  # ...
}

# Restrictive security groups
resource "aws_security_group" "app" {
  name        = "${var.project_name}-app-sg"
  description = "Security group for app servers"
  vpc_id      = module.vpc.vpc_id

  # Only allow traffic from load balancer
  ingress {
    description     = "HTTP from ALB"
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  # Allow all outbound
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### Secrets Management

```hcl
# Store secrets in AWS Secrets Manager
resource "random_password" "db_password" {
  length  = 32
  special = true
}

resource "aws_secretsmanager_secret" "db_password" {
  name                    = "${var.environment}/db/password"
  recovery_window_in_days = 30
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = random_password.db_password.result
}

# Reference secret in application
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = aws_secretsmanager_secret.db_password.id
}

resource "aws_db_instance" "main" {
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
  # ...
}
```

---

## Troubleshooting

### State Lock Issues

```bash
# View state lock
terraform force-unlock <lock-id>

# Remove state lock manually (DynamoDB)
aws dynamodb delete-item \
  --table-name terraform-state-locks \
  --key '{"LockID":{"S":"<state-file-path>"}}'
```

### Import Existing Resources

```bash
# Import VPC
terraform import aws_vpc.main vpc-1234567890abcdef0

# Import EC2 instance
terraform import aws_instance.app i-1234567890abcdef0

# Import security group
terraform import aws_security_group.app sg-1234567890abcdef0
```

### State Management

```bash
# List resources in state
terraform state list

# Show resource details
terraform state show aws_instance.app

# Move resource in state
terraform state mv aws_instance.old aws_instance.new

# Remove resource from state
terraform state rm aws_instance.app

# Pull remote state
terraform state pull > terraform.tfstate.backup
```

### Debugging

```bash
# Enable debug logging
export TF_LOG=DEBUG
terraform plan

# Specific provider logging
export TF_LOG_PROVIDER=DEBUG
terraform apply

# Save logs to file
export TF_LOG_PATH=./terraform.log
```

---

**Best Practices Summary:**
- Use modules for reusability
- Remote state with locking
- Encryption at rest
- Resource tagging for cost tracking
- Environment-specific configurations
- Secrets in dedicated stores
- Version constraints in modules
- Validate before apply

**Next Steps:**
- Read monitoring.md for observability
- Read kubernetes.md for K8s integration
- Read cicd.md for automated deployments
