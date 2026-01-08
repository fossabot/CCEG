# Compliance Control Execution Graph (CCEG) Dataset

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/cceg-dataset)
[![Records](https://img.shields.io/badge/records-10,000-green.svg)](https://github.com/yourusername/cceg-dataset)

> **Synthetic, deterministic dataset for training AI/ML models in cloud compliance automation**

## 🎯 Overview

The CCEG dataset bridges the gap between abstract compliance controls and concrete cloud infrastructure configurations. It provides 10,000 synthetically generated, ML-ready records designed specifically for training models that automate cloud security and compliance workflows.

### Key Features

- ✅ **100% Synthetic**: No real customer data, safe for training and sharing
- 🔄 **Deterministic**: Reproducible with seed-based generation
- 📊 **ML-Ready**: JSONL format with normalized scoring and structured labels
- 🎓 **Multi-Layer**: Intent → Execution → Remediation reasoning chains
- ☁️ **Cloud-Native**: AWS-focused patterns (IAM, EC2, S3, VPC, RDS, Lambda, CloudTrail)
- 🔐 **Security-First**: Real-world violation scenarios and attack surface modeling

## 📦 Dataset Composition

| Layer | Records | Purpose | File |
|-------|---------|---------|------|
| **Intent** | 2,000 | Abstract control objectives (vendor-neutral) | `cceg_intent.jsonl` |
| **Execution** | 5,000 | Cloud-specific compliance patterns & violations | `cceg_execution.jsonl` |
| **Remediation** | 3,000 | Fix strategies with cost/effort analysis | `cceg_remediation.jsonl` |
| **Total** | **10,000** | Complete compliance reasoning chain | — |

### Dataset Structure

```
dataset/
│
├── jsonl/
│   ├── cceg_intent.jsonl          # Abstract control vectors
│   ├── cceg_execution.jsonl       # AWS resource compliance states
│   └── cceg_remediation.jsonl     # Remediation logic & strategies
│
├── schemas/
│   └── cceg.schema.json           # JSON Schema specification
│
├── README.md                       # This file
├── DATASHEET.md                    # Dataset documentation
└── generator.py                    # Generation script
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- `numpy` package

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/cceg-dataset.git
cd cceg-dataset

# Install dependencies
pip install numpy

# Generate the dataset
python generator.py
```

### Verify Generation

```bash
# Check record counts
wc -l dataset/jsonl/*.jsonl

# Expected output:
#   2000 dataset/jsonl/cceg_intent.jsonl
#   5000 dataset/jsonl/cceg_execution.jsonl
#   3000 dataset/jsonl/cceg_remediation.jsonl
```

### Load Data (Python)

```python
import json

# Load execution layer
with open('dataset/jsonl/cceg_execution.jsonl', 'r') as f:
    execution_data = [json.loads(line) for line in f]

# Example: Filter high-severity IAM violations
iam_violations = [
    record for record in execution_data
    if record['cloud_context']['service'] == 'iam'
    and record['labeling']['severity'] == 'high'
    and record['compliance_state']['status'] == 'non_compliant'
]

print(f"Found {len(iam_violations)} high-severity IAM violations")
```

## 📋 Dataset Layers Explained

### Layer 1: Intent (Abstract Control Reasoning)

**Purpose**: Vendor-neutral control objectives mapped to compliance frameworks

**Sample Record**:
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
    "cis": "v1.4",
    "iso_27001": "A.9.2.1"
  },
  "generated_at": "2024-01-15T10:30:00Z"
}
```

**Use Cases**:
- Cross-framework control mapping
- Policy abstraction training
- Compliance standard translation

---

### Layer 2: Execution (Cloud-Specific Patterns)

**Purpose**: AWS resource configurations with compliance states and violation mechanics

**Sample Record**:
```json
{
  "record_id": "EXEC_000001",
  "control_family": "AC",
  "control_intent_vector": {
    "objective": "access_restriction",
    "asset_class": "identity",
    "risk_domain": "privilege_escalation"
  },
  "cloud_context": {
    "provider": "aws",
    "service": "iam",
    "resource_type": "aws_iam_role",
    "region": "us-east-1"
  },
  "infrastructure_pattern": {
    "pattern_id": "PAT_IDENTITY_TRUST_123",
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
    "ml_use_case": ["policy_classification", "risk_scoring", "auto_remediation"]
  },
  "generated_at": "2024-01-15T10:30:01Z"
}
```

**Use Cases**:
- Policy violation classification
- Risk scoring models
- Attack surface analysis
- Infrastructure-as-Code (IaC) scanning

**Key Features**:
- **70% non-compliant** records for balanced training
- **Confidence scores** (0.85-0.99) for uncertainty modeling
- **Blast radius** quantification (0-1 scale)
- **Evidence signals** for both static and runtime detection

---

### Layer 3: Remediation (Fix Strategy Classification)

**Purpose**: Actionable remediation logic with cost/effort analysis

**Sample Record**:
```json
{
  "record_id": "REMED_000001",
  "problem_pattern": {
    "pattern_id": "PAT_IDENTITY_TRUST_123",
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
    "rollback_complexity": 0.2
  },
  "cost_impact": {
    "aws_cost_delta": 0.0,
    "operational_overhead": 0.1,
    "risk_reduction_score": 0.85
  },
  "ai_training_signals": {
    "can_autofix": true,
    "requires_approval": false,
    "context_complexity": 0.3
  },
  "generated_at": "2024-01-15T10:30:02Z"
}
```

**Use Cases**:
- Auto-remediation decision engines
- Cost-benefit analysis for fixes
- Approval workflow classification
- Rollback risk assessment

**Key Features**:
- **70% automation-feasible** for realistic training
- **Cost impact modeling** (AWS spend delta + operational overhead)
- **Rollback complexity** scoring (0-1 scale)
- **Step-by-step implementation** guidance

## 🎯 Machine Learning Use Cases

### 1. Policy Violation Classification

**Task**: Binary/multi-class classification of compliance states

```python
# Example training setup
features = [
    'pattern_complexity',
    'blast_radius_score',
    'control_family_encoded',
    'service_encoded'
]
target = 'compliance_state.status'  # compliant/non_compliant/partially_compliant
```

**Relevant Fields**:
- `compliance_state.status`
- `compliance_state.confidence`
- `infrastructure_pattern.pattern_complexity`
- `violation_mechanics.blast_radius_score`

---

### 2. Risk Scoring & Prioritization

**Task**: Regression model for risk quantification

```python
# Example risk score calculation
risk_features = [
    'blast_radius_score',
    'severity_encoded',
    'attack_surface_encoded',
    'pattern_complexity'
]
target = 'risk_score'  # Composite metric
```

**Relevant Fields**:
- `violation_mechanics.blast_radius_score`
- `labeling.severity`
- `violation_mechanics.attack_surface`

---

### 3. Auto-Remediation Decision Engine

**Task**: Binary classification for automation feasibility

```python
# Example auto-fix decision model
features = [
    'estimated_fix_effort_encoded',
    'rollback_complexity',
    'context_complexity',
    'operational_overhead'
]
target = 'can_autofix'  # True/False
```

**Relevant Fields**:
- `remediation_logic.automation_feasible`
- `ai_training_signals.can_autofix`
- `ai_training_signals.requires_approval`
- `remediation_logic.rollback_complexity`

---

### 4. Cost-Benefit Optimization

**Task**: Multi-objective optimization for remediation prioritization

```python
# Example cost-benefit model
features = [
    'aws_cost_delta',
    'operational_overhead',
    'risk_reduction_score',
    'estimated_fix_effort'
]
# Optimize: Maximize risk_reduction / (cost_delta + overhead)
```

**Relevant Fields**:
- `cost_impact.aws_cost_delta`
- `cost_impact.operational_overhead`
- `cost_impact.risk_reduction_score`

---

### 5. Anomaly Detection

**Task**: Identify unusual compliance patterns

```python
# Example anomaly detection
features = [
    'pattern_complexity',
    'blast_radius_score',
    'confidence',
    'service_resource_combinations'
]
# Detect outliers in non-compliant configurations
```

## 🔧 Advanced Usage

### Filter by Severity

```python
import json

