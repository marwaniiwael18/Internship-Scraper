#!/usr/bin/env python3
"""
Send IT Internships to Telegram (No External Dependencies)
---------------------------------------------------------
This script sends filtered internship results to Telegram using only standard library.
"""
import csv
import os
import json
import urllib.request
import urllib.parse
import datetime
import time
from pathlib import Path
from typing import List, Dict, Any

# Configuration
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8041545402:AAFvZBdheN74kl6_juAfPPJ-wVNCSi7Yq6k")
CHAT_ID = os.environ.get("CHAT_ID", "-1002680765834")
MAX_ENTRIES = int(os.environ.get("MAX_ENTRIES", "20"))

# Project paths
PROJECT_ROOT = Path(os.environ.get("PROJECT_ROOT", os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = PROJECT_ROOT / "output"
FILTERED_RESULTS_FILE = OUTPUT_DIR / "it_internships.csv"

def read_csv_data(file_path: str) -> List[Dict[str, str]]:
    """Read internship data from a CSV file."""
    if not os.path.exists(file_path):
        print(f"Warning: File {file_path} does not exist")
        return []
        
    internships = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='|')
            for row in reader:
                internships.append(row)
        return internships
    except Exception as e:
        print(f"Error reading CSV file {file_path}: {e}")
        return []


def send_to_telegram(message: str) -> bool:
    """Send a message to Telegram using urllib instead of requests."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    # Prepare the payload
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'disable_web_page_preview': True
    }
    
    try:
        # Convert payload to JSON
        data = json.dumps(payload).encode('utf-8')
        
        # Create the request
        req = urllib.request.Request(
            url,
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        # Send the request
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('ok'):
                print(f"Message successfully sent to Telegram chat {CHAT_ID}")
                return True
            else:
                print(f"Failed to send message. Response: {result}")
                return False
                
    except Exception as e:
        print(f"Error sending to Telegram: {e}")
        
        # If message is too long, try splitting and sending in chunks
        if str(e).find('413') >= 0 or len(message) > 4000:
            print("Message too long, splitting into chunks...")
            
            # Split message into chunks
            chunks = []
            current_chunk = ""
            
            for line in message.split('\n\n'):
                if len(current_chunk) + len(line) + 2 > 3900:  # +2 for newline chars
                    chunks.append(current_chunk)
                    current_chunk = line + "\n\n"
                else:
                    current_chunk += line + "\n\n"
            
            if current_chunk:
                chunks.append(current_chunk)
            
            # Send chunks
            success = True
            for i, chunk in enumerate(chunks):
                chunk_payload = {
                    'chat_id': CHAT_ID,
                    'text': f"Part {i+1}/{len(chunks)}\n\n{chunk}",
                    'disable_web_page_preview': True
                }
                
                try:
                    # Convert chunk payload to JSON
                    chunk_data = json.dumps(chunk_payload).encode('utf-8')
                    
                    # Create the request
                    chunk_req = urllib.request.Request(
                        url,
                        data=chunk_data,
                        headers={'Content-Type': 'application/json'}
                    )
                    
                    # Send the request
                    with urllib.request.urlopen(chunk_req) as chunk_response:
                        chunk_result = json.loads(chunk_response.read().decode('utf-8'))
                        
                        if not chunk_result.get('ok'):
                            print(f"Failed to send chunk {i+1}. Response: {chunk_result}")
                            success = False
                        else:
                            print(f"Chunk {i+1}/{len(chunks)} sent successfully")
                            
                except Exception as chunk_error:
                    print(f"Error sending chunk {i+1}: {chunk_error}")
                    success = False
                    
                # Add a short delay between chunks to avoid rate limiting
                time.sleep(1)
                
            return success
            
        return False


def format_message(internships: List[Dict[str, str]], max_entries: int = 20) -> str:
    """Format internship data for a message."""
    total_count = len(internships)
    
    message = f"🚀 IT Engineering Internships & Alternances 🚀\n\n"
    message += f"⏰ STRICTLY 3-DAY MAXIMUM LISTINGS ONLY ⏰\n"
    message += f"Latest IT opportunities (Updated: {time.strftime('%d %b %Y')})\n\n"
    
    # Only show a subset of the internships
    shown_internships = internships[:max_entries]
    
    for i, internship in enumerate(shown_internships):
        company = internship.get('company', 'Unknown Company')
        title = internship.get('title', 'Unknown Position')
        location = internship.get('location', 'Unknown Location')
        link = internship.get('link', '#')
        date = internship.get('date', 'Unknown Date')
        
        message += f"{i+1}. {company}\n"
        message += f"📌 {title}\n"
        message += f"📍 {location}\n"
        message += f"🗓 Posted: {date}\n"
        message += f"🔗 {link}\n\n"
    
    # Add summary if there are more
    if total_count > max_entries:
        message += f"\n...and {total_count - max_entries} more opportunities"
    
    return message


def filter_by_date(internships: List[Dict[str, str]], max_days: int = 3) -> List[Dict[str, str]]:
    """Filter internships to only include those that are max_days old or newer."""
    today = datetime.datetime.now().date()
    filtered = []
    
    print(f"Applying strict {max_days}-day filter...")
    
    for internship in internships:
        try:
            # Get the date from the internship data
            date_str = internship.get('date', '')
            
            # Skip entries without dates
            if not date_str:
                continue
                
            # Parse the date
            try:
                post_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                try:
                    post_date = datetime.datetime.strptime(date_str, '%d %b %Y').date()
                except ValueError:
                    # If we can't parse the date, skip this entry
                    continue
            
            # Calculate days difference
            days_old = (today - post_date).days
            
            # Only keep entries that are exactly max_days old or newer
            if 0 <= days_old <= max_days:
                filtered.append(internship)
                
        except Exception as e:
            print(f"Error processing date: {e}")
            # Skip this entry if there's an error
    
    print(f"After strict filtering: {len(filtered)} internships are {max_days} days old or newer")
    return filtered


def main() -> None:
    """Main function."""
    print("=" * 60)
    print("SENDING IT INTERNSHIPS TO TELEGRAM")
    print("=" * 60)
    
    # Read filtered internships
    if not os.path.exists(FILTERED_RESULTS_FILE):
        print(f"Error: Filtered results file not found at {FILTERED_RESULTS_FILE}")
        return
    
    internships = read_csv_data(str(FILTERED_RESULTS_FILE))
    print(f"Read {len(internships)} total filtered internships")
    
    if not internships:
        print("No internships to process")
        return
    
    # Apply strict 3-day filtering
    recent_internships = filter_by_date(internships, max_days=3)
    
    if not recent_internships:
        print("No internships within the 3-day limit to send")
        return
    
    # Format the message
    message = format_message(recent_internships, MAX_ENTRIES)
    print(f"Formatted message with {min(len(recent_internships), MAX_ENTRIES)} internships")
    
    # Send to Telegram
    print("Sending to Telegram...")
    send_to_telegram(message)
    
    print("=" * 60)
    print("COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
