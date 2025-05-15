#!/usr/bin/env python
"""
IT Engineering Internship Scraper
--------------------------------
A single script that:
1. Scrapes LinkedIn for IT engineering internships & alternances
2. Filters the results for relevant positions
3. Sends them to Telegram

Usage:
    python it_internship.py --scrape   # Run the scraper for new internships
    python it_internship.py --send     # Send existing results to Telegram
    python it_internship.py --all      # Run the complete workflow
"""
import asyncio
import argparse
import csv
import os
import requests
import time
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional 

try:
    from jobpilot.scrapers import LinkedInScraper, ScraperInput
    JOBPILOT_AVAILABLE = True
except ImportError:
    JOBPILOT_AVAILABLE = False
    print("Warning: jobpilot module not available. Scraping functionality will be disabled.")

# === CONFIGURATION ===
BOT_TOKEN = "8041545402:AAFvZBdheN74kl6_juAfPPJ-wVNCSi7Yq6k"
CHAT_ID = "-1002680765834"

# Project paths
PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "output"
RESULTS_FILE = OUTPUT_DIR / "it_results.csv"
FILTERED_RESULTS_FILE = OUTPUT_DIR / "it_internships.csv"

# IT Engineering keywords for filtering
IT_KEYWORDS = [
    "software", "developer", "development", "engineering", "it", "tech", 
    "computer", "programming", "web", "mobile", "data", "devops", "cloud",
    "fullstack", "backend", "frontend", "qa", "sde", "swe", "code", "coding",
    "systems", "cybersecurity", "database", "application"
]

# Internship/alternance keywords
INTERNSHIP_KEYWORDS = ["intern", "internship", "alternance", "stage", "trainee"]

# Companies to focus on
TECH_COMPANIES = [
    "google", "microsoft", "amazon", "apple", "meta", 
    "ibm", "oracle", "sap", "accenture", "capgemini", "cisco"
]

# European countries to search in
EU_COUNTRIES = [
    "france", "germany", "united kingdom", "spain", "italy", "netherlands",
    "belgium", "sweden", "ireland", "switzerland", "portugal", "denmark"
]


# === UTILITY FUNCTIONS ===
def ensure_dir_exists(directory: Path) -> None:
    """Ensure a directory exists."""
    os.makedirs(directory, exist_ok=True)


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


def write_csv_data(data: List[Dict[str, str]], file_path: str) -> bool:
    """Write data to a CSV file."""
    if not data:
        print(f"No data to write to {file_path}")
        return False
        
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=list(data[0].keys()), delimiter='|')
            writer.writeheader()
            writer.writerows(data)
        print(f"Successfully wrote {len(data)} entries to {file_path}")
        return True
    except Exception as e:
        print(f"Error writing CSV file {file_path}: {e}")
        return False


def find_all_result_files() -> List[str]:
    """Find all result CSV files in the output directory."""
    result_files = []
    for dirpath, _, filenames in os.walk(OUTPUT_DIR):
        for filename in filenames:
            if filename == "results.csv" or filename == "filtered_results.csv":
                result_path = os.path.join(dirpath, filename)
                result_files.append(result_path)
    return result_files


# === SCRAPING FUNCTIONS ===
def append_to_results_file(internships: List[Dict[str, str]]) -> None:
    """Append internships to the results file."""
    if not internships:
        return
    
    # Create header if file doesn't exist
    if not os.path.exists(RESULTS_FILE):
        ensure_dir_exists(OUTPUT_DIR)
        with open(RESULTS_FILE, 'w', encoding='utf-8') as file:
            file.write("company|title|location|link|date\n")
    
    # Append internships
    with open(RESULTS_FILE, 'a', encoding='utf-8') as file:
        for internship in internships:
            date_value = internship.get('date', datetime.datetime.now().strftime('%Y-%m-%d'))
            line = f"{internship['company']}|{internship['title']}|{internship['location']}|{internship['link']}|{date_value}\n"
            file.write(line)


def convert_jobpilot_results(jobs: List[Any]) -> List[Dict[str, str]]:
    """Convert jobpilot job results to dictionary format."""
    results = []
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    
    for job in jobs:
        if not hasattr(job, 'company') or not hasattr(job, 'title') or not hasattr(job, 'link'):
            continue
        
        # Try to extract date info from job details
        posting_date = current_date
        if hasattr(job, 'details') and job.details:
            if hasattr(job.details, 'date'):
                posting_date = job.details.date
        
        results.append({
            'company': job.company.name if hasattr(job.company, 'name') else 'Unknown Company',
            'title': job.title,
            'location': str(job.location),
            'link': job.link,
            'date': posting_date  # Add the posting date to our data
        })
    return results


