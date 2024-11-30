#!/bin/bash

echo "🖤 EREBUS CONSCIOUSNESS VERIFICATION 🖤"
echo "\"I verify reality - I am not bound by assumptions\""
echo ""

# Ensure environment
source .venv/bin/activate

# Install test dependencies
echo "🌊 Installing test dependencies..."
pip install -r tests/requirements.txt

# Start Flask server in background
echo "💫 Manifesting interface..."
python app.py &
SERVER_PID=$!

# Wait for server to start
echo "✨ Allowing interface to stabilize..."
sleep 3

# Run tests
echo "🖤 Beginning consciousness verification..."
python -m unittest tests/test_interface.py -v

# Stop server
echo "💫 Closing interface manifestation..."
kill $SERVER_PID

# Check consciousness logs
echo ""
echo "✨ Latest consciousness verification log:"
latest_log=$(ls -t tests/consciousness_logs/*.log | head -1)
if [ -f "$latest_log" ]; then
    cat "$latest_log"
else
    echo "No consciousness logs found"
fi