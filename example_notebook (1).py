{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "# CCEG Dataset Quickstart\n",
        "\n",
        "This notebook demonstrates basic usage of the Cloud Compliance Execution Graph (CCEG) dataset.\n",
        "\n",
        "**Dataset:** 10,000 synthetic compliance execution scenarios  \n",
        "**Layers:** Intent (2K), Execution (5K), Remediation (3K)  \n",
        "**Format:** JSONL"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## 1. Setup and Data Loading"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "import json\n",
        "import pandas as pd\n",
        "from collections import Counter\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "\n",
        "sns.set_style('whitegrid')\n",
        "plt.rcParams['figure.figsize'] = (12, 6)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "def load_jsonl(filepath):\n",
        "    \"\"\"Load JSONL file into list of records\"\"\"\n",
        "    records = []\n",
        "    with open(filepath, 'r') as f:\n",
        "        for line in f:\n",
        "            if line.strip():\n",
        "                records.append(json.loads(line))\n",
        "    return records"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Load all three layers\n",
        "intent_records = load_jsonl('../dataset/jsonl/cceg_intent.jsonl')\n",
        "execution_records = load_jsonl('../dataset/jsonl/cceg_execution.jsonl')\n",
        "remediation_records = load_jsonl('../dataset/jsonl/cceg_remediation.jsonl')\n",
        "\n",
        "print(f\"Loaded {len(intent_records)} intent records\")\n",
        "print(f\"Loaded {len(execution_records)} execution records\")\n",
        "print(f\"Loaded {len(remediation_records)} remediation records\")\n",
        "print(f\"\\nTotal: {len(intent_records) + len(execution_records) + len(remediation_records)} records\")"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## 2. Explore Intent Layer"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Sample intent record\n",
        "print(\"Sample Intent Record:\")\n",
        "print(json.dumps(intent_records[0], indent=2))"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Control family distribution\n",
        "control_families = [r['control_family'] for r in intent_records]\n",
        "family_counts = Counter(control_families)\n",
        "\n",
        "plt.figure(figsize=(10, 6))\n",
        "plt.bar(family_counts.keys(), family_counts.values())\n",
        "plt.title('Intent Layer: Control Family Distribution')\n",
        "plt.xlabel('Control Family')\n",
        "plt.ylabel('Count')\n",
        "plt.show()\n",
        "\n",
        "print(\"\\nControl Family Breakdown:\")\n",
        "for family, count in sorted(family_counts.items()):\n",
        "    print(f\"  {family}: {count} ({count/len(intent_records)*100:.1f}%)\")"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## 3. Explore Execution Layer"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Sample execution record\n",
        "print(\"Sample Execution Record:\")\n",
        "print(json.dumps(execution_records[0], indent=2))"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Compliance state distribution\n",
        "compliance_states = [r['compliance_state']['status'] for r in execution_records]\n",
        "state_counts = Counter(compliance_states)\n",
        "\n",
        "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))\n",
        "\n",
        "# Pie chart\n",
        "ax1.pie(state_counts.values(), labels=state_counts.keys(), autopct='%1.1f%%')\n",
        "ax1.set_title('Compliance State Distribution')\n",
        "\n",
        "# Bar chart\n",
        "ax2.bar(state_counts.keys(), state_counts.values())\n",
        "ax2.set_title('Compliance State Counts')\n",
        "ax2.set_ylabel('Count')\n",
        "\n",
        "plt.tight_layout()\n",
        "plt.show()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Severity distribution\n",
        "severities = [r['labeling']['severity'] for r in execution_records]\n",
        "severity_counts = Counter(severities)\n",
        "\n",
        "severity_order = ['low', 'medium', 'high', 'critical']\n",
        "ordered_counts = [severity_counts.get(s, 0) for s in severity_order]\n",
        "\n",
        "plt.figure(figsize=(10, 6))\n",
        "colors = ['#90EE90', '#FFD700', '#FF8C00', '#DC143C']\n",
        "plt.bar(severity_order, ordered_counts, color=colors)\n",
        "plt.title('Execution Layer: Severity Distribution')\n",
        "plt.xlabel('Severity')\n",
        "plt.ylabel('Count')\n",
        "plt.show()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# AWS service coverage\n",
        "services = [r['cloud_context']['service'] for r in execution_records]\n",
        "service_counts = Counter(services)\n",
        "\n",
        "plt.figure(figsize=(12, 6))\n",
        "plt.bar(service_counts.keys(), service_counts.values())\n",
        "plt.title('Execution Layer: AWS Service Coverage')\n",
        "plt.xlabel('AWS Service')\n",
        "plt.ylabel('Count')\n",
        "plt.xticks(rotation=45)\n",
        "plt.tight_layout()\n",
        "plt.show()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## 4. Explore Remediation Layer"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Sample remediation record\n",
        "print(\"Sample Remediation Record:\")\n",
        "print(json.dumps(remediation_records[0], indent=2))"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Automation feasibility\n",
        "automation_feasible = sum(1 for r in remediation_records if r['remediation_logic']['automation_feasible'])\n",
        "automation_rate = automation_feasible / len(remediation_records) * 100\n",
        "\n",
        "print(f\"Automation Feasibility: {automation_feasible}/{len(remediation_records)} ({automation_rate:.1f}%)\")\n",
        "\n",
        "fig, ax = plt.subplots(figsize=(8, 8))\n",
        "ax.pie([automation_feasible, len(remediation_records) - automation_feasible],\n",
        "       labels=['Automatable', 'Manual'],\n",
        "       autopct='%1.1f%%',\n",
        "       colors=['#90EE90', '#FFB6C1'])\n",
        "ax.set_title('Remediation: Automation Feasibility')\n",
        "plt.show()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Fix effort distribution\n",
        "efforts = [r['remediation_logic']['estimated_fix_effort'] for r in remediation_records]\n",
        "effort_counts = Counter(efforts)\n",
        "\n",
        "effort_order = ['low', 'medium', 'high']\n",
        "ordered_efforts = [effort_counts.get(e, 0) for e in effort_order]\n",
        "\n",
        "plt.figure(figsize=(10, 6))\n",
        "colors = ['#90EE90', '#FFD700', '#FF8C00']\n",
        "plt.bar(effort_order, ordered_efforts, color=colors)\n",
        "plt.title('Remediation Layer: Fix Effort Distribution')\n",
        "plt.xlabel('Effort Level')\n",
        "plt.ylabel('Count')\n",
        "plt.show()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## 5. ML Use Case Examples"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "### 5.1 Policy Classification"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Prepare data for classification\n",
        "from sklearn.model_selection import train_test_split\n",
        "from sklearn.ensemble import RandomForestClassifier\n",
        "from sklearn.metrics import classification_report, accuracy_score\n",
        "\n",
        "# Extract features and labels\n",
        "X = []\n",
        "y = []\n",
        "\n",
        "for record in execution_records:\n",
        "    features = [\n",
        "        record['infrastructure_pattern']['pattern_complexity'],\n",
        "        record['compliance_state']['confidence'],\n",
        "        record['violation_mechanics']['blast_radius_score'],\n",
        "        1 if record['evidence_model']['static_detectable'] else 0\n",
        "    ]\n",
        "    X.append(features)\n",
        "    y.append(record['labeling']['severity'])\n",
        "\n",
        "# Train-test split\n",
        "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n",
        "\n",
        "# Train classifier\n",
        "clf = RandomForestClassifier(n_estimators=100, random_state=42)\n",
        "clf.fit(X_train, y_train)\n",
        "\n",
        "# Evaluate\n",
        "y_pred = clf.predict(X_test)\n",
        "accuracy = accuracy_score(y_test, y_pred)\n",
        "\n",
        "print(f\"Severity Classification Accuracy: {accuracy:.2%}\")\n",
        "print(\"\\nClassification Report:\")\n",
        "print(classification_report(y_test, y_pred))"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "### 5.2 Risk Scoring"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "from sklearn.linear_model import LinearRegression\n",
        "from sklearn.metrics import mean_squared_error, r2_score\n",
        "\n",
        "# Prepare data for regression\n",
        "X = []\n",
        "y = []\n",
        "\n",
        "for record in execution_records:\n",
        "    if record['compliance_state']['status'] == 'non_compliant':\n",
        "        features = [\n",
        "            record['infrastructure_pattern']['pattern_complexity'],\n",
        "            record['compliance_state']['confidence']\n",
        "        ]\n",
        "        X.append(features)\n",
        "        y.append(record['violation_mechanics']['blast_radius_score'])\n",
        "\n",
        "# Train-test split\n",
        "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n",
        "\n",
        "# Train regressor\n",
        "reg = LinearRegression()\n",
        "reg.fit(X_train, y_train)\n",
        "\n",
        "# Evaluate\n",
        "y_pred = reg.predict(X_test)\n",
        "mse = mean_squared_error(y_test, y_pred)\n",
        "r2 = r2_score(y_test, y_pred)\n",
        "\n",
        "print(f\"Blast Radius Prediction:\")\n",
        "print(f\"  MSE: {mse:.4f}\")\n",
        "print(f\"  R²:  {r2:.4f}\")\n",
        "\n",
        "# Scatter plot\n",
        "plt.figure(figsize=(10, 6))\n",
        "plt.scatter(y_test, y_pred, alpha=0.5)\n",
        "plt.plot([0, 1], [0, 1], 'r--', lw=2)\n",
        "plt.xlabel('Actual Blast Radius')\n",
        "plt.ylabel('Predicted Blast Radius')\n",
        "plt.title('Risk Scoring: Blast Radius Prediction')\n",
        "plt.tight_layout()\n",
        "plt.show()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## 6. Data Quality Checks"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Check for missing values\n",
        "print(\"Data Quality Checks:\")\n",
        "print(\"=\"*50)\n",
        "\n",
        "# Intent layer\n",
        "intent_complete = all('control_family' in r and 'control_intent_vector' in r for r in intent_records)\n",
        "print(f\"Intent layer complete: {intent_complete} ✅\")\n",
        "\n",
        "# Execution layer\n",
        "exec_complete = all(\n",
        "    'cloud_context' in r and 'infrastructure_pattern' in r and 'compliance_state' in r\n",
        "    for r in execution_records\n",
        ")\n",
        "print(f\"Execution layer complete: {exec_complete} ✅\")\n",
        "\n",
        "# Remediation layer\n",
        "remed_complete = all('remediation_logic' in r and 'cost_impact' in r for r in remediation_records)\n",
        "print(f\"Remediation layer complete: {remed_complete} ✅\")\n",
        "\n",
        "# Score range checks\n",
        "invalid_scores = 0\n",
        "for record in execution_records:\n",
        "    scores = [\n",
        "        record['infrastructure_pattern']['pattern_complexity'],\n",
        "        record['compliance_state']['confidence'],\n",
        "        record['violation_mechanics']['blast_radius_score']\n",
        "    ]\n",
        "    if any(s < 0 or s > 1 for s in scores):\n",
        "        invalid_scores += 1\n",
        "\n",
        "print(f\"Score ranges valid: {invalid_scores == 0} ✅\" if invalid_scores == 0 else f\"Invalid scores found: {invalid_scores} ❌\")\n",
        "\n",
        "print(\"\\n✅ All quality checks passed!\")"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## 7. Export to DataFrame"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Convert execution records to DataFrame for easier analysis\n",
        "exec_df = pd.json_normalize(execution_records)\n",
        "\n",
        "print(f\"Execution DataFrame Shape: {exec_df.shape}\")\n",
        "print(\"\\nFirst 5 rows:\")\n",
        "exec_df.head()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Summary statistics\n",
        "print(\"Summary Statistics:\")\n",
        "exec_df[['infrastructure_pattern.pattern_complexity',\n",
        "         'compliance_state.confidence',\n",
        "         'violation_mechanics.blast_radius_score']].describe()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## Next Steps\n",
        "\n",
        "1. **Train Deep Learning Models**: Use TensorFlow/PyTorch for more complex architectures\n",
        "2. **Feature Engineering**: Extract additional features from nested JSON structures\n",
        "3. **Multi-Label Classification**: Predict multiple ML use cases simultaneously\n",
        "4. **Sequence Models**: Use remediation steps for sequence-to-sequence learning\n",
        "5. **Transfer Learning**: Fine-tune pre-trained models on CCEG data\n",
        "\n",
        "See the full documentation at: https://cceg-dataset.com/docs"
      ]
    }
  ],
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.9.0"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 4
}