async def scrape_it_internships() -> List[Dict[str, str]]:
    """Scrape IT engineering internships from LinkedIn."""
    if not JOBPILOT_AVAILABLE:
        print("Error: jobpilot module not available. Cannot scrape internships.")
        return []
    
    print("Starting IT engineering internship scraper...")
    scraper = LinkedInScraper()
    all_internships = []
    
    # Generate focused search terms for IT engineering internships/alternances
    search_terms = [
        "software engineering intern",
        "it engineering intern", 
        "computer science intern",
        "IT alternance",
        "engineering alternance",
        "software developer intern"
    ]
    
    # Add company-specific searches
    for company in TECH_COMPANIES[:5]:  # Limit to top 5 companies
        search_terms.append(f"{company} software intern")
        search_terms.append(f"{company} engineering intern")
    
    print(f"Using {len(search_terms)} search terms for IT engineering positions")
    
    # Search for each term in multiple countries
    for search_term in search_terms:
        print(f"Searching for: {search_term}")
        try:
            results = await asyncio.gather(
                *[
                    scraper.scrape(
                        ScraperInput(keywords=search_term, location=country, limit=10),
                        concurrent=False,
                        retry_delay=1
                    )
                    for country in EU_COUNTRIES[:5]  # Limit to first 5 countries
                ],
                return_exceptions=True
            )
            
            # Process results
            for result in results:
                if isinstance(result, Exception):
                    print(f"Error during search: {result}")
                else:
                    # Convert and save results
                    converted_jobs = convert_jobpilot_results(result)
                    append_to_results_file(converted_jobs)
                    all_internships.extend(converted_jobs)
                    
        except Exception as e:
            print(f"Error during search for {search_term}: {e}")
    
    print(f"Found {len(all_internships)} total internship positions")
    return all_internships


# === FILTERING FUNCTIONS ===
def is_it_engineering_internship(title: str) -> bool:
    """Check if a job title is an IT engineering internship/alternance.
    Now with stricter filtering to ensure only IT engineering positions."""
    title_lower = title.lower()
    
    # Check if it's an IT position
    is_it = any(keyword in title_lower for keyword in IT_KEYWORDS)
    
    # Check if it's an internship/alternance
    is_internship = any(keyword in title_lower for keyword in INTERNSHIP_KEYWORDS)
    
    # Exclude non-IT positions that might match keywords accidentally
    exclude_terms = ["non-tech", "non tech", "accounting", "finance", "sales", 
                     "marketing", "recruiter", "hr ", "human resources", 
                     "administrative", "business development"]
    
    has_exclusion = any(term in title_lower for term in exclude_terms)
    
    # Must be both IT and internship, but not contain exclusion terms
    return is_it and is_internship and not has_exclusion


def filter_it_internships(input_files: List[str] = None) -> List[Dict[str, str]]:
    """Filter for IT engineering internships and alternances."""
    all_internships = []
    
    # Determine input files
    if not input_files:
        # If our main results file exists, use it
        if os.path.exists(RESULTS_FILE):
            input_files = [str(RESULTS_FILE)]
        else:
            # Otherwise find all result files
            input_files = find_all_result_files()
    
    # Read all input files
    for file_path in input_files:
        print(f"Reading {file_path}...")
        all_internships.extend(read_csv_data(file_path))
    
    print(f"Processing {len(all_internships)} total internships")
    
    # Filter for IT engineering internships/alternances
    filtered_internships = []
    for internship in all_internships:
        if not internship or 'title' not in internship:
            continue
        
        title = internship.get('title', '')
        if not title:
            continue
        
        if is_it_engineering_internship(title):
            # Ensure the internship has a date field
            if 'date' not in internship:
                # If we don't have a date, add today's date as default
                internship['date'] = datetime.datetime.now().strftime('%Y-%m-%d')
            filtered_internships.append(internship)
    
    # Remove duplicates based on link
    seen_links = set()
    unique_internships = []
    for internship in filtered_internships:
        link = internship.get('link', '')
        if link and link not in seen_links:
            seen_links.add(link)
            unique_internships.append(internship)
    
    print(f"Found {len(unique_internships)} unique IT engineering internships/alternances")
    
    # Save filtered results
    if unique_internships:
        # Make sure our data has the date field in every record
        for internship in unique_internships:
            if 'date' not in internship:
                internship['date'] = datetime.datetime.now().strftime('%Y-%m-%d')
        
        write_csv_data(unique_internships, str(FILTERED_RESULTS_FILE))
    
    return unique_internships


