# Cost Optimization - Cloud Infrastructure

## AWS Cost Optimization

### Compute Savings

**Reserved Instances (RIs):**
- 1-year: 30-40% savings
- 3-year: 50-60% savings
- Best for: Predictable workloads

**Savings Plans:**
- Flexible (any instance family, region)
- 1-year: ~40% savings
- 3-year: ~60% savings

**Spot Instances:**
- 70-90% discount vs On-Demand
- Best for: Fault-tolerant, stateless workloads
- Use with Auto Scaling Groups + mixed instances

**Example Strategy:**
```
Baseline capacity: 20 instances → Reserved (70%)
Variable capacity: 0-30 instances → Spot (90% cheaper)
Failover: On-Demand (instant availability)
```

### Database Cost Optimization

**RDS Reserved Instances:**
```
On-Demand db.m5.xlarge: $0.192/hour = $1,382/month
3-Year RI: $0.096/hour = $691/month (50% savings)
```

**Aurora Serverless:**
- Pay per ACU (Aurora Capacity Unit) per second
- Auto-scales based on load
- Best for: Intermittent workloads

**Read Replicas + Caching:**
```
Before: Single RDS instance (db.r5.8xlarge) = $4,800/month
After:
  - Primary: db.r5.4xlarge = $2,400/month
  - 2x Read Replicas: db.r5.2xlarge × 2 = $1,200/month
  - ElastiCache (cache.r6g.large) = $150/month
Total: $3,750/month (22% savings + better performance)
```

### Storage Optimization

**S3 Lifecycle Policies:**
```json
{
  "Rules": [
    {
      "Id": "MoveToIA",
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"  // 50% cheaper
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER"  // 80% cheaper
        },
        {
          "Days": 365,
          "StorageClass": "DEEP_ARCHIVE"  // 95% cheaper
        }
      ]
    }
  ]
}
```

**Cost Comparison:**
```
S3 Standard: $0.023/GB/month
S3 IA: $0.0125/GB/month (46% savings)
S3 Glacier: $0.004/GB/month (83% savings)
S3 Deep Archive: $0.00099/GB/month (96% savings)
```

### Data Transfer Costs

**Egress Costs:**
- Within same AZ: Free
- Cross-AZ: $0.01/GB
- To Internet: $0.09/GB (first 10 TB)

**Optimization:**
```
Before: Direct download from S3
  10 TB/month × $0.09/GB = $900/month

After: CloudFront CDN
  10 TB/month × $0.085/GB = $850/month
  + Cache hit ratio 80% → 2 TB from S3
  2 TB × $0.09/GB = $180/month
Total: $180/month (80% savings)
```

---

## GCP Cost Optimization

### Sustained Use Discounts (Automatic)
- 25% discount for running VMs >25% of month
- 50% discount for running VMs 100% of month
- Automatic (no commitment needed)

### Committed Use Discounts (CUDs)
- 1-year: 37% savings
- 3-year: 55% savings

### Preemptible VMs
- 80% discount vs regular VMs
- Max 24-hour runtime
- Best for: Batch jobs, fault-tolerant workloads

---

## Azure Cost Optimization

### Reserved Instances
- 1-year: 40% savings
- 3-year: 60% savings

### Spot VMs
- Up to 90% discount
- Eviction with 30-second warning

### Azure Hybrid Benefit
- Reuse existing Windows Server licenses
- Up to 49% savings on VMs

---

## Multi-Cloud Cost Comparison

| Service | AWS | GCP | Azure |
|---------|-----|-----|-------|
| Compute (2 vCPU, 8GB RAM) | $0.096/hr | $0.095/hr | $0.096/hr |
| Object Storage | $0.023/GB | $0.020/GB | $0.018/GB |
| Data Egress (first 10 TB) | $0.09/GB | $0.12/GB | $0.087/GB |
| Managed PostgreSQL | $0.272/hr | $0.257/hr | $0.288/hr |

---

## FinOps Best Practices

### Tagging Strategy
```
Cost Center: engineering, marketing, operations
Environment: production, staging, development
Owner: team-backend, team-frontend
Project: project-alpha, project-beta
```

### Cost Allocation Reports
```sql
-- AWS Cost Explorer Query
SELECT
  resource_id,
  SUM(cost) as total_cost
FROM cost_data
WHERE date >= '2024-01-01'
  AND tag_cost_center = 'engineering'
GROUP BY resource_id
ORDER BY total_cost DESC
LIMIT 20;
```

