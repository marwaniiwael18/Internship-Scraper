#!/bin/bash

# Define colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}   SENDING FILTERED RESULTS TO TELEGRAM     ${NC}"
echo -e "${GREEN}============================================${NC}"

python3 -c '
import os
import csv
import json
import requests
import datetime
from pathlib import Path

# Configuration
BOT_TOKEN = "8041545402:AAFvZBdheN74kl6_juAfPPJ-wVNCSi7Yq6k"
CHAT_ID = "-1002680765834"
MAX_ENTRIES = 20

# Project paths
PROJECT_ROOT = Path("/Users/macbook/Desktop/internship-scraper")
OUTPUT_DIR = PROJECT_ROOT / "output"
FILTERED_RESULTS_FILE = OUTPUT_DIR / "it_internships.csv"

# Read filtered internships
internships = []
try:
    with open(FILTERED_RESULTS_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter="|")
        for row in reader:
            internships.append(row)
    print(f"Read {len(internships)} internships from {FILTERED_RESULTS_FILE}")
except Exception as e:
    print(f"Error reading file: {e}")
    exit(1)

# Filter for most recent 4 days
today = datetime.datetime.now().date()
recent_internships = []

for internship in internships:
    try:
        date_str = internship.get("date", "")
        if not date_str:
            recent_internships.append(internship)
            continue
            
        # Try to parse the date
        try:
            post_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            # Try alternate format
            try:
                post_date = datetime.datetime.strptime(date_str, "%d %b %Y").date()
            except ValueError:
                recent_internships.append(internship)
                continue
        
        # Keep only posts from the last 4 days
        days_old = (today - post_date).days
        if days_old <= 4:
            recent_internships.append(internship)
            
    except Exception as e:
        print(f"Error processing date: {e}")
        recent_internships.append(internship)

print(f"Filtered to {len(recent_internships)} internships from the last 4 days")

# Function to send message to Telegram
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print(f"Message successfully sent to Telegram")
            return True
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            
            # If message is too long, try splitting it
            if len(message) > 4000:
                print("Message too long, splitting into chunks...")
                
                # Create chunks of around 3900 characters (just to be safe)
                chunks = [message[i:i+3900] for i in range(0, len(message), 3900)]
                
                # Send each chunk
                success = True
                for i, chunk in enumerate(chunks):
                    chunk_payload = {
                        "chat_id": CHAT_ID,
                        "text": f"Part {i+1}/{len(chunks)}\n\n{chunk}",
                        "disable_web_page_preview": True
                    }
                    
                    chunk_response = requests.post(url, json=chunk_payload)
                    if chunk_response.status_code != 200:
                        print(f"Failed to send chunk {i+1}")
                        success = False
                
                return success
                
            return False
    except Exception as e:
        print(f"Error sending to Telegram: {e}")
        return False

# Format message with internships
message = "🚀 IT Engineering Internships & Alternances 🚀\n\n"

# Get a subset of internships to show
shown_internships = recent_internships[:MAX_ENTRIES]

# Add each internship
for i, internship in enumerate(shown_internships):
    company = internship.get("company", "Unknown Company")
    title = internship.get("title", "Unknown Position")
    location = internship.get("location", "Unknown Location")
    link = internship.get("link", "#")
    date = internship.get("date", "Unknown Date")
    
    message += f"{i+1}. {company}\n"
    message += f"📌 {title}\n"
    message += f"📍 {location}\n"
    message += f"🗓 Posted: {date}\n"
    message += f"🔗 {link}\n\n"

# Add summary
if len(recent_internships) > MAX_ENTRIES:
    message += f"\n...and {len(recent_internships) - MAX_ENTRIES} more opportunities\n"

message += f"\nUpdated: {datetime.datetime.now().strftime("%d %b %Y")}"

# Send the message
if recent_internships:
    print(f"Sending {len(shown_internships)} internships to Telegram...")
    send_to_telegram(message)
else:
    print("No internships to send")
'

echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}   COMPLETED                                ${NC}"
echo -e "${GREEN}============================================${NC}"
