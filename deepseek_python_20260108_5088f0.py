#!/usr/bin/env python3
"""
CCEG Dataset Generator
Synthetic, deterministic compliance execution scenarios
Total: 10,000 records across 3 layers
"""

import json
import hashlib
import random
from datetime import datetime
from typing import Dict, List, Any
import numpy as np

# Deterministic seed for reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

class CCEGGenerator:
    """Generate synthetic compliance execution scenarios"""
    
    # Constants
    CONTROL_FAMILIES = ["AC", "AU", "CM", "IA", "SC", "SI", "RA", "PL"]
    
    OBJECTIVES = {
        "AC": ["access_restriction", "least_privilege", "separation_duties"],
        "AU": ["audit_logging", "log_integrity", "log_retention"],
        "CM": ["config_management", "change_control", "baseline_config"],
        "IA": ["identification", "authentication", "authorization"],
        "SC": ["system_protection", "boundary_defense", "encryption"],
        "SI": ["system_integrity", "malware_protection", "vulnerability_scan"],
        "RA": ["risk_assessment", "vulnerability_assessment", "threat_modeling"],
        "PL": ["planning", "policy_development", "security_training"]
    }
    
    ASSET_CLASSES = ["identity", "compute", "storage", "network", "data", "management"]
    
    RISK_DOMAINS = [
        "privilege_escalation", "data_exfiltration", "config_drift",
        "insufficient_monitoring", "lateral_movement", "data_loss",
        "credential_exposure", "service_disruption"
    ]
    
    # AWS Contexts
    AWS_SERVICES = {
        "iam": ["aws_iam_user", "aws_iam_role", "aws_iam_policy", "aws_iam_group"],
        "ec2": ["aws_instance", "aws_security_group", "aws_launch_template"],
        "s3": ["aws_s3_bucket", "aws_s3_bucket_policy"],
        "vpc": ["aws_vpc", "aws_subnet", "aws_network_acl", "aws_security_group"],
        "rds": ["aws_db_instance", "aws_db_security_group"],
        "lambda": ["aws_lambda_function", "aws_lambda_permission"],
        "cloudtrail": ["aws_cloudtrail"]
    }
    
    PATTERN_CLASSES = [
        "identity_trust", "network_exposure", "data_encryption",
        "logging_gap", "key_rotation", "backup_config",
        "permission_boundary", "resource_policy"
    ]
    
    FAILURE_MODES = {
        "identity_trust": [
            "overly_permissive_trust_policy",
            "external_principal_allowed",
            "service_principal_wildcard"
        ],
        "network_exposure": [
            "publicly_accessible_resource",
            "overly_permissive_security_group",
            "no_flow_logs"
        ],
        "data_encryption": [
            "encryption_disabled",
            "unencrypted_data_transit",
            "customer_key_not_used"
        ]
    }
    
    def __init__(self):
        self.record_counter = 0
        self.pattern_registry = {}
        
    def _generate_id(self, data: Dict) -> str:
        """Generate deterministic ID from data"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]
    
    def _select_with_weights(self, items: List, weights: List[float]) -> Any:
        """Weighted random selection"""
        return random.choices(items, weights=weights, k=1)[0]
    
    def generate_intent_layer(self, count: int = 2000) -> List[Dict]:
        """Generate abstract intent vectors (vendor-neutral)"""
        records = []
        
        for _ in range(count):
            control_family = random.choice(self.CONTROL_FAMILIES)
            
            record = {
                "record_id": f"INT_{self.record_counter:06d}",
                "control_family": control_family,
                "control_intent_vector": {
                    "objective": random.choice(self.OBJECTIVES[control_family]),
                    "asset_class": random.choice(self.ASSET_CLASSES),
                    "risk_domain": random.choice(self.RISK_DOMAINS)
                },
                "abstraction_level": "vendor_neutral",
                "standard_mappings": {
                    "nist_800_53": f"{control_family}-{random.randint(1, 20)}",
                    "cis": f"v{random.randint(1, 8)}.{random.randint(1, 15)}",
                    "iso_27001": f"A.{random.randint(5, 18)}.{random.randint(1, 4)}"
                },
                "generated_at": datetime.utcnow().isoformat() + "Z"
            }
            
            records.append(record)
            self.record_counter += 1
            
        return records
    
    def generate_execution_layer(self, count: int = 5000) -> List[Dict]:
        """Generate cloud-specific execution patterns"""
        records = []
        
        for _ in range(count):
            # Select service and resource
            service = random.choice(list(self.AWS_SERVICES.keys()))
            resource_type = random.choice(self.AWS_SERVICES[service])
            
            # Determine pattern
            pattern_class = random.choice(self.PATTERN_CLASSES)
            pattern_id = f"PAT_{pattern_class.upper()}_{random.randint(100, 999)}"
            
            # Generate failure mode based on pattern
            failure_modes = self.FAILURE_MODES.get(pattern_class, ["configuration_gap"])
            failure_mode = random.choice(failure_modes)
            
            # Compliance state (70% non-compliant for training)
            status = random.choices(
                ["compliant", "non_compliant", "partially_compliant"],
                weights=[0.15, 0.70, 0.15],
                k=1
            )[0]
            
            record = {
                "record_id": f"EXEC_{self.record_counter:06d}",
                "control_family": random.choice(self.CONTROL_FAMILIES),
                "control_intent_vector": {
                    "objective": random.choice(["access_restriction", "audit_logging", "config_management"]),
                    "asset_class": random.choice(self.ASSET_CLASSES),
                    "risk_domain": random.choice(self.RISK_DOMAINS)
                },
                "cloud_context": {
                    "provider": "aws",
                    "service": service,
                    "resource_type": resource_type,
                    "region": random.choice(["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"])
                },
                "infrastructure_pattern": {
                    "pattern_id": pattern_id,
                    "pattern_class": pattern_class,
                    "pattern_complexity": round(random.uniform(0.3, 0.95), 2)
                },
                "compliance_state": {
                    "status": status,
                    "confidence": round(random.uniform(0.85, 0.99), 2)
                },
                "violation_mechanics": {
                    "failure_mode": failure_mode,
                    "attack_surface": self._generate_attack_surface(pattern_class),
                    "blast_radius_score": round(random.uniform(0.4, 0.95), 2)
                },
                "evidence_model": {
                    "terraform_signal": self._generate_terraform_signal(resource_type),
                    "runtime_signal": self._generate_runtime_signal(service),
                    "static_detectable": random.choice([True, False])
                },
                "labeling": {
                    "severity": random.choices(
                        ["low", "medium", "high", "critical"],
                        weights=[0.2, 0.3, 0.3, 0.2],
                        k=1
                    )[0],
                    "ml_use_case": random.sample(
                        ["policy_classification", "risk_scoring", "auto_remediation", "anomaly_detection"],
                        k=random.randint(1, 3)
                    )
                },
                "generated_at": datetime.utcnow().isoformat() + "Z"
            }
            
            records.append(record)
            self.record_counter += 1
            
        return records
    
    def generate_remediation_layer(self, count: int = 3000) -> List[Dict]:
        """Generate remediation reasoning data"""
        records = []
        
        strategies = [
            "trust_policy_constraint", "encryption_enablement", "logging_enablement",
            "network_restriction", "key_rotation", "backup_configuration",
            "permission_reduction", "resource_isolation", "monitoring_enablement"
        ]
        
        for _ in range(count):
            strategy = random.choice(strategies)
            
            record = {
                "record_id": f"REMED_{self.record_counter:06d}",
                "problem_pattern": {
                    "pattern_id": f"PAT_{random.choice(self.PATTERN_CLASSES).upper()}_{random.randint(100, 999)}",
                    "failure_mode": random.choice(list(self.FAILURE_MODES.values())[0]),
                    "affected_resource": random.choice(list(self.AWS_SERVICES.values())[0])
                },
                "remediation_logic": {
                    "strategy": strategy,
                    "automation_feasible": random.choices([True, False], weights=[0.7, 0.3])[0],
                    "estimated_fix_effort": random.choices(["low", "medium", "high"], weights=[0.5, 0.3, 0.2])[0],
                    "implementation_steps": self._generate_implementation_steps(strategy),
                    "verification_checks": self._generate_verification_checks(strategy),
                    "rollback_complexity": round(random.uniform(0.1, 0.9), 2)
                },
                "cost_impact": {
                    "aws_cost_delta": round(random.uniform(-50, 150), 2),
                    "operational_overhead": round(random.uniform(0.1, 0.9), 2),
                    "risk_reduction_score": round(random.uniform(0.3, 0.95), 2)
                },
                "ai_training_signals": {
                    "can_autofix": random.choice([True, False]),
                    "requires_approval": random.choice([True, False]),
                    "context_complexity": round(random.uniform(0.2, 0.95), 2)
                },
                "generated_at": datetime.utcnow().isoformat() + "Z"
            }
            
            records.append(record)
            self.record_counter += 1
            
        return records
    
    def _generate_attack_surface(self, pattern_class: str) -> str:
        """Generate attack surface description"""
        mappings = {
            "identity_trust": "cross_account_assume_role",
            "network_exposure": "internet_facing_endpoint",
            "data_encryption": "unencrypted_data_access",
            "logging_gap": "unaudited_activity",
            "key_rotation": "stale_cryptographic_material"
        }
        return mappings.get(pattern_class, "configuration_exploit")
    
    def _generate_terraform_signal(self, resource_type: str) -> str:
        """Generate Terraform signal"""
        signals = {
            "aws_iam_role": "assume_role_policy",
            "aws_iam_policy": "policy_document",
            "aws_s3_bucket": "acl or public_access_block",
            "aws_security_group": "ingress/egress_rules",
            "aws_db_instance": "storage_encrypted",
            "aws_cloudtrail": "is_multi_region_trail"
        }
        return signals.get(resource_type, "resource_configuration")
    
    def _generate_runtime_signal(self, service: str) -> str:
        """Generate runtime signal"""
        signals = {
            "iam": "cloudtrail:AssumeRole",
            "s3": "s3:GetObject",
            "ec2": "ec2:RunInstances",
            "cloudtrail": "cloudtrail:CreateTrail",
            "lambda": "lambda:InvokeFunction"
        }
        return signals.get(service, f"{service}:API_Call")
    
    def _generate_implementation_steps(self, strategy: str) -> List[str]:
        """Generate remediation steps"""
        steps_map = {
            "trust_policy_constraint": [
                "Identify trust policy document",
                "Remove wildcard principals",
                "Add specific account constraints",
                "Apply updated policy"
            ],
            "encryption_enablement": [
                "Enable encryption at rest",
                "Configure KMS key",
                "Update resource policy",
                "Verify encryption status"
            ]
        }
        return steps_map.get(strategy, [
            "Analyze current configuration",
            "Apply security controls",
            "Validate remediation",
            "Update documentation"
        ])
    
    def _generate_verification_checks(self, strategy: str) -> List[str]:
        """Generate verification checks"""
        checks_map = {
            "trust_policy_constraint": [
                "Trust policy allows only required principals",
                "No wildcards in account IDs",
                "Conditions are properly scoped"
            ],
            "encryption_enablement": [
                "Encryption status shows enabled",
                "KMS key is customer managed",
                "No unencrypted data access logs"
            ]
        }
        return checks_map.get(strategy, [
            "Configuration matches security baseline",
            "No active violations detected",
            "Monitoring alerts are configured"
        ])
    
    def save_jsonl(self, records: List[Dict], filename: str):
        """Save records to JSONL file"""
        with open(filename, 'w') as f:
            for record in records:
                f.write(json.dumps(record) + '\n')
        
        print(f"Saved {len(records)} records to {filename}")

def main():
    """Generate all dataset layers"""
    generator = CCEGGenerator()
    
    print("Generating CCEG Dataset...")
    print("=" * 50)
    
    # Layer 1: Intent (2,000 records)
    print("Generating Intent Layer (2,000 records)...")
    intent_records = generator.generate_intent_layer(2000)
    generator.save_jsonl(intent_records, "dataset/jsonl/cceg_intent.jsonl")
    
    # Reset counter for clean IDs
    generator.record_counter = 0
    
    # Layer 2: Execution (5,000 records)
    print("\nGenerating Execution Layer (5,000 records)...")
    execution_records = generator.generate_execution_layer(5000)
    generator.save_jsonl(execution_records, "dataset/jsonl/cceg_execution.jsonl")
    
    # Reset counter for clean IDs
    generator.record_counter = 0
    
    # Layer 3: Remediation (3,000 records)
    print("\nGenerating Remediation Layer (3,000 records)...")
    remediation_records = generator.generate_remediation_layer(3000)
    generator.save_jsonl(remediation_records, "dataset/jsonl/cceg_remediation.jsonl")
    
    print("\n" + "=" * 50)
    print("Dataset Generation Complete!")
    print(f"Total Records: {2000 + 5000 + 3000}")
    print("Files saved in /dataset/jsonl/")

if __name__ == "__main__":
    main()