### Budget Alerts
```json
{
  "Budget": {
    "BudgetName": "Monthly-Prod-Budget",
    "BudgetLimit": {
      "Amount": "10000",
      "Unit": "USD"
    },
    "TimeUnit": "MONTHLY"
  },
  "NotificationsWithSubscribers": [
    {
      "Notification": {
        "NotificationType": "ACTUAL",
        "ComparisonOperator": "GREATER_THAN",
        "Threshold": 80
      },
      "Subscribers": [
        {
          "SubscriptionType": "EMAIL",
          "Address": "devops@example.com"
        }
      ]
    }
  ]
}
```

---

## Right-Sizing

### CPU Utilization Analysis
```
If avg CPU < 40% for 30 days → Downsize instance
If avg CPU > 80% for 7 days → Upsize instance
```

### Example Right-Sizing
```
Before: m5.2xlarge (8 vCPU, 32 GB) = $0.384/hr
CPU Usage: 15% average

After: m5.xlarge (4 vCPU, 16 GB) = $0.192/hr
Savings: $1,382/month per instance (50%)
```

---

## Serverless Cost Optimization

### AWS Lambda
```
Invocations: $0.20 per 1M requests
Duration: $0.0000166667 per GB-second

Example:
10M requests/month × 512 MB × 200ms avg
= 10M × 0.0000166667 × 0.1 GB-sec
= $16.67/month (vs $70/month for t3.micro)
```

**Optimization:**
- Reduce memory allocation (if CPU not bottleneck)
- Optimize cold start (use Provisioned Concurrency sparingly)
- Use Lambda Layers for shared dependencies

---

## Cost Monitoring Tools

**AWS:**
- Cost Explorer
- AWS Budgets
- Cost Anomaly Detection
- CloudWatch metrics (billing alarms)

**Third-Party:**
- CloudHealth
- Kubecost (Kubernetes)
- Infracost (IaC cost estimation)

---

## Cost Optimization Checklist

**Compute:**
- [ ] Right-size instances (match utilization)
- [ ] Use Reserved/Savings Plans (predictable workloads)
- [ ] Spot/Preemptible VMs (fault-tolerant workloads)
- [ ] Auto-scaling (scale down during off-hours)
- [ ] Terminate unused instances

**Storage:**
- [ ] S3 lifecycle policies (move to cheaper tiers)
- [ ] Delete unused EBS volumes
- [ ] Use S3 Intelligent-Tiering
- [ ] Compress data before storing

**Database:**
- [ ] Reserved Instances (production DBs)
- [ ] Aurora Serverless (intermittent workloads)
- [ ] Read replicas + caching (reduce DB load)
- [ ] Automated backups retention (7 days vs 30 days)

**Network:**
- [ ] CloudFront CDN (reduce egress costs)
- [ ] VPC endpoints (avoid NAT Gateway charges)
- [ ] Consolidate data transfers
- [ ] Use AWS PrivateLink

**Monitoring:**
- [ ] Set up cost allocation tags
- [ ] Create budget alerts (80%, 100%, 120%)
- [ ] Weekly cost review meetings
- [ ] Quarterly cost optimization audits

---

## ROI Calculation

**Example: Migrate to Spot Instances**
```
Current: 50 On-Demand m5.large = $3,650/month
Proposed: 35 Reserved + 15 Spot (avg)
  = (35 × $43.80) + (15 × $18.25)
  = $1,533 + $274 = $1,807/month

Annual Savings: ($3,650 - $1,807) × 12 = $22,116
Implementation Cost: $5,000 (engineering time)
Payback Period: 2.7 months
3-Year ROI: (($22,116 × 3) - $5,000) / $5,000 = 1,227%
```

---

## Key Takeaways

1. **Measure First** - Can't optimize what you don't measure
2. **Right-Size** - 40% of cloud spend is wasted on oversized resources
3. **Commit When Predictable** - 50-60% savings with RIs/Savings Plans
4. **Use Spot/Preemptible** - 70-90% savings for fault-tolerant workloads
5. **Storage Tiers** - Lifecycle policies save 80-95% on archival data
6. **Monitor Continuously** - Costs drift without ongoing attention
7. **Automate Cleanup** - Orphaned resources add up quickly
8. **Culture of Cost Awareness** - Engineers must see cost impact