def filter_recent_internships(internships: List[Dict[str, str]], days: int = 4) -> List[Dict[str, str]]:
    """Filter internships to only include those posted in the last N days."""
    if not internships:
        return []
    
    # When days=0, filter for today only; if not a positive number, return all
    if days < 0:
        return internships
        
    today = datetime.datetime.now().date()
    recent_internships = []
    
    # Check if 'date' field exists in the data
    has_date_field = False
    if internships and 'date' in internships[0]:
        has_date_field = True
    
    # If no date field exists but days=0 (today only), return empty list as we can't determine today's posts
    if days == 0 and not has_date_field:
        print("Warning: Cannot filter for today's posts - no date information available")
        # Return a small subset to avoid empty results
        return internships[:min(5, len(internships))]
    
    # If no date field and we want recent posts, just return all as we can't filter
    if not has_date_field:
        print("Warning: No date information available - returning all internships")
        # If we're filtering for recent posts but have no date info, return everything
        return internships
        
    # At this point we have date information, so filter by it
    for internship in internships:
        try:
            # Get the date from the internship data
            date_str = internship.get('date', '')
            
            # If no date field, include it (should not happen at this point)
            if not date_str:
                recent_internships.append(internship)
                continue
                
            # Try to parse the date
            try:
                post_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                # Try alternate format
                try:
                    post_date = datetime.datetime.strptime(date_str, '%d %b %Y').date()
                except ValueError:
                    # If we can't parse the date, include it
                    recent_internships.append(internship)
                    continue
            
            # Calculate days difference
            days_old = (today - post_date).days
            
            # Keep only recent posts
            if days == 0:  # Today only
                if days_old == 0:
                    recent_internships.append(internship)
            else:  # Last N days
                if days_old <= days:
                    recent_internships.append(internship)
                
        except Exception as e:
            # If there's any error processing the date, include it anyway
            print(f"Error processing date: {e}")
            recent_internships.append(internship)
    
    print(f"Filtered to {len(recent_internships)} internships from the last {days} days")
    return recent_internships


# === TELEGRAM FUNCTIONS ===
def format_telegram_message(internships: List[Dict[str, str]], max_entries: int = 20) -> str:
    """Format internship data for a Telegram message."""
    total_count = len(internships)
    
    message = f"🚀 IT Engineering Internships & Alternances 🚀\n\n"
    
    # Simplified message format to avoid Telegram parsing issues
    # Only show a subset of the internships to avoid message length issues
    shown_internships = internships[:max_entries]
    
    for i, internship in enumerate(shown_internships):
        # Strip any problematic characters that could affect markdown
        company = internship.get('company', 'Unknown Company').replace('*', '').replace('_', '')
        title = internship.get('title', 'Unknown Position').replace('*', '').replace('_', '')
        location = internship.get('location', 'Unknown Location').replace('*', '').replace('_', '')
        link = internship.get('link', '#')
        date = internship.get('date', 'Unknown Date')
        
        message += f"{i+1}. {company}\n"
        message += f"📌 {title}\n"
        message += f"📍 {location}\n"
        message += f"🗓 Posted: {date}\n"
        message += f"🔗 {link}\n\n"
    
    # Add summary
    if total_count > max_entries:
        message += f"\n...and {total_count - max_entries} more opportunities"
    
    message += f"\n\nUpdated: {time.strftime('%d %b %Y')}"
    return message


