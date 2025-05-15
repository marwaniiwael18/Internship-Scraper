#!/bin/bash

# IT Engineering Internship Scraper Runner
# ---------------------------------------
# Simple script to run the IT internship scraper

# Move to the script directory
cd "$(dirname "$0")" || exit 1

# Display banner
echo "============================================"
echo "   IT ENGINEERING INTERNSHIP SCRAPER"
echo "============================================"

# Ensure Poetry is in PATH
export PATH="$HOME/.local/bin:$PATH"

# Check for arguments
if [ "$1" == "--scrape" ]; then
    echo "Running complete workflow (scrape + filter + send)"
    poetry run python it_internship.py --all
elif [ "$1" == "--today" ]; then
    echo "Filtering and sending today's results only"
    poetry run python it_internship.py --send --today
elif [ "$1" == "--recent" ]; then
    days=${2:-3}  # Default to 3 days if not specified
    echo "Filtering and sending results from the last $days days"
    poetry run python it_internship.py --send --days "$days"
else
    echo "Filtering and sending recent results (3 days)"
    poetry run python it_internship.py --send --days 3
fi

echo "============================================"
echo "   COMPLETED"
echo "============================================"