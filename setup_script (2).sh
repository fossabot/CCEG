#!/bin/bash
# CCEG Dataset Setup Script
# Creates directory structure and generates dataset

set -e  # Exit on error

echo "=============================================="
echo "CCEG Dataset Setup"
echo "=============================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.8+ required (found $python_version)"
    exit 1
fi

echo "✅ Python $python_version detected"
echo ""

# Create directory structure
echo "Creating directory structure..."
mkdir -p dataset/jsonl
mkdir -p dataset/schemas
mkdir -p examples
mkdir -p logs

echo "✅ Directories created"
echo ""

# Check for required Python packages
echo "Checking Python dependencies..."

packages=("numpy")
missing_packages=()

for package in "${packages[@]}"; do
    if ! python3 -c "import $package" 2>/dev/null; then
        missing_packages+=($package)
    fi
done

if [ ${#missing_packages[@]} -gt 0 ]; then
    echo "⚠️  Missing packages: ${missing_packages[*]}"
    echo "Installing dependencies..."
    pip install numpy
    echo "✅ Dependencies installed"
else
    echo "✅ All dependencies satisfied"
fi
echo ""

# Generate dataset
echo "Generating dataset (this may take a few moments)..."
echo "=============================================="

if [ -f "generator.py" ]; then
    python3 generator.py 2>&1 | tee logs/generation_$(date +%Y%m%d_%H%M%S).log
    
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        echo ""
        echo "✅ Dataset generation complete!"
    else
        echo ""
        echo "❌ Dataset generation failed. Check logs/ for details."
        exit 1
    fi
else
    echo "❌ Error: generator.py not found"
    exit 1
fi

echo ""
echo "=============================================="
echo "Validating dataset..."
echo "=============================================="
echo ""

# Optional: Run validation if available
if [ -f "validate_schema.py" ]; then
    # Check if jsonschema is available
    if python3 -c "import jsonschema" 2>/dev/null; then
        echo "Running schema validation..."
        python3 validate_schema.py
    else
        echo "⚠️  jsonschema not installed - skipping validation"
        echo "   Install with: pip install jsonschema"
    fi
else
    echo "⚠️  validate_schema.py not found - skipping validation"
fi

echo ""
echo "=============================================="
echo "Setup Complete!"
echo "=============================================="
echo ""
echo "Dataset files created:"
echo "  📁 dataset/jsonl/cceg_intent.jsonl        (2,000 records)"
echo "  📁 dataset/jsonl/cceg_execution.jsonl     (5,000 records)"
echo "  📁 dataset/jsonl/cceg_remediation.jsonl   (3,000 records)"
echo ""
echo "Next steps:"
echo "  1. Review README.md for dataset overview"
echo "  2. Check DATASHEET.md for full documentation"
echo "  3. Run validation: python3 validate_schema.py"
echo "  4. Explore data: jupyter notebook examples/quickstart.ipynb"
echo ""
echo "For support: support@cceg-dataset.com"
echo ""
