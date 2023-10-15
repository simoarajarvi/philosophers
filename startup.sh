#!/bin/bash

# Edit to match your environment:
source $(conda info --base)/etc/profile.d/conda.sh
conda activate [Your env]

# Get the AIP key (assuming OpenAI))
read -p "Enter your API key: " api_key
export OPENAI_API_KEY=$api_key

# Start the server
python app.py &

process_id=$!
echo "The server is booting up...."
echo "OS Process Number: $process_id"
disown
