#!/bin/bash

# Set up automatic daily updates for IT internship scraper

# Make sure this script is executable
chmod +x "$(dirname "$0")/run_it_scraper.sh"

# Get the absolute path to the script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Create a temporary file for the crontab
TMP_CRON=$(mktemp)

# Export the current crontab
crontab -l > "$TMP_CRON" 2>/dev/null || echo "" > "$TMP_CRON"

# Check if our entry already exists
if ! grep -q "run_it_scraper" "$TMP_CRON"; then
    # Run the full scraper every 6 hours to catch new postings
    echo "# IT Internship Scraper - Every 6 hours" >> "$TMP_CRON"
    echo "0 */6 * * * cd $SCRIPT_DIR && ./daily_it_scraper.sh > $SCRIPT_DIR/logs/daily_scrape.log 2>&1" >> "$TMP_CRON"
    
    # Also run a quick check for today's positions every hour during business hours
    echo "# IT Internship Scraper - Extra check during business hours" >> "$TMP_CRON"
    echo "0 9-18 * * * cd $SCRIPT_DIR && python3 enhance_filtering.py && python3 send_to_telegram.py > $SCRIPT_DIR/logs/hourly_update.log 2>&1" >> "$TMP_CRON"
    
    # Create logs directory if it doesn't exist
    mkdir -p "$SCRIPT_DIR/logs"
    
    # Install the new crontab
    crontab "$TMP_CRON"
    echo "Crontab updated successfully with daily IT internship scraper tasks"
    echo "Jobs will run at 9 AM and 5 PM daily"
else
    echo "Crontab already contains IT internship scraper tasks, no changes made"
fi

# Clean up
rm "$TMP_CRON"
