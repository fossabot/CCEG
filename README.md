# Cloud Compliance Execution Graph (CCEG) Dataset

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Records](https://img.shields.io/badge/records-10,000-green.svg)
![License](https://img.shields.io/badge/license-Commercial-red.svg)

## Overview

The **Cloud Compliance Execution Graph (CCEG)** is a synthetic, vendor-neutral dataset designed for training ML models on cloud compliance automation, policy classification, risk assessment, and automated remediation.

Unlike datasets that reproduce copyrighted control text, CCEG provides **abstracted execution scenarios** that capture the intent, mechanics, and remediation logic of compliance operations without violating intellectual property.

## 🎯 Key Features

- **10,000 synthetic records** across 3 specialized layers
- **Zero copyright concerns** - no reproduced control text
- **ML-optimized format** - JSONL for streaming and efficient processing
- **Multi-dimensional labeling** - severity, automation feasibility, ML use cases
- **Real infrastructure patterns** - AWS IAM, EC2, S3, RDS, Lambda, VPC, CloudTrail
- **Deterministic generation** - reproducible with seed value
- **Production-ready** - validated schema, comprehensive documentation

## 📊 Dataset Composition

| Layer | Records | Purpose | File |
|-------|---------|---------|------|
| **Intent** | 2,000 | Vendor-neutral compliance reasoning | `cceg_intent.jsonl` |
| **Execution** | 5,000 | Cloud-specific detection patterns | `cceg_execution.jsonl` |
| **Remediation** | 3,000 | Automated fix strategies | `cceg_remediation.jsonl` |

### Layer 1: Intent (Vendor-Neutral)

Abstract compliance objectives without cloud-specific details. Ideal for:
- LLM prompt engineering
- Intent classification
- Policy reasoning
- Cross-platform mapping

**Sample Record:**
```json
{
  "record_id": "INT_000001",
  "control_family": "AC",
  "control_intent_vector": {
    "objective": "access_restriction",
    "asset_class": "identity",
    "risk_domain": "privilege_escalation"
  },
  "abstraction_level": "vendor_neutral",
  "standard_mappings": {
    "nist_800_53": "AC-3",
    "cis": "v1.12",
    "iso_27001": "A.9.2"
  }
}
```

### Layer 2: Execution (Cloud-Specific)

AWS resource compliance states with violation mechanics. Ideal for:
- Policy validation engines
- Compliance posture assessment
- Drift detection
- Risk scoring models

**Sample Record:**
```json
{
  "record_id": "EXEC_000001",
  "control_family": "AC",
  "cloud_context": {
    "provider": "aws",
    "service": "iam",
    "resource_type": "aws_iam_role",
    "region": "us-east-1"
  },
  "infrastructure_pattern": {
    "pattern_id": "PAT_IDENTITY_TRUST_347",
    "pattern_class": "identity_trust",
    "pattern_complexity": 0.72
  },
  "compliance_state": {
    "status": "non_compliant",
    "confidence": 0.94
  },
  "violation_mechanics": {
    "failure_mode": "overly_permissive_trust_policy",
    "attack_surface": "cross_account_assume_role",
    "blast_radius_score": 0.81
  },
  "evidence_model": {
    "terraform_signal": "assume_role_policy",
    "runtime_signal": "cloudtrail:AssumeRole",
    "static_detectable": true
  },
  "labeling": {
    "severity": "high",
    "ml_use_case": ["policy_classification", "risk_scoring"]
  }
}
```

### Layer 3: Remediation (Fix Strategies)

Automated remediation logic with cost/effort estimates. Ideal for:
- Auto-remediation systems
- Fix strategy classification
- Cost-benefit analysis
- Approval workflow automation

**Sample Record:**
```json
{
  "record_id": "REMED_000001",
  "problem_pattern": {
    "pattern_id": "PAT_IDENTITY_TRUST_347",
    "failure_mode": "overly_permissive_trust_policy",
    "affected_resource": "aws_iam_role"
  },
  "remediation_logic": {
    "strategy": "trust_policy_constraint",
    "automation_feasible": true,
    "estimated_fix_effort": "low",
    "implementation_steps": [
      "Identify trust policy document",
      "Remove wildcard principals",
      "Add specific account constraints",
      "Apply updated policy"
    ],
    "verification_checks": [
      "Trust policy allows only required principals",
      "No wildcards in account IDs",
      "Conditions are properly scoped"
    ],
    "rollback_complexity": 0.23
  },
  "cost_impact": {
    "aws_cost_delta": 0.00,
    "operational_overhead": 0.15,
    "risk_reduction_score": 0.87
  },
  "ai_training_signals": {
    "can_autofix": true,
    "requires_approval": false,
    "context_complexity": 0.34
  }
}
```

## 🚀 Getting Started

### Installation

```bash
# Clone or download the dataset
git clone https://github.com/your-org/cceg-dataset.git
cd cceg-dataset

# Verify file structure
ls -R dataset/
```

### Quick Start (Python)

```python
import json

# Load intent layer
with open('dataset/jsonl/cceg_intent.jsonl', 'r') as f:
    intent_records = [json.loads(line) for line in f]

print(f"Loaded {len(intent_records)} intent records")

# Load execution layer
with open('dataset/jsonl/cceg_execution.jsonl', 'r') as f:
    execution_records = [json.loads(line) for line in f]

print(f"Loaded {len(execution_records)} execution records")

# Filter non-compliant resources
non_compliant = [
    r for r in execution_records 
    if r['compliance_state']['status'] == 'non_compliant'
]

print(f"Found {len(non_compliant)} non-compliant scenarios")
```

### Generate Dataset

```bash
# Run the generator script
python generator.py

# Output:
# Generating CCEG Dataset...
# ==================================================
# Generating Intent Layer (2,000 records)...
# Saved 2000 records to dataset/jsonl/cceg_intent.jsonl
# 
# Generating Execution Layer (5,000 records)...
# Saved 5000 records to dataset/jsonl/cceg_execution.jsonl
# 
# Generating Remediation Layer (3,000 records)...
# Saved 3000 records to dataset/jsonl/cceg_remediation.jsonl
# ==================================================
# Dataset Generation Complete!
# Total Records: 10000
```

## 📋 Schema Validation

The dataset includes a comprehensive JSON Schema for validation:

```bash
# Install jsonschema validator
pip install jsonschema

# Validate records
python validate_schema.py
```

See `schemas/cceg.schema.json` for the complete specification.

## 💡 Use Cases

### 1. Policy Classification
Train models to categorize compliance violations:
```python
# Features: control_intent_vector, infrastructure_pattern
# Labels: labeling.ml_use_case, labeling.severity
```

### 2. Risk Scoring
Predict blast radius and impact:
```python
# Features: violation_mechanics, infrastructure_pattern.pattern_complexity
# Labels: violation_mechanics.blast_radius_score, labeling.severity
```

### 3. Auto-Remediation
Generate Terraform fixes automatically:
```python
# Features: problem_pattern, cloud_context
# Labels: remediation_logic.strategy, remediation_logic.implementation_steps
```

### 4. Drift Detection
Identify configuration changes from baseline:
```python
# Features: evidence_model, infrastructure_pattern
# Labels: compliance_state.status
```

### 5. Compliance Posture Assessment
Continuous monitoring dashboards:
```python
# Aggregate compliance_state.status across resources
# Visualize by control_family, service, severity
```

## 🏗️ Infrastructure Coverage

### AWS Services (10+)
- **IAM** - Roles, policies, users, groups
- **EC2** - Instances, security groups, launch templates
- **S3** - Buckets, bucket policies, access controls
- **VPC** - VPCs, subnets, NACLs, security groups
- **RDS** - Database instances, security groups
- **Lambda** - Functions, permissions
- **CloudTrail** - Trail configuration
- **KMS** - Key management
- **CloudWatch** - Log groups
- **EKS** - Kubernetes clusters

### Infrastructure Patterns (10+)
- Identity trust relationships
- Network exposure risks
- Data encryption gaps
- Logging deficiencies
- Key rotation failures
- Backup configuration issues
- Permission boundaries
- Resource isolation problems

## 📈 Dataset Statistics

```
Total Records:           10,000
- Intent Layer:           2,000 (20%)
- Execution Layer:        5,000 (50%)
- Remediation Layer:      3,000 (30%)

Compliance Distribution:
- Compliant:              1,500 (15%)
- Non-Compliant:          7,000 (70%)
- Partially Compliant:    1,500 (15%)

Severity Distribution:
- Low:                    2,000 (20%)
- Medium:                 3,000 (30%)
- High:                   3,000 (30%)
- Critical:               2,000 (20%)

Automation Feasibility:
- Automatable:            7,000 (70%)
- Manual Required:        3,000 (30%)
```

## 🔒 Copyright & Licensing

This dataset is **fully synthetic** and contains:
- ✅ NO copyrighted NIST 800-53 control text
- ✅ NO copyrighted CIS Benchmark text
- ✅ NO copyrighted ISO 27001 text
- ✅ Abstracted intent vectors only
- ✅ Synthetic infrastructure patterns

**License:** Commercial dataset. Contact for licensing terms.

## 📚 Documentation

- **README.md** - This file (quick start guide)
- **DATASHEET.md** - Comprehensive dataset documentation
- **schemas/cceg.schema.json** - JSON Schema specification
- **generator.py** - Deterministic generation script

## 🤝 Citation

If you use this dataset in research or commercial products, please cite:

```bibtex
@dataset{cceg2025,
  title={Cloud Compliance Execution Graph (CCEG)},
  author={CCEG Team},
  year={2025},
  version={1.0.0},
  url={https://github.com/your-org/cceg-dataset}
}
```

## 📧 Contact & Support

- **Commercial Licensing:**ranasingheinfrastructure@gmail.com
- **Technical Support:**ranasingheinfrastructure@gmail.com
- **Issues:** GitHub Issues (for dataset bugs)

## 🗺️ Roadmap

### Version 1.1 (Q2 2025)
- Azure resource support
- GCP resource support
- Kubernetes security patterns

### Version 2.0 (Q3 2025)
- 50,000+ records
- Extended control families (IR, BC, DR)
- Multi-cloud scenarios
- Real-time drift detection patterns

## ⚖️ Legal Notice

This dataset is provided for compliance automation and ML training purposes. It does not constitute legal advice or guarantee compliance with any specific regulatory framework. Users are responsible for validating compliance requirements with qualified professionals.

---

**Version:** 1.0.0  
**Release Date:** January 2025  
**Format:** JSONL  
**Size:** ~50MB (compressed)
