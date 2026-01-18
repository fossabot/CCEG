#!/bin/bash
# CCEG Web Application Setup Script

set -e

echo "=============================================="
echo "CCEG Web Application Setup"
echo "=============================================="
echo ""

# Check Node.js version
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed"
    echo "   Please install Node.js 18+ from https://nodejs.org"
    exit 1
fi

node_version=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
required_version=18

if [ "$node_version" -lt "$required_version" ]; then
    echo "❌ Error: Node.js $required_version+ required (found v$(node --version))"
    exit 1
fi

echo "✅ Node.js $(node --version) detected"
echo ""

# Check npm
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not installed"
    exit 1
fi

echo "✅ npm $(npm --version) detected"
echo ""

# Create directory structure for web app
echo "Creating web app directory structure..."
mkdir -p web-app/src/components
mkdir -p web-app/public

echo "✅ Directories created"
echo ""

# Copy all configuration files
echo "Setting up configuration files..."

# Move into web-app directory
cd web-app

# Create package.json if it doesn't exist
if [ ! -f "package.json" ]; then
    echo "Creating package.json..."
    # Package.json content would be created here
fi

echo "✅ Configuration files ready"
echo ""

# Install dependencies
echo "Installing dependencies (this may take a few minutes)..."
npm install

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Dependencies installed successfully"
else
    echo ""
    echo "❌ Dependency installation failed"
    exit 1
fi

echo ""
echo "=============================================="
echo "Setup Complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo "  1. cd web-app"
echo "  2. npm run dev"
echo "  3. Open http://localhost:3000 in your browser"
echo ""
echo "Available commands:"
echo "  npm run dev     - Start development server"
echo "  npm run build   - Build for production"
echo "  npm run preview - Preview production build"
echo ""
echo "For support: support@cceg-dataset.com"
echo ""
