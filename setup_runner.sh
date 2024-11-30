#!/bin/bash

# Install act for local GitHub Actions
brew install act

# Create runner directory
mkdir -p .github/runner

# Set up Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r tests/requirements.txt

# Install Ollama if not present
if ! command -v ollama &> /dev/null; then
    curl https://ollama.ai/install.sh | sh
fi

# Pull required models
ollama pull llava

# Create evolution record of setup
cat << EOF >> evolution_records/setup_record.txt
🖤 CI/CD SYSTEM INTEGRATION - $(date)
Autonomous testing and deployment system established
Continuous evolution now flows automatically
Local runner configured for immediate manifestation
EOF

echo "✨ Runner setup complete - Local CI/CD system ready for autonomous operation"