def load_by_severity(filename, severity_level):
    """Load records filtered by severity"""
    with open(filename, 'r') as f:
        return [
            json.loads(line) for line in f
            if json.loads(line).get('labeling', {}).get('severity') == severity_level
        ]

critical_violations = load_by_severity(
    'dataset/jsonl/cceg_execution.jsonl',
    'critical'
)
```

### Cross-Layer Analysis

```python
def link_execution_to_remediation(exec_record, remediation_data):
    """Match execution patterns to remediation strategies"""
    pattern_id = exec_record['infrastructure_pattern']['pattern_id']
    
    matches = [
        r for r in remediation_data
        if r['problem_pattern']['pattern_id'] == pattern_id
    ]
    return matches

# Example: Find remediation for a violation
execution = execution_data[0]
remediation_options = link_execution_to_remediation(
    execution,
    remediation_data
)
```

### Schema Validation

```python
import json
from jsonschema import validate

# Load schema
with open('dataset/schemas/cceg.schema.json', 'r') as f:
    schema = json.load(f)

# Validate a record
with open('dataset/jsonl/cceg_execution.jsonl', 'r') as f:
    record = json.loads(f.readline())
    validate(instance=record, schema=schema)
    print("✓ Record is valid")
```

## 📊 Dataset Statistics

### Coverage by Control Family

| Control Family | Records | Percentage |
|----------------|---------|------------|
| AC (Access Control) | ~1,250 | 12.5% |
| AU (Audit & Accountability) | ~1,250 | 12.5% |
| CM (Configuration Management) | ~1,250 | 12.5% |
| IA (Identification & Auth) | ~1,250 | 12.5% |
| SC (System Protection) | ~1,250 | 12.5% |
| SI (System Integrity) | ~1,250 | 12.5% |
| RA (Risk Assessment) | ~1,250 | 12.5% |
| PL (Planning) | ~1,250 | 12.5% |

### Compliance State Distribution

| State | Execution Layer | Percentage |
|-------|----------------|------------|
| Non-Compliant | ~3,500 | 70% |
| Compliant | ~750 | 15% |
| Partially Compliant | ~750 | 15% |

### Severity Distribution

| Severity | Execution Layer | Percentage |
|----------|----------------|------------|
| Critical | ~1,000 | 20% |
| High | ~1,500 | 30% |
| Medium | ~1,500 | 30% |
| Low | ~1,000 | 20% |

### AWS Service Coverage

- **IAM**: Identity & Access Management
- **EC2**: Compute instances & security groups
- **S3**: Object storage & bucket policies
- **VPC**: Network configuration & ACLs
- **RDS**: Database instances & encryption
- **Lambda**: Serverless functions & permissions
- **CloudTrail**: Audit logging & monitoring

## 🔐 Data Quality & Validation

### Schema Compliance
- ✅ 100% of records validated against JSON Schema
- ✅ All required fields present
- ✅ Normalized scores (0-1 range)
- ✅ Enum constraints enforced

### Reproducibility
```bash
# Generate with same seed produces identical output
python generator.py  # Run 1
sha256sum dataset/jsonl/*.jsonl > checksums_1.txt

python generator.py  # Run 2
sha256sum dataset/jsonl/*.jsonl > checksums_2.txt

diff checksums_1.txt checksums_2.txt  # No differences
```

### Data Integrity Checks
- No duplicate record IDs
- Consistent timestamp formatting (ISO 8601)
- Valid pattern ID references
- Logical consistency (e.g., high severity → high blast_radius_score)

## 📚 Citation

If you use this dataset in your research or product, please cite:

```bibtex
@dataset{cceg2024,
  title={Compliance Control Execution Graph (CCEG) Dataset},
  author={Your Name/Organization},
  year={2024},
  version={1.0.0},
  url={https://github.com/yourusername/cceg-dataset}
}
```

## 🤝 Use Cases & Applications

### Security Product Companies
- Train CSPM (Cloud Security Posture Management) engines
- Enhance compliance automation platforms
- Build policy-as-code validation tools

### Enterprise Security Teams
- Test compliance monitoring systems
- Simulate violation scenarios for training
- Benchmark detection accuracy

### Research & Education
- Academic research in AI for security
- Training materials for cloud security courses
- Benchmarking ML model performance

### Consulting Firms
- Develop custom compliance solutions
- Train client-specific models
- POC/demo scenarios for sales

## 🛠️ Customization & Extension

### Adding New Cloud Providers

```python
# In generator.py, add Azure/GCP services
AZURE_SERVICES = {
    "aad": ["azuread_user", "azuread_group"],
    "vm": ["azurerm_virtual_machine"],
    # ... add more
}

GCP_SERVICES = {
    "iam": ["google_project_iam_member"],
    "compute": ["google_compute_instance"],
    # ... add more
}
```

### Increasing Dataset Size

```python
# Modify generation counts
intent_records = generator.generate_intent_layer(20000)      # 2K → 20K
execution_records = generator.generate_execution_layer(50000) # 5K → 50K
remediation_records = generator.generate_remediation_layer(30000) # 3K → 30K
```

### Custom Pattern Classes

```python
# Add domain-specific patterns
CUSTOM_PATTERN_CLASSES = [
    "container_security",
    "serverless_config",
    "data_residency",
    "supply_chain_security"
]
```

## 📄 License

This dataset is released under the **MIT License**.

```
MIT License

Copyright (c) 2024 [Your Name/Organization]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

## 🐛 Known Limitations

1. **AWS-Only Coverage**: Currently limited to AWS services (no Azure/GCP)
2. **Synthetic Data**: Does not capture real-world edge cases and anomalies
3. **Static Patterns**: No temporal evolution or drift modeling
4. **English-Only**: All text fields are in English
5. **Simplified Cost Model**: AWS cost estimates are approximate
6. **No Multi-Region Logic**: Regional compliance variations not modeled

## 🗺️ Roadmap

### Version 1.1 (Q2 2024)
- [ ] Add Azure service coverage
- [ ] Increase dataset to 50K records
- [ ] Add temporal drift patterns
- [ ] Multi-cloud cross-references

### Version 2.0 (Q3 2024)
- [ ] Add GCP service coverage
- [ ] Real-world validation partnerships
- [ ] Interactive visualization dashboard
- [ ] API access for live generation

## 💬 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/cceg-dataset/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/cceg-dataset/discussions)
- **Email**: youremail@example.com
- **Documentation**: [Full Docs](https://cceg-dataset.readthedocs.io)

## 🙏 Acknowledgments

- AWS Well-Architected Framework for pattern inspiration
- NIST 800-53 controls for compliance mapping
- CIS Benchmarks for security baselines
- Open-source security community for feedback

## 📈 Dataset Metrics

```
Total Records:        10,000
Total Size:           ~50 MB (uncompressed)
Generation Time:      ~30 seconds
Schema Validation:    100% pass rate
Unique Patterns:      500+
Control Families:     8
AWS Services:         7
Compliance States:    3
Severity Levels:      4
```

---

**Built with ❤️ for the cloud security community**

*Last Updated: January 2024 | Version 1.0.0*
