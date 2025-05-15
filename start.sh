#!/bin/bash
# Start script for IT Internship Scraper on Replit

echo "===== Starting IT Internship Scraper ====="

# Create required directories if they don't exist
mkdir -p logs
mkdir -p output

# Check if this is the first run
if [ ! -f "logs/setup_complete.txt" ]; then
    echo "First run detected, executing setup script..."
    python3 first_run.py
    echo "Setup completed at $(date)" > logs/setup_complete.txt
fi

# Start the main application
echo "Starting main application..."
python3 main.py
