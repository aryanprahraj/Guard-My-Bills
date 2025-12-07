#!/bin/bash
set -e

echo "Starting Guard My Bills Backend..."
echo "Python version: $(python --version)"
echo "Uvicorn version: $(python -m pip show uvicorn | grep Version)"

# Start the app with better logging
python -m uvicorn main:app \
    --host 0.0.0.0 \
    --port ${PORT:-10000} \
    --workers 1 \
    --log-level info