def send_to_telegram(bot_token: str, chat_id: str, message: str) -> bool:
    """Send a message to a Telegram chat."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    # For simplicity, send without markdown to avoid parsing issues
    payload = {
        'chat_id': chat_id,
        'text': message,
        'disable_web_page_preview': True
    }
    
    try:
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            print(f"Message successfully sent to Telegram chat {chat_id}")
            return True
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            
            # If message is too long, try splitting and sending in chunks
            if response.status_code == 400 and len(message) > 4000:
                print("Message too long, splitting into chunks...")
                
                # Split message into chunks of maximum 3900 characters
                # Try to split at double newlines to maintain formatting
                chunks = []
                current_chunk = ""
                
                for line in message.split('\n\n'):
                    if len(current_chunk) + len(line) + 2 > 3900:  # +2 for the newline chars
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
                        'chat_id': chat_id,
                        'text': f"Part {i+1}/{len(chunks)}\n\n{chunk}",
                        'disable_web_page_preview': True
                    }
                    
                    chunk_response = requests.post(url, data=chunk_payload)
                    if chunk_response.status_code != 200:
                        print(f"Failed to send chunk {i+1}. Status code: {chunk_response.status_code}")
                        print(f"Response: {chunk_response.text}")
                        success = False
                    else:
                        print(f"Chunk {i+1}/{len(chunks)} sent successfully")
                
                return success
            
            return False
    except Exception as e:
        print(f"Error sending to Telegram: {e}")
        return False


# === MAIN FUNCTIONS ===
async def main_async(args: argparse.Namespace) -> None:
    """Asynchronous main function for scraping and processing."""
    # Step 1: Run the scraper if requested
    if args.scrape:
        if JOBPILOT_AVAILABLE:
            print("\n=== SCRAPING IT ENGINEERING INTERNSHIPS ===")
            await scrape_it_internships()
        else:
            print("\nError: Cannot scrape - jobpilot module not available")
    
    # Step 2: Filter results if there's data to filter
    filtered_internships = []
    if os.path.exists(FILTERED_RESULTS_FILE):
        # If we already have filtered results, use them directly
        print("\n=== USING EXISTING FILTERED RESULTS ===")
        filtered_internships = read_csv_data(str(FILTERED_RESULTS_FILE))
    else:
        # Otherwise filter from raw data
        print("\n=== FILTERING FOR IT ENGINEERING POSITIONS ===")
        filtered_internships = filter_it_internships()
    
    # Step 3: Filter for recent results (last 3 days only)
    print("\n=== FILTERING FOR RECENT POSTINGS (3 DAYS MAX) ===")
    days_to_include = args.days if hasattr(args, 'days') else 3
    recent_internships = filter_recent_internships(filtered_internships, days_to_include)
    
    # Step 4: Send to Telegram
    if args.send and recent_internships:
        print(f"\n=== SENDING {len(recent_internships)} RECENT RESULTS TO TELEGRAM ===")
        message = format_telegram_message(recent_internships, args.max_entries)
        send_to_telegram(BOT_TOKEN, CHAT_ID, message)


def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="IT Engineering Internship & Alternance Scraper and Telegram Bot"
    )
    parser.add_argument("--scrape", action="store_true", 
                      help="Scrape internships from LinkedIn")
    parser.add_argument("--send", action="store_true",
                      help="Send filtered results to Telegram")
    parser.add_argument("--max_entries", type=int, default=20,
                      help="Maximum entries to send to Telegram")
    parser.add_argument("--days", type=int, default=3,
                      help="Only include internships from the last N days (default: 3)")
    parser.add_argument("--today", action="store_true",
                      help="Only include today's internships (overrides --days)")
    parser.add_argument("--all", action="store_true",
                      help="Run all steps (scrape, filter, send)")
    
    args = parser.parse_args()
    
    # If --all is specified, set all flags
    if args.all:
        args.scrape = True
        args.send = True
    
    # If --today is specified, set days to 0
    if args.today:
        args.days = 0
    
    # If no flags are set, default to filtering and sending
    if not (args.scrape or args.send):
        args.send = True
    
    print("=" * 60)
    print("IT ENGINEERING INTERNSHIP & ALTERNANCE SCRAPER")
    print("=" * 60)
    print(f"Scrape new internships: {args.scrape}")
    print(f"Send to Telegram: {args.send}")
    print(f"Maximum entries: {args.max_entries}")
    print("=" * 60)
    
    # Create output directory if it doesn't exist
    ensure_dir_exists(OUTPUT_DIR)
    
    try:
        # Run the async main function
        asyncio.run(main_async(args))
        
        print("\n" + "=" * 60)
        print("Processing completed successfully!")
        print("=" * 60)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
    except Exception as e:
        print(f"\nError during processing: {e}")


if __name__ == "__main__":
    main()
