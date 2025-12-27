#!/bin/bash
# Start the server with HTTPS support

cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start uvicorn with SSL
uvicorn server:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    --ssl-keyfile=key.pem \
    --ssl-certfile=cert.pem
