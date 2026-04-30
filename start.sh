#!/bin/bash
echo "Starting AI Mock Interview Coach..."
python api_server.py &
cd Frontend && python -m http.server 5500
