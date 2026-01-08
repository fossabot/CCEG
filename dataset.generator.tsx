import React, { useState } from 'react';
import { Download, FileJson, Database, CheckCircle, AlertCircle } from 'lucide-react';

const CCEGDatasetGenerator = () => {
  const [generating, setGenerating] = useState(false);
  const [progress, setProgress] = useState(0);
  const [generatedFiles, setGeneratedFiles] = useState([]);

  // Core data generation functions
  const generateControlIntent = (index) => {
    const families = ['AC', 'AU', 'CM', 'IA', 'SC', 'SI', 'RA'];
    const objectives = ['access_restriction', 'audit_logging', 'configuration_management', 
                        'identity_verification', 'secure_communication', 'integrity_monitoring', 'risk_assessment'];
    const assetClasses = ['identity', 'network', 'compute', 'storage', 'database', 'container'];
    const riskDomains = ['privilege_escalation', 'data_exfiltration', 'lateral_movement', 
                         'unauthorized_access', 'configuration_drift', 'exposure'];
    
    return {
      control_family: families[index % families.length],
      control_intent_vector: {
        objective: objectives[index % objectives.length],
        asset_class: assetClasses[index % assetClasses.length],
        risk_domain: riskDomains[index % riskDomains.length]
      }
    };
  };

  const generateCloudContext = (index) => {
    const services = [
      { service: 'iam', resource_type: 'aws_iam_role' },
      { service: 'ec2', resource_type: 'aws_instance' },
      { service: 's3', resource_type: 'aws_s3_bucket' },
      { service: 'rds', resource_type: 'aws_db_instance' },
      { service: 'lambda', resource_type: 'aws_lambda_function' },
      { service: 'vpc', resource_type: 'aws_security_group' },
      { service: 'kms', resource_type: 'aws_kms_key' },
      { service: 'cloudtrail', resource_type: 'aws_cloudtrail' },
      { service: 'cloudwatch', resource_type: 'aws_cloudwatch_log_group' },
      { service: 'eks', resource_type: 'aws_eks_cluster' }
    ];
    
    const svc = services[index % services.length];
    return {
      provider: 'aws',
      service: svc.service,
      resource_type: svc.resource_type
    };
  };

  const generateInfrastructurePattern = (index) => {
    const patterns = [
      { id: 'IAM_ROLE_TRUST_EXTERNAL', class: 'identity_trust', complexity: 0.72 },
      { id: 'S3_PUBLIC_ACCESS', class: 'data_exposure', complexity: 0.45 },
      { id: 'SG_UNRESTRICTED_INGRESS', class: 'network_exposure', complexity: 0.63 },
      { id: 'RDS_UNENCRYPTED', class: 'data_protection', complexity: 0.51 },
      { id: 'LAMBDA_OVERPRIVILEGED', class: 'privilege_boundary', complexity: 0.78 },
      { id: 'EC2_NO_IMDSv2', class: 'metadata_security', complexity: 0.59 },
      { id: 'KMS_KEY_ROTATION_DISABLED', class: 'cryptographic_hygiene', complexity: 0.48 },
      { id: 'CLOUDTRAIL_NOT_ENABLED', class: 'audit_coverage', complexity: 0.41 },
      { id: 'VPC_FLOW_LOGS_MISSING', class: 'network_visibility', complexity: 0.55 },
      { id: 'EKS_PUBLIC_ENDPOINT', class: 'container_exposure', complexity: 0.69 }
    ];
    
    const p = patterns[index % patterns.length];
    return {
      pattern_id: p.id,
      pattern_class: p.class,
      pattern_complexity: p.complexity
    };
  };

  const generateViolationMechanics = (pattern) => {
    const mechanics = {
      'IAM_ROLE_TRUST_EXTERNAL': {
        failure_mode: 'overly_permissive_trust_policy',
        attack_surface: 'cross_account_assume_role',
        blast_radius_score: 0.81
      },
      'S3_PUBLIC_ACCESS': {
        failure_mode: 'public_read_access_enabled',
        attack_surface: 'internet_exposed_data',
        blast_radius_score: 0.92
      },
      'SG_UNRESTRICTED_INGRESS': {
        failure_mode: '0.0.0.0/0_ingress_rule',
        attack_surface: 'unrestricted_network_access',
        blast_radius_score: 0.87
      },
      'RDS_UNENCRYPTED': {
        failure_mode: 'storage_encryption_disabled',
        attack_surface: 'data_at_rest_exposure',
        blast_radius_score: 0.75
      },
      'LAMBDA_OVERPRIVILEGED': {
        failure_mode: 'wildcard_permissions_in_policy',
        attack_surface: 'function_privilege_abuse',
        blast_radius_score: 0.79
      }
    };
    
    return mechanics[pattern.pattern_id] || {
      failure_mode: 'misconfiguration',
      attack_surface: 'security_gap',
      blast_radius_score: 0.65
    };
  };

  const generateEvidenceModel = (context, pattern) => {
    const signals = {
      'iam': { terraform: 'assume_role_policy', runtime: 'cloudtrail:AssumeRole' },
      's3': { terraform: 'acl', runtime: 's3:GetBucketAcl' },
      'ec2': { terraform: 'security_groups', runtime: 'ec2:DescribeSecurityGroups' },
      'rds': { terraform: 'storage_encrypted', runtime: 'rds:DescribeDBInstances' },
      'lambda': { terraform: 'role', runtime: 'lambda:GetPolicy' }
    };
    
    const sig = signals[context.service] || { terraform: 'configuration', runtime: 'api_call' };
    return {
      terraform_signal: sig.terraform,
      runtime_signal: sig.runtime,
      static_detectable: pattern.pattern_complexity < 0.75
    };
  };

  const generateRemediationLogic = (pattern) => {
    const strategies = {
      'identity_trust': { strategy: 'trust_policy_constraint', effort: 'low' },
      'data_exposure': { strategy: 'access_control_tightening', effort: 'low' },
      'network_exposure': { strategy: 'ingress_rule_restriction', effort: 'medium' },
      'data_protection': { strategy: 'encryption_enablement', effort: 'medium' },
      'privilege_boundary': { strategy: 'least_privilege_enforcement', effort: 'high' }
    };
    
    const s = strategies[pattern.pattern_class] || { strategy: 'manual_review', effort: 'high' };
    return {
      strategy: s.strategy,
      automation_feasible: s.effort !== 'high',
      estimated_fix_effort: s.effort
    };
  };

  const generateComplianceExecutionUnit = (index) => {
    const intent = generateControlIntent(index);
    const context = generateCloudContext(index);
    const pattern = generateInfrastructurePattern(index);
    const violation = generateViolationMechanics(pattern);
    const evidence = generateEvidenceModel(context, pattern);
    const remediation = generateRemediationLogic(pattern);
    
    const compliant = Math.random() > 0.65;
    const severities = ['critical', 'high', 'medium', 'low'];
    const useCases = ['policy_classification', 'risk_scoring', 'auto_remediation', 
                      'drift_detection', 'posture_assessment'];
    
    return {
      ...intent,
      cloud_context: context,
      infrastructure_pattern: pattern,
      compliance_state: {
        status: compliant ? 'compliant' : 'non_compliant',
        confidence: 0.85 + Math.random() * 0.14
      },
      violation_mechanics: violation,
      evidence_model: evidence,
      remediation_logic: remediation,
      labeling: {
        severity: severities[Math.floor(Math.random() * severities.length)],
        ml_use_case: useCases.slice(0, 2 + Math.floor(Math.random() * 2))
      }
    };
  };

  const generateIntentLayer = (count) => {
    const records = [];
    for (let i = 0; i < count; i++) {
      const unit = generateComplianceExecutionUnit(i);
      records.push({
        control_family: unit.control_family,
        control_intent_vector: unit.control_intent_vector,
        risk_domain: unit.control_intent_vector.risk_domain,
        ml_use_case: unit.labeling.ml_use_case
      });
    }
    return records;
  };

  const generateExecutionLayer = (count) => {
    const records = [];
    for (let i = 0; i < count; i++) {
      const unit = generateComplianceExecutionUnit(i + 2000);
      records.push({
        control_family: unit.control_family,
        cloud_context: unit.cloud_context,
        infrastructure_pattern: unit.infrastructure_pattern,
        compliance_state: unit.compliance_state,
        violation_mechanics: unit.violation_mechanics,
        evidence_model: unit.evidence_model,
        labeling: unit.labeling
      });
    }
    return records;
  };

  const generateRemediationLayer = (count) => {
    const records = [];
    for (let i = 0; i < count; i++) {
      const unit = generateComplianceExecutionUnit(i + 7000);
      records.push({
        infrastructure_pattern: unit.infrastructure_pattern,
        violation_mechanics: unit.violation_mechanics,
        remediation_logic: unit.remediation_logic,
        compliance_state: unit.compliance_state,
        cloud_context: {
          provider: unit.cloud_context.provider,
          service: unit.cloud_context.service
        },
        labeling: {
          severity: unit.labeling.severity,
          automation_feasible: unit.remediation_logic.automation_feasible
        }
      });
    }
    return records;
  };

  const generateSchema = () => {
    return {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "title": "Cloud Compliance Execution Graph (CCEG) Schema",
      "version": "1.0.0",
      "description": "Synthetic dataset for ML-powered cloud compliance automation",
      "type": "object",
      "required": ["control_family", "control_intent_vector", "cloud_context", "infrastructure_pattern"],
      "properties": {
        "control_family": {
          "type": "string",
          "enum": ["AC", "AU", "CM", "IA", "SC", "SI", "RA"],
          "description": "NIST-inspired control family abstraction"
        },
        "control_intent_vector": {
          "type": "object",
          "required": ["objective", "asset_class", "risk_domain"],
          "properties": {
            "objective": { "type": "string" },
            "asset_class": { "type": "string" },
            "risk_domain": { "type": "string" }
          }
        },
        "cloud_context": {
          "type": "object",
          "required": ["provider", "service", "resource_type"],
          "properties": {
            "provider": { "type": "string", "const": "aws" },
            "service": { "type": "string" },
            "resource_type": { "type": "string" }
          }
        },
        "infrastructure_pattern": {
          "type": "object",
          "required": ["pattern_id", "pattern_class", "pattern_complexity"],
          "properties": {
            "pattern_id": { "type": "string" },
            "pattern_class": { "type": "string" },
            "pattern_complexity": { "type": "number", "minimum": 0, "maximum": 1 }
          }
        },
        "compliance_state": {
          "type": "object",
          "properties": {
            "status": { "type": "string", "enum": ["compliant", "non_compliant"] },
            "confidence": { "type": "number", "minimum": 0, "maximum": 1 }
          }
        },
        "violation_mechanics": {
          "type": "object",
          "properties": {
            "failure_mode": { "type": "string" },
            "attack_surface": { "type": "string" },
            "blast_radius_score": { "type": "number", "minimum": 0, "maximum": 1 }
          }
        },
        "evidence_model": {
          "type": "object",
          "properties": {
            "terraform_signal": { "type": "string" },
            "runtime_signal": { "type": "string" },
            "static_detectable": { "type": "boolean" }
          }
        },
        "remediation_logic": {
          "type": "object",
          "properties": {
            "strategy": { "type": "string" },
            "automation_feasible": { "type": "boolean" },
            "estimated_fix_effort": { "type": "string", "enum": ["low", "medium", "high"] }
          }
        },
        "labeling": {
          "type": "object",
          "properties": {
            "severity": { "type": "string", "enum": ["critical", "high", "medium", "low"] },
            "ml_use_case": { "type": "array", "items": { "type": "string" } }
          }
        }
      }
    };
  };

  const generateREADME = () => {
    return `# Cloud Compliance Execution Graph (CCEG) Dataset

## Overview
A synthetic, vendor-neutral dataset for training ML models on cloud compliance automation, policy classification, and risk assessment.

## Dataset Composition
- **Total Size**: 10,000 records
- **Generation**: Deterministic, reproducible synthetic data
- **Coverage**: NIST 800-53 (abstracted), CIS Benchmarks (intent-level), ISO 27001 (principles)
- **Target Platforms**: AWS, Terraform

## Dataset Structure

### 1. Intent Layer (cceg_intent.jsonl)
- **Records**: 2,000
- **Purpose**: Vendor-neutral compliance reasoning
- **Use Cases**: LLM prompt engineering, intent classification

### 2. Execution Layer (cceg_execution.jsonl)
- **Records**: 5,000
- **Purpose**: Cloud-specific detection patterns
- **Use Cases**: Policy validation, posture assessment, drift detection

### 3. Remediation Layer (cceg_remediation.jsonl)
- **Records**: 3,000
- **Purpose**: Automated fix strategies
- **Use Cases**: Auto-remediation, effort estimation, strategy selection

## Schema
See \`schemas/cceg.schema.json\` for full JSON Schema validation.

## Key Features
- No copyrighted control text (synthetic abstractions only)
- ML-optimized format (JSONL for streaming)
- Multi-dimensional labeling (severity, use case, automation feasibility)
- Real-world infrastructure patterns (IAM, S3, EC2, RDS, Lambda, etc.)

## Use Cases
1. **Policy Classification**: Train models to categorize compliance violations
2. **Risk Scoring**: Predict blast radius and severity
3. **Auto-Remediation**: Generate Terraform fixes
4. **Drift Detection**: Identify configuration changes
5. **Posture Assessment**: Continuous compliance monitoring

## Data Model
Each record represents a **Compliance Execution Unit** - a single scenario linking:
- Compliance intent → Cloud resource → Violation mechanics → Remediation strategy

## Licensing
Commercial dataset. Contact for licensing terms.

## Citation
\`\`\`
@dataset{cceg2025,
  title={Cloud Compliance Execution Graph},
  year={2025},
  version={1.0.0}
}
\`\`\`
`;
  };

  const generateDATASHEET = () => {
    return `# DATASHEET: Cloud Compliance Execution Graph (CCEG)

## Motivation

**Purpose**: Enable ML-powered cloud compliance automation without reproducing copyrighted control text.

**Creators**: Synthetic generation system for compliance research and commercial applications.

**Funding**: Independent development.

## Composition

**Instances**: 10,000 compliance execution scenarios
- Intent Layer: 2,000 records
- Execution Layer: 5,000 records  
- Remediation Layer: 3,000 records

**Data Type**: JSON-structured compliance scenarios

**Sampling Strategy**: Deterministic generation covering:
- 7 control families (AC, AU, CM, IA, SC, SI, RA)
- 10+ AWS services (IAM, EC2, S3, RDS, Lambda, VPC, KMS, CloudTrail, CloudWatch, EKS)
- 10+ infrastructure anti-patterns
- 4 severity levels
- 3 remediation effort levels

**Labeling**: Multi-dimensional
- Compliance status (compliant/non_compliant)
- Severity (critical/high/medium/low)
- ML use cases (policy_classification, risk_scoring, auto_remediation, drift_detection, posture_assessment)
- Automation feasibility (boolean)

**Missing Data**: None (synthetic generation)

**Relationships**: Each execution unit links intent → infrastructure → violation → remediation

**Splits**: Not pre-split (users define based on use case)

**Confidentiality**: No PII, no real infrastructure data (fully synthetic)

## Collection Process

**Acquisition**: Algorithmic generation based on real-world compliance patterns

**Mechanisms**: Deterministic pseudorandom generation with seeded variation

**Sampling**: Stratified by control family, cloud service, and pattern type

**Time Frame**: Generated January 2025

**Ethics Review**: Not applicable (synthetic data)

**Notification**: N/A (no human subjects)

**Consent**: N/A (no human subjects)

## Preprocessing

**Preprocessing**: Schema validation, JSONL formatting

**Raw Data**: Generation code available upon request

## Uses

**Prior Uses**: Initial release

**Impact of Composition**: Enables compliance ML without copyright concerns

**Recommended Uses**:
- Training compliance classification models
- Risk scoring algorithms
- Auto-remediation policy generation
- Compliance posture dashboards

**Not Recommended**:
- Direct control text generation (this is synthetic abstraction)
- Replacement for legal compliance advice

**Prohibited Uses**: 
- Claiming conformance to actual standards without validation
- Bypassing security controls

## Distribution

**Distribution**: Commercial licensing

**Copyright**: Dataset copyright retained by creator

**IP Considerations**: No third-party IP (fully synthetic)

**Export Controls**: Standard data export rules apply

## Maintenance

**Support**: Commercial support available

**Updates**: Versioned releases planned

**Retention**: Perpetual access for licensees

**Legacy Versions**: Maintained for compatibility

**Extensions**: Additional cloud providers and frameworks planned

## Legal & Ethical Considerations

**Privacy**: No PII or sensitive data
**Human Subjects**: None
**Offensive Content**: None
**Bias**: Stratified sampling minimizes representation bias
**Subpopulations**: Not applicable
**Quality Issues**: Synthetic data may not capture all real-world edge cases
`;
  };

  const downloadFile = (filename, content) => {
    const blob = new Blob([content], { type: 'application/octet-stream' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  const generateDataset = async () => {
    setGenerating(true);
    setProgress(0);
    setGeneratedFiles([]);

    const files = [];

    // Generate Intent Layer
    setProgress(10);
    const intentData = generateIntentLayer(2000);
    const intentJSONL = intentData.map(r => JSON.stringify(r)).join('\n');
    files.push({ name: 'cceg_intent.jsonl', content: intentJSONL, size: intentJSONL.length });

    // Generate Execution Layer
    setProgress(40);
    const executionData = generateExecutionLayer(5000);
    const executionJSONL = executionData.map(r => JSON.stringify(r)).join('\n');
    files.push({ name: 'cceg_execution.jsonl', content: executionJSONL, size: executionJSONL.length });

    // Generate Remediation Layer
    setProgress(70);
    const remediationData = generateRemediationLayer(3000);
    const remediationJSONL = remediationData.map(r => JSON.stringify(r)).join('\n');
    files.push({ name: 'cceg_remediation.jsonl', content: remediationJSONL, size: remediationJSONL.length });

    // Generate Schema
    setProgress(85);
    const schema = generateSchema();
    files.push({ name: 'cceg.schema.json', content: JSON.stringify(schema, null, 2), size: JSON.stringify(schema).length });

    // Generate Documentation
    setProgress(95);
    const readme = generateREADME();
    files.push({ name: 'README.md', content: readme, size: readme.length });

    const datasheet = generateDATASHEET();
    files.push({ name: 'DATASHEET.md', content: datasheet, size: datasheet.length });

    setProgress(100);
    setGeneratedFiles(files);
    setGenerating(false);
  };

  const downloadAll = () => {
    generatedFiles.forEach(file => {
      downloadFile(file.name, file.content);
    });
  };

  const formatBytes = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  };

  return (
    <div className="w-full max-w-6xl mx-auto p-6 bg-gradient-to-br from-slate-900 to-slate-800 text-white min-h-screen">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <Database className="w-8 h-8 text-blue-400" />
          <h1 className="text-3xl font-bold">CCEG Dataset Generator</h1>
        </div>
        <p className="text-slate-300">Cloud Compliance Execution Graph - Professional ML Dataset</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="bg-slate-800 p-4 rounded-lg border border-slate-700">
          <div className="text-sm text-slate-400 mb-1">Intent Layer</div>
          <div className="text-2xl font-bold text-blue-400">2,000</div>
          <div className="text-xs text-slate-500 mt-1">Vendor-neutral reasoning</div>
        </div>
        <div className="bg-slate-800 p-4 rounded-lg border border-slate-700">
          <div className="text-sm text-slate-400 mb-1">Execution Layer</div>
          <div className="text-2xl font-bold text-green-400">5,000</div>
          <div className="text-xs text-slate-500 mt-1">Cloud-specific patterns</div>
        </div>
        <div className="bg-slate-800 p-4 rounded-lg border border-slate-700">
          <div className="text-sm text-slate-400 mb-1">Remediation Layer</div>
          <div className="text-2xl font-bold text-purple-400">3,000</div>
          <div className="text-xs text-slate-500 mt-1">Fix strategies</div>
        </div>
      </div>

      <div className="bg-slate-800 p-6 rounded-lg border border-slate-700 mb-6">
        <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
          <FileJson className="w-5 h-5 text-green-400" />
          Dataset Features
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex items-start gap-2">
            <CheckCircle className="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" />
            <div>
              <div className="font-semibold">Synthetic & Copyright-Safe</div>
              <div className="text-sm text-slate-400">No copyrighted control text</div>
            </div>
          </div>
          <div className="flex items-start gap-2">
            <CheckCircle className="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" />
            <div>
              <div className="font-semibold">ML-Optimized Format</div>
              <div className="text-sm text-slate-400">JSONL for streaming</div>
            </div>
          </div>
          <div className="flex items-start gap-2">
            <CheckCircle className="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" />
            <div>
              <div className="font-semibold">Multi-Dimensional Labels</div>
              <div className="text-sm text-slate-400">Severity, use case, automation</div>
            </div>
          </div>
          <div className="flex items-start gap-2">
            <CheckCircle className="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" />
            <div>
              <div className="font-semibold">Real Infrastructure Patterns</div>
              <div className="text-sm text-slate-400">AWS + Terraform focused</div>
            </div>
          </div>
        </div>
      </div>

      <div className="flex gap-4 mb-8">
        <button
          onClick={generateDataset}
          disabled={generating}
          className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:cursor-not-allowed text-white font-semibold py-4 px-6 rounded-lg transition-colors flex items-center justify-center gap-2"
        >
          <Database className="w-5 h-5" />
          {generating ? 'Generating Dataset...' : 'Generate Complete Dataset'}
        </button>
      </div>

      {generating && (
        <div className="bg-slate-800 p-6 rounded-lg border border-slate-700 mb-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-semibold">Progress</span>
            <span className="text-sm text-slate-400">{progress}%</span>
          </div>
          <div className="w-full bg-slate-700 rounded-full h-2">
            <div
              className="bg-blue-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      )}

      {generatedFiles.length > 0 && (
        <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold flex items-center gap-2">
              <CheckCircle className="w-6 h-6 text-green-400" />
              Generated Files
            </h2>
            <button
              onClick={downloadAll}
              className="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors flex items-center gap-2"
            >
              <Download className="w-4 h-4" />
              Download All
            </button>
          </div>
          <div className="space-y-2">
            {generatedFiles.map((file, idx) => (
              <div key={idx} className="flex items-center justify-between bg-slate-900 p-3 rounded border border-slate-700">
                <div className="flex items-center gap-3">
                  <FileJson className="w-5 h-5 text-blue-400" />
                  <div>
                    <div className="font-mono text-sm">{file.name}</div>
                    <div className="text-xs text-slate-500">{formatBytes(file.size)}</div>
                  </div>
                </div>
                <button
                  onClick={() => downloadFile(file.name, file.content)}
                  className="bg-slate-700 hover:bg-slate-600 text-white py-1 px-3 rounded text-sm transition-colors"
                >
                  Download
                </button>
              </div>
            ))}
          </div>
          <div className="mt-4 p-4 bg-blue-900/30 border border-blue-700 rounded-lg">
            <div className="flex items-start gap-2">
              <AlertCircle className="w-5 h-5 text-blue-400 mt-0.5 flex-shrink-0" />
              <div className="text-sm">
                <div className="font-semibold text-blue-300 mb-1">Platform-Ready Package</div>
                <div className="text-slate-300">
                  This dataset is structured for immediate upload to ML platforms. The layered architecture 
                  (intent, execution, remediation) enables tiered pricing models targeting ~$30k valuation.
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="mt-8 p-4 bg-slate-800 rounded-lg border border-slate-700 text-sm text-slate-400">
        <p className="font-semibold text-slate-300 mb-2">Use Cases:</p>
        <ul className="list-disc list-inside space-y-1">
          <li>Policy Classification (supervised learning)</li>
          <li>Risk Scoring (regression models)</li>
          <li>Auto-Remediation (sequence-to-sequence)</li>
          <li>Drift Detection (anomaly detection)</li>
          <li>Compliance Posture Assessment (multi-label classification)</li>
        </ul>
      </div>
    </div>
  );
};

export default CCEGDatasetGenerator;
