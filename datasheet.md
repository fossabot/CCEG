# DATASHEET: Cloud Compliance Execution Graph (CCEG)

**Version:** 1.0.0  
**Release Date:** January 2025  
**Last Updated:** January 8, 2025

This datasheet follows the framework proposed by Gebru et al. (2018) for documenting machine learning datasets.

---

## Table of Contents

1. [Motivation](#motivation)
2. [Composition](#composition)
3. [Collection Process](#collection-process)
4. [Preprocessing/Cleaning/Labeling](#preprocessingcleaninglabeling)
5. [Uses](#uses)
6. [Distribution](#distribution)
7. [Maintenance](#maintenance)
8. [Legal & Ethical Considerations](#legal--ethical-considerations)

---

## Motivation

### For what purpose was the dataset created?

The CCEG dataset was created to enable machine learning research and commercial applications in cloud compliance automation **without reproducing copyrighted control text** from standards like NIST 800-53, CIS Benchmarks, or ISO 27001.

Existing compliance datasets either:
1. Reproduce copyrighted material (creating legal risk)
2. Lack execution-level details needed for automation
3. Focus on documentation rather than operational scenarios

CCEG addresses these gaps by providing **synthetic execution scenarios** that capture compliance intent, violation mechanics, and remediation logic in a vendor-neutral, ML-friendly format.

### Who created the dataset?

The dataset was created by a team specializing in cloud security automation and synthetic data generation. The generation methodology was developed through consultation with:
- Cloud security architects
- Compliance automation engineers
- ML researchers in security domains
- Legal experts in intellectual property

### Who funded the creation of the dataset?

This is an independent commercial dataset project. No external funding was received.

### Any other comments?

The dataset generation code (`generator.py`) is available to licensees for:
- Verification of synthetic generation process
- Reproducibility of results
- Extension to additional cloud platforms or patterns

---

## Composition

### What do the instances that comprise the dataset represent?

Each instance represents a **Compliance Execution Unit** - a complete scenario linking:
1. **Compliance intent** (what we're trying to achieve)
2. **Cloud infrastructure** (where it's implemented)
3. **Violation mechanics** (how it fails)
4. **Remediation strategy** (how to fix it)

This is fundamentally different from traditional compliance datasets that represent control text or requirement statements.

### How many instances are there in total?

**Total: 10,000 instances** across three specialized layers:

| Layer | Count | Purpose |
|-------|-------|---------|
| Intent | 2,000 | Abstract, vendor-neutral compliance reasoning |
| Execution | 5,000 | Cloud-specific detection and validation patterns |
| Remediation | 3,000 | Automated fix strategies with cost/effort analysis |

### Does the dataset contain all possible instances?

No. The dataset is a **representative sample** of common compliance execution scenarios in AWS environments. It covers:
- 8 major control families (AC, AU, CM, IA, SC, SI, RA, PL)
- 10+ AWS services (IAM, EC2, S3, RDS, Lambda, VPC, KMS, CloudTrail, etc.)
- 10+ infrastructure anti-patterns
- Multiple severity levels and remediation strategies

Real-world environments contain far more edge cases and combinations than can be represented in a finite dataset.

### What data does each instance consist of?

Instances vary by layer but generally include:

**Intent Layer:**
- Control family classification (NIST-inspired)
- Intent vector (objective, asset class, risk domain)
- Standard mappings (abstract references, not text)
- Metadata (timestamps, IDs)

**Execution Layer:**
- All intent layer fields
- Cloud context (provider, service, resource type, region)
- Infrastructure pattern (ID, class, complexity score)
- Compliance state (status, confidence)
- Violation mechanics (failure mode, attack surface, blast radius)
- Evidence model (Terraform signals, runtime signals, detectability)
- Multi-dimensional labels (severity, ML use cases)

**Remediation Layer:**
- Problem pattern description
- Remediation logic (strategy, automation feasibility, effort, steps)
- Cost impact (AWS cost delta, operational overhead, risk reduction)
- AI training signals (autofix capability, approval requirements, complexity)

**Data Types:**
- Strings (IDs, categorical values, descriptions)
- Numbers (scores, confidence levels, costs)
- Booleans (flags for automation, detectability)
- Arrays (steps, checks, use cases)
- Nested objects (structured data)

### Is there a label or target associated with each instance?

Yes, multiple labels depending on the ML use case:

**For Classification Tasks:**
- `compliance_state.status` (compliant/non_compliant/partially_compliant)
- `labeling.severity` (low/medium/high/critical)
- `infrastructure_pattern.pattern_class` (identity_trust, network_exposure, etc.)
- `remediation_logic.strategy` (specific remediation approach)

**For Regression Tasks:**
- `violation_mechanics.blast_radius_score` (0-1 scale)
- `infrastructure_pattern.pattern_complexity` (0-1 scale)
- `cost_impact.risk_reduction_score` (0-1 scale)
- `compliance_state.confidence` (0-1 scale)

**For Multi-Label Classification:**
- `labeling.ml_use_case` (array of applicable scenarios)

**For Binary Classification:**
- `remediation_logic.automation_feasible` (true/false)
- `evidence_model.static_detectable` (true/false)
- `ai_training_signals.can_autofix` (true/false)

### Is any information missing from individual instances?

No. The synthetic generation process ensures all required fields are populated. Optional fields may be absent depending on the layer:
- Intent layer omits cloud-specific details (by design)
- Some remediation records may have simplified cost models

### Are relationships between individual instances made explicit?

**Implicit relationships exist** but are not explicitly linked via foreign keys:
- Intent patterns may appear across multiple execution scenarios
- Execution scenarios with similar `pattern_id` share violation mechanics
- Remediation strategies can apply to multiple problem patterns

Users can join layers on:
- `control_family` + `control_intent_vector.objective`
- `infrastructure_pattern.pattern_class`
- `cloud_context.service` + `cloud_context.resource_type`

A future version may include explicit relationship IDs.

### Are there recommended data splits?

No pre-defined splits. Recommended approaches:

**Stratified by Severity:**
```python
# 70% train, 15% validation, 15% test
# Stratify by labeling.severity to maintain class balance
```

**Stratified by Service:**
```python
# Ensure all AWS services represented in train/val/test
# Stratify by cloud_context.service
```

**Temporal Split (if using generated_at):**
```python
# Simulate production scenario where older data trains new models
# Sort by generated_at, split chronologically
```

**Leave-One-Service-Out:**
```python
# Train on 9 services, test on 1 (generalization testing)
```

### Are there any errors, sources of noise, or redundancies in the dataset?

**Errors:** None known. Synthetic generation follows deterministic rules.

**Noise:** Intentional variation in:
- Confidence scores (0.85-0.99 range for realism)
- Complexity scores (0.3-0.95 range)
- Blast radius scores (realistic distribution)

**Redundancies:** 
- Multiple records may share the same `control_family` or `pattern_class` (by design)
- This represents real-world scenarios where similar violations occur across resources
- No exact duplicate records exist (verified by unique `record_id`)

### Is the dataset self-contained, or does it link to or depend on external resources?

**Self-contained.** The dataset includes:
- All necessary data in JSONL files
- Complete schema specification
- Documentation

**No external dependencies** for basic usage.

**Optional external context:**
- AWS documentation for understanding service-specific fields
- Terraform documentation for resource type details
- NIST 800-53 / CIS / ISO 27001 **for understanding control families** (but not required - the dataset is abstracted)

### Does the dataset contain data that might be considered confidential?

**No.** The dataset is 100% synthetic with:
- No real cloud account information
- No actual IP addresses or credentials
- No customer data or PII
- No proprietary infrastructure configurations

All data is algorithmically generated and does not represent any real organization's environment.

### Does the dataset contain data that, if viewed directly, might be offensive, insulting, threatening, or might otherwise cause anxiety?

No. The dataset contains only technical cloud infrastructure and compliance data.

### Does the dataset identify any subpopulations?

Not applicable. The dataset describes cloud resources and compliance states, not human populations.

### Is it possible to identify individuals from the dataset?

No. The dataset contains zero personal information.

### Does the dataset contain data that might be considered sensitive?

**No sensitive data.** While the dataset describes security violations and remediation strategies, all data is synthetic and does not represent real security vulnerabilities in any actual system.

---

## Collection Process

### How was the data associated with each instance acquired?

**Method:** Algorithmic generation using deterministic pseudorandom functions.

**Process:**
1. Define compliance pattern vocabulary (control families, services, patterns)
2. Create generation rules mapping intent → infrastructure → violation
3. Apply seeded randomization for realistic variation
4. Generate instances according to layer-specific schemas
5. Validate against JSON Schema

### What mechanisms or procedures were used to collect the data?

The `generator.py` script implements a class-based generation system:

```python
class CCEGGenerator:
    def __init__(self):
        random.seed(SEED)  # Reproducibility
    
    def generate_intent_layer(count):
        # Creates abstract intent vectors
    
    def generate_execution_layer(count):
        # Creates cloud-specific scenarios
    
    def generate_remediation_layer(count):
        # Creates fix strategies
```

All data flows through these controlled generation functions - no manual entry or external data sources.

### If the dataset is a sample from a larger set, what was the sampling strategy?

**Not a sample.** The dataset is the complete output of the generation process for version 1.0.

The generation process implements **stratified sampling** to ensure coverage:
- All control families represented proportionally
- All AWS services included
- All severity levels distributed realistically (20%/30%/30%/20%)
- Compliance states weighted toward non-compliant (70%) for training value

### Who was involved in the data collection process and how were they compensated?

**No human data collectors.** Generation is fully automated.

The development team (dataset designers and engineers) are employees/contractors compensated with standard salaries.

### Over what timeframe was the data collected?

**Generation Time:** Less than 5 minutes (deterministic script execution)

**Development Timeframe:** 
- Vocabulary design: 2 weeks
- Generation logic: 3 weeks  
- Validation and testing: 1 week

**Dataset Timestamp:** All records have `generated_at` timestamps from the generation run (January 2025).

### Were any ethical review processes conducted?

**Formal IRB review:** Not applicable (no human subjects).

**Internal ethical review:** Yes, conducted by the development team covering:
- Copyright compliance (ensured no reproduced text)
- Realistic but non-exploitable patterns (no actual vulnerability details)
- Potential misuse scenarios (addressed in usage guidelines)

### Did you collect the data from the individuals in question directly, or obtain it via third parties or other sources?

Not applicable. No data collected from individuals.

### Were the individuals in question notified about the data collection?

Not applicable. No individuals involved.

### Did the individuals in question consent to the collection and use of their data?

Not applicable. No individuals involved.

### If consent was obtained, were the consenting individuals provided with a mechanism to revoke their consent in the future or for certain uses?

Not applicable. No consent required.

### Has an analysis of the potential impact of the dataset and its use on data subjects been conducted?

Not applicable. No data subjects.

---

## Preprocessing/Cleaning/Labeling

### Was any preprocessing/cleaning/labeling of the data done?

**Preprocessing:** None required. Data generated in final format.

**Validation:** 
- JSON Schema validation for all records
- Field type checking
- Enum value verification
- Range validation for numeric scores

**Labeling:** 
- Multi-dimensional labels generated as part of the synthetic process
- Labels are deterministic based on pattern characteristics

### Was the "raw" data saved in addition to the preprocessed/cleaned/labeled data?

The "raw" data IS the final data. The generation script directly produces JSONL output.

The script itself (`generator.py`) serves as the "raw data" definition - users can regenerate identical output by running with the same seed.

### Is the software that was used to preprocess/clean/label the data available?

Yes. The `generator.py` script is provided with commercial licenses and includes:
- All generation logic
- Validation functions
- Export to JSONL
- Schema generation

**Dependencies:**
- Python 3.8+
- Standard library only (json, random, hashlib, datetime)
- NumPy (optional, for advanced randomization)

---

## Uses

### Has the dataset been used for any tasks already?

**Initial Release** - Not yet deployed in production systems.

**Development Testing:**
- Policy classification model training (proof-of-concept)
- Risk scoring regression models
- Auto-remediation strategy selection

### Is there a repository that links to any or all papers or systems that use the dataset?

Will be established post-release at: `https://cceg-dataset.com/research`

### What (other) tasks could the dataset be used for?

**Primary Use Cases:**
1. **Policy Classification** - Categorize compliance violations
2. **Risk Scoring** - Predict blast radius and severity
3. **Auto-Remediation** - Generate Terraform fixes
4. **Drift Detection** - Identify configuration changes
5. **Compliance Posture Assessment** - Dashboard visualization

**Extended Use Cases:**
6. **Anomaly Detection** - Flag unusual compliance patterns
7. **Cost-Benefit Analysis** - Evaluate remediation ROI
8. **Approval Workflow Automation** - Route high-risk changes
9. **LLM Fine-Tuning** - Train models on compliance reasoning
10. **Security Benchmarking** - Compare infrastructure against baselines

### Is there anything about the composition of the dataset or the way it was collected and preprocessed/cleaned/labeled that might impact future uses?

**Synthetic Nature:** 
- Models trained on this data may not generalize to all real-world edge cases
- Recommended to combine with production telemetry for deployment

**AWS-Only:** 
- Version 1.0 covers only AWS
- Azure/GCP support planned for v1.1

**Pattern Coverage:**
- 10+ common patterns included
- Rare or novel attack vectors not represented

**Temporal Limitations:**
- Generated with 2025 AWS service knowledge
- New services/features not included until future versions

### Are there tasks for which the dataset should not be used?

**Do NOT use for:**
1. **Legal Compliance Determination** - This dataset trains ML models; it does not constitute legal advice or guarantee compliance with any regulatory framework
2. **Production Security Decisions Without Validation** - Synthetic data should be validated against real infrastructure before deployment
3. **Bypassing Security Controls** - Do not use violation patterns to exploit systems
4. **Claiming Standard Conformance** - Records reference abstract control families, not actual NIST/CIS/ISO requirements

**Recommended Prohibitions:**
- Do not use to train models that auto-remediate without human approval on critical infrastructure
- Do not use as sole source for regulatory audit preparation
- Do not distribute violation mechanics to untrusted parties

---

## Distribution

### Will the dataset be distributed to third parties outside of the entity on behalf of which the dataset was created?

**Yes.** This is a commercial dataset intended for distribution to:
- ML/AI companies building compliance automation tools
- Cloud security vendors
- Research institutions
- Enterprise security teams

### How will the dataset be distributed?

**Distribution Channels:**
1. **Direct Licensing** - Contact licensing@cceg-dataset.com
2. **ML Platform Marketplaces** - Hugging Face, AWS Data Exchange (planned)
3. **Research Program** - Academic licenses available

**Format:** 
- JSONL files (compressed .tar.gz)
- Includes generator script, schema, documentation

**Delivery:** Digital download or S3 bucket access

### When will the dataset be distributed?

**Initial Release:** Q1 2025  
**Platform Availability:** Q2 2025

### Will the dataset be distributed under a copyright or other intellectual property license?

**Yes.** Commercial license with standard terms:
- **Permitted:** ML training, commercial product development, research publication
- **Restricted:** Redistribution without modification, sub-licensing
- **Prohibited:** Claiming as own work, removing attribution

**Academic Exception:** Research-only licenses available for non-commercial use.

### Have any third parties imposed IP-based or other restrictions on the data?

**No.** The dataset is fully synthetic and contains no third-party IP.

### Do any export controls or other regulatory restrictions apply?

**Standard Export Controls:** 
- Subject to U.S. export regulations
- No specific ITAR or EAR restrictions (not defense articles or dual-use technology)
- Standard commercial software export rules apply

**GDPR/Privacy:** Not applicable (no personal data)

---

## Maintenance

### Who will be supporting/hosting/maintaining the dataset?

**CCEG Team** provides:
- Technical support (support@cceg-dataset.com)
- Bug fixes and schema updates
- Documentation improvements

### How can the owner/curator/manager of the dataset be contacted?

- **General Inquiries:** ranasingheinfrastructure@gmail.com
- **Commercial Licensing:**ranasingheinfrastructure@gmail.com
- **Technical Support:**ranasingheinfrastructure@gmail.com
- **GitHub Issues:** github.com/cceg-dataset/cceg (for bugs)

### Is there an erratum?

Will be maintained at: `https://cceg-dataset.com/erratum`

Currently: No known errors.

### Will the dataset be updated?

**Yes.** Planned update schedule:

**v1.1 (Q2 2025):**
- Azure and GCP support
- Additional AWS services (ECS, EKS, Fargate)
- Extended pattern library

**v2.0 (Q3 2025):**
- 50,000+ records
- New control families (IR, BC, DR)
- Multi-cloud scenarios
- Real-time drift patterns

**Versioning:** Semantic versioning (MAJOR.MINOR.PATCH)

### If the dataset relates to people, are there applicable limits on the retention of the data?

Not applicable. No data about people.

### Will older versions of the dataset continue to be supported/hosted/maintained?

**Yes.** All major versions will remain available to licensees:
- v1.x supported for 2 years after v2.0 release
- Downloads available indefinitely for licensees
- Schema compatibility maintained

### If others want to extend/augment/build on/contribute to the dataset, is there a mechanism for them to do so?

**Community Contributions:** Accepted via:
1. GitHub pull requests (for new patterns or services)
2. Partner program (for major extensions like new cloud providers)
3. Research collaborations (for novel generation techniques)

**Requirements:**
- Maintain synthetic, copyright-free approach
- Follow schema standards
- Provide validation tests

---

## Legal & Ethical Considerations

### Were any ethical review processes conducted?

**Internal Review:** Yes, covering:
- Copyright compliance verification
- Realistic but non-exploitable pattern design
- Potential misuse scenarios and mitigations
- Licensing terms and restrictions

**External Review:** None conducted (not required for synthetic technical data).

### Does the dataset relate to people?

**No.** The dataset describes cloud infrastructure resources, not people.

### Does the dataset identify any subpopulations?

**No.** Not applicable to infrastructure data.

### Is it possible to identify individuals from the dataset?

**No.** Zero personal information included.

### Does the dataset contain data that might be considered sensitive in any way?

**Security Context:** The dataset describes security violations and remediation strategies. While this could be considered "sensitive" in a security context:

- All patterns are **well-documented in public security literature**
- No actual vulnerabilities in real systems are disclosed
- Patterns are abstracted and do not include exploit code
- Intended use is defensive (compliance automation), not offensive

**Recommendation:** Licensees should restrict access to the dataset to authorized security personnel.

### Any other comments?

**Copyright Compliance Guarantee:**  
This dataset was specifically designed to avoid copyright infringement. It contains:
- ✅ NO text from NIST 800-53 controls
- ✅ NO text from CIS Benchmark requirements  
- ✅ NO text from ISO 27001 clauses
- ✅ ONLY synthetic abstractions of control intent

Legal review confirmed compliance with intellectual property law.

**Quality Assurance:**
- All records pass JSON Schema validation
- Deterministic generation ensures reproducibility
- Stratified sampling provides balanced representation
- Real-world consultation informed pattern design

**Ethical AI Considerations:**
- Dataset designed to improve security, not exploit systems
- Automation feasibility flags prevent over-reliance on auto-remediation
- Cost/risk scores support human decision-making
- Approval workflow fields encourage human oversight

---

**Document Version:** 1.0.0  
**Last Updated:** January 8, 2025  
**Authors:** CCEG Dataset Team  
**Contact:** ranasingheinfrastructure@gmail.com
