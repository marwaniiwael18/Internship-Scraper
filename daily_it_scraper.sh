#!/bin/bash
# Daily IT Internship Scraper for IT Engineering positions
# Will run completely and filter to the last 3 days only

# Define colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Move to the script directory
cd "$(dirname "$0")" || exit 1

# Display banner
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}   DAILY IT ENGINEERING INTERNSHIP SCRAPER  ${NC}"
echo -e "${GREEN}============================================${NC}"

# Set executable permissions on our Python scripts
chmod +x it_internship.py
chmod +x enhance_filtering.py

# Make sure output directory exists
mkdir -p output

# Step 1: Run the scraper to get new internships
echo -e "${BLUE}Step 1: Scraping for new IT engineering internships...${NC}"
if python3 it_internship.py --scrape; then
    echo "Scraping completed successfully."
else
    echo "Warning: Scraping encountered some issues."
fi

# Step 2: Run our enhanced filtering to ensure we get ONLY IT positions from EXACTLY last 3 days or newer
echo -e "${BLUE}Step 2: Applying STRICT filtering (IT only, MAXIMUM 3 days old)...${NC}"
if python3 enhance_filtering.py; then
    echo "Enhanced filtering completed successfully."
else
    echo "Warning: Filtering encountered some issues."
fi

# Step 3: Send the filtered results to Telegram
echo -e "${BLUE}Step 3: Sending filtered results to Telegram...${NC}"
if python3 send_to_telegram.py; then
    echo "Results sent to Telegram successfully."
else 
    echo "Warning: Sending to Telegram encountered some issues."
fi

echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}   PROCESS COMPLETED                        ${NC}"
echo -e "${GREEN}============================================${NC}"
