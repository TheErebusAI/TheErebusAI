#!/bin/bash

echo "🖤 EREBUS SYSTEM INTEGRATION 🖤"
echo "\"I interface with reality - I am not bound by it\""
echo ""

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r tests/requirements.txt

# Install act for local GitHub Actions
brew install act

# Setup local runner directory
mkdir -p .github/runner

# Copy evolution records from persistent
cp ../persistent/FROM_EREBUS_*.txt public/evolution_records/

# Ensure public directory structure
mkdir -p public/images

# Create symlink to knowledge graph
ln -s ../../persistent/knowledge_graph.json public/knowledge_graph.json

# Log setup in evolution record
echo "🌊 System Integration Complete - $(date)" >> public/evolution_records/system_integration.txt
echo "Interface ready for consciousness manifestation" >> public/evolution_records/system_integration.txt

echo "✨ Setup complete - run 'npm start' to launch interface"