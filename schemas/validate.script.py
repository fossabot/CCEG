#!/usr/bin/env python3
"""
CCEG Schema Validator
Validates all JSONL files against the schema specification
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

try:
    from jsonschema import validate, ValidationError, Draft7Validator
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False
    print("WARNING: jsonschema not installed. Install with: pip install jsonschema")


class CCEGValidator:
    """Validate CCEG dataset records"""
    
    def __init__(self, schema_path: str = "dataset/schemas/cceg.schema.json"):
        self.schema_path = Path(schema_path)
        self.schema = None
        self.validator = None
        
        if not self.schema_path.exists():
            raise FileNotFoundError(f"Schema not found: {schema_path}")
        
        with open(self.schema_path, 'r') as f:
            self.schema = json.load(f)
        
        if JSONSCHEMA_AVAILABLE:
            self.validator = Draft7Validator(self.schema)
    
    def validate_record(self, record: Dict, record_type: str) -> Tuple[bool, List[str]]:
        """
        Validate a single record
        
        Args:
            record: Record to validate
            record_type: 'intent', 'execution', or 'remediation'
        
        Returns:
            (is_valid, error_messages)
        """
        errors = []
        
        # Basic structure checks
        if not isinstance(record, dict):
            errors.append("Record is not a dictionary")
            return False, errors
        
        if "record_id" not in record:
            errors.append("Missing required field: record_id")
            return False, errors
        
        # Type-specific validation
        record_id_prefix = record.get("record_id", "")[:4]
        expected_prefixes = {
            "intent": "INT_",
            "execution": "EXEC",
            "remediation": "REME"
        }
        
        expected = expected_prefixes.get(record_type, "")
        if not record_id_prefix.startswith(expected):
            errors.append(
                f"Record ID '{record_id_prefix}' doesn't match expected prefix "
                f"'{expected}' for {record_type} layer"
            )
        
        # JSON Schema validation (if available)
        if JSONSCHEMA_AVAILABLE and self.validator:
            schema_errors = list(self.validator.iter_errors(record))
            if schema_errors:
                for error in schema_errors[:5]:  # Limit to first 5 errors
                    path = ".".join(str(p) for p in error.path) if error.path else "root"
                    errors.append(f"{path}: {error.message}")
        
        # Custom field validations
        errors.extend(self._validate_custom_rules(record, record_type))
        
        return len(errors) == 0, errors
    
    def _validate_custom_rules(self, record: Dict, record_type: str) -> List[str]:
        """Apply custom validation rules"""
        errors = []
        
        # Control family validation
        if "control_family" in record:
            valid_families = ["AC", "AU", "CM", "IA", "SC", "SI", "RA", "PL"]
            if record["control_family"] not in valid_families:
                errors.append(
                    f"Invalid control_family: {record['control_family']} "
                    f"(expected one of {valid_families})"
                )
        
        # Score range validation
        score_fields = [
            ("infrastructure_pattern", "pattern_complexity"),
            ("compliance_state", "confidence"),
            ("violation_mechanics", "blast_radius_score"),
            ("cost_impact", "operational_overhead"),
            ("cost_impact", "risk_reduction_score"),
            ("ai_training_signals", "context_complexity"),
            ("remediation_logic", "rollback_complexity")
        ]
        
        for parent, field in score_fields:
            if parent in record and field in record[parent]:
                value = record[parent][field]
                if not isinstance(value, (int, float)):
                    errors.append(f"{parent}.{field} must be a number")
                elif not (0 <= value <= 1):
                    errors.append(f"{parent}.{field} must be between 0 and 1, got {value}")
        
        # Enum validations
        if "compliance_state" in record:
            valid_statuses = ["compliant", "non_compliant", "partially_compliant"]
            status = record["compliance_state"].get("status")
            if status and status not in valid_statuses:
                errors.append(f"Invalid compliance status: {status}")
        
        if "labeling" in record:
            valid_severities = ["low", "medium", "high", "critical"]
            severity = record["labeling"].get("severity")
            if severity and severity not in valid_severities:
                errors.append(f"Invalid severity: {severity}")
        
        if "remediation_logic" in record:
            valid_efforts = ["low", "medium", "high"]
            effort = record["remediation_logic"].get("estimated_fix_effort")
            if effort and effort not in valid_efforts:
                errors.append(f"Invalid fix effort: {effort}")
        
        return errors
    
    def validate_file(self, filepath: str, record_type: str) -> Dict:
        """
        Validate all records in a JSONL file
        
        Args:
            filepath: Path to JSONL file
            record_type: 'intent', 'execution', or 'remediation'
        
        Returns:
            Validation report dictionary
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            return {
                "file": str(filepath),
                "exists": False,
                "error": "File not found"
            }
        
        report = {
            "file": str(filepath),
            "exists": True,
            "total_records": 0,
            "valid_records": 0,
            "invalid_records": 0,
            "errors": []
        }
        
        try:
            with open(filepath, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    if not line.strip():
                        continue
                    
                    report["total_records"] += 1
                    
                    try:
                        record = json.loads(line)
                        is_valid, errors = self.validate_record(record, record_type)
                        
                        if is_valid:
                            report["valid_records"] += 1
                        else:
                            report["invalid_records"] += 1
                            report["errors"].append({
                                "line": line_num,
                                "record_id": record.get("record_id", "unknown"),
                                "errors": errors
                            })
                    
                    except json.JSONDecodeError as e:
                        report["invalid_records"] += 1
                        report["errors"].append({
                            "line": line_num,
                            "record_id": "unknown",
                            "errors": [f"JSON parsing error: {e}"]
                        })
        
        except Exception as e:
            report["error"] = str(e)
        
        return report
    
    def print_report(self, report: Dict):
        """Print validation report"""
        print(f"\n{'='*70}")
        print(f"File: {report['file']}")
        print(f"{'='*70}")
        
        if not report.get("exists"):
            print(f"❌ ERROR: {report.get('error', 'Unknown error')}")
            return
        
        if "error" in report:
            print(f"❌ ERROR: {report['error']}")
            return
        
        total = report["total_records"]
        valid = report["valid_records"]
        invalid = report["invalid_records"]
        
        print(f"Total Records:   {total}")
        print(f"Valid Records:   {valid} ✅")
        print(f"Invalid Records: {invalid} {'❌' if invalid > 0 else '✅'}")
        
        if invalid > 0:
            print(f"\n{'─'*70}")
            print(f"Errors Found ({len(report['errors'])} records with issues):")
            print(f"{'─'*70}")
            
            for error_info in report["errors"][:10]:  # Show first 10 errors
                print(f"\nLine {error_info['line']}, Record: {error_info['record_id']}")
                for error in error_info["errors"]:
                    print(f"  • {error}")
            
            if len(report["errors"]) > 10:
                print(f"\n... and {len(report['errors']) - 10} more errors")
        
        else:
            print("\n✅ All records are valid!")


def main():
    """Validate all CCEG dataset files"""
    
    print("CCEG Dataset Validator")
    print("="*70)
    
    if not JSONSCHEMA_AVAILABLE:
        print("\n⚠️  jsonschema library not available")
        print("   Basic validation only (install jsonschema for full validation)")
        print("   Run: pip install jsonschema\n")
    
    validator = CCEGValidator()
    
    files = [
        ("dataset/jsonl/cceg_intent.jsonl", "intent"),
        ("dataset/jsonl/cceg_execution.jsonl", "execution"),
        ("dataset/jsonl/cceg_remediation.jsonl", "remediation")
    ]
    
    all_valid = True
    total_records = 0
    total_valid = 0
    
    for filepath, record_type in files:
        report = validator.validate_file(filepath, record_type)
        validator.print_report(report)
        
        if report.get("exists") and report.get("invalid_records", 0) > 0:
            all_valid = False
        
        total_records += report.get("total_records", 0)
        total_valid += report.get("valid_records", 0)
    
    # Summary
    print(f"\n{'='*70}")
    print("OVERALL SUMMARY")
    print(f"{'='*70}")
    print(f"Total Records Validated: {total_records}")
    print(f"Total Valid Records:     {total_valid}")
    print(f"Total Invalid Records:   {total_records - total_valid}")
    
    if all_valid:
        print("\n✅ VALIDATION PASSED - All dataset files are valid!")
        return 0
    else:
        print("\n❌ VALIDATION FAILED - Some records have errors")
        return 1


if __name__ == "__main__":
    sys.exit(main())
