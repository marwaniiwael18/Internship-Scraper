#!/usr/bin/env python
"""
IT Filtering Enhancement Script
--------------------------------
This script enhances the filtering of IT engineering internships by:
1. Setting a strict 3-day limit for recent listings
2. Adding additional filtering to ensure only IT engineering positions are included
3. Improves handling of dates and position categorization
"""
import os
import csv
import datetime
from pathlib import Path
from typing import List, Dict, Any

# Project paths
PROJECT_ROOT = Path("/Users/macbook/Desktop/internship-scraper")
OUTPUT_DIR = PROJECT_ROOT / "output"
RESULTS_FILE = OUTPUT_DIR / "it_results.csv"
FILTERED_RESULTS_FILE = OUTPUT_DIR / "it_internships.csv"

# IT Keywords for filtering
IT_KEYWORDS = [
    "software", "developer", "development", "engineering", "it", "tech", 
    "computer", "programming", "web", "mobile", "data", "devops", "cloud",
    "fullstack", "backend", "frontend", "qa", "sde", "swe", "code", "coding",
    "systems", "cybersecurity", "database", "application", "ai", "machine learning",
    "python", "java", "javascript", "typescript", "c++", "c#", "react", "angular",
    "node", "aws", "azure", "devops", "docker", "kubernetes", "gitlab", "github"
]

# Internship keywords
INTERNSHIP_KEYWORDS = ["intern", "internship", "alternance", "stage", "trainee"]

# Exclusion terms - positions we don't want even if they match other criteria
EXCLUDE_TERMS = [
    "non-tech", "non tech", "accounting", "finance", "sales", "marketing", 
    "recruiter", "hr ", "human resources", "administrative", "business development"
]

def read_csv_data(file_path: str) -> List[Dict[str, str]]:
    """Read internship data from a CSV file."""
    if not os.path.exists(file_path):
        print(f"Warning: File {file_path} does not exist")
        return []
        
    internships = []
    try:
        # First check if file is empty
        if os.path.getsize(file_path) == 0:
            print(f"Warning: File {file_path} is empty")
            return []
            
        # Read the file and check the content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()
            
        if not content:
            return []
            
        # Check if the file has a header row
        first_line = content[0].strip()
        if "company" not in first_line.lower():
            # No header, we need to add one
            fieldnames = ["company", "title", "location", "link", "date"]
            
            # Re-read with fieldnames
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, fieldnames=fieldnames, delimiter='|')
                for row in reader:
                    internships.append(row)
        else:
            # Has header, read normally
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


def is_it_engineering_internship(title: str) -> bool:
    """Enhanced check if a job title is an IT engineering internship/alternance."""
    if not title:
        return False
        
    title_lower = title.lower()
    
    # Data science is considered part of IT
    if "data scientist" in title_lower or "data science" in title_lower:
        return True
    
    # Software engineering is always IT
    if "software" in title_lower and ("engineer" in title_lower or "developer" in title_lower):
        return True
    
    # Check if it has direct IT-related keywords
    direct_it_terms = ["software", "developer", "engineering", "computer science", 
                        "web", "mobile", "fullstack", "backend", "frontend", "cloud"]
    is_direct_it = any(term in title_lower for term in direct_it_terms)
    
    # Check if it's an internship/alternance (must match at least one keyword)
    is_internship = any(keyword in title_lower for keyword in INTERNSHIP_KEYWORDS)
    
    # Check if it contains any exclusion terms (must not match any)
    has_exclusion = any(term in title_lower for term in EXCLUDE_TERMS)
    
    # Special case for general engineering positions from tech companies
    # These are usually IT-related even if not explicitly mentioned
    tech_companies = ["google", "microsoft", "amazon", "apple", "meta", "spacex", 
                     "ibm", "oracle", "sap", "accenture", "cisco"]
    is_tech_company = any(company in title_lower for company in tech_companies)
    
    # Return True for IT-related positions
    if is_direct_it and is_internship and not has_exclusion:
        return True
    
    # Return True for tech company engineering positions
    if is_tech_company and "engineer" in title_lower and is_internship and not has_exclusion:
        return True
    
    return False


def filter_recent_internships(internships: List[Dict[str, str]], days: int = 3) -> List[Dict[str, str]]:
    """Filter internships to STRICTLY include only those that are exactly max_days old or newer."""
    today = datetime.datetime.now().date()
    recent_internships = []
    
    print(f"STRICT FILTERING: Including ONLY internships from the last {days} days...")
    print(f"Today's date: {today}")
    
    for internship in internships:
        try:
            # Get the date from the internship data
            date_str = internship.get('date', '')
            
            # If no date field, skip this entry
            if not date_str:
                continue
                
            # Try to parse the date
            try:
                post_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                # Try alternate format
                try:
                    post_date = datetime.datetime.strptime(date_str, '%d %b %Y').date()
                except ValueError:
                    # If we can't parse the date, skip this entry
                    continue
            
            # Calculate days difference
            days_old = (today - post_date).days
            
            # STRICT: Only include entries that are exactly N days old or newer (0 to N days)
            if 0 <= days_old <= days:
                recent_internships.append(internship)
                
        except Exception as e:
            print(f"Error processing date for entry: {e}")
            # Skip this entry if there's any error processing the date
            continue
    
    print(f"Strict filtering: Found {len(recent_internships)} internships that are EXACTLY {days} days old or newer")
    print(f"Any older internships have been removed")
    return recent_internships


def main():
    """Main function to enhance filtering."""
    print("=" * 60)
    print("IT ENGINEERING INTERNSHIP FILTER ENHANCEMENT")
    print("=" * 60)
    
    # Read existing internship data
    if not os.path.exists(RESULTS_FILE):
        print(f"Error: Results file not found at {RESULTS_FILE}")
        return
    
    all_internships = read_csv_data(str(RESULTS_FILE))
    print(f"Read {len(all_internships)} internships from {RESULTS_FILE}")
    
    # Filter for IT engineering internships with enhanced criteria
    filtered_internships = []
    for internship in all_internships:
        if not internship or 'title' not in internship:
            continue
        
        title = internship.get('title', '')
        if not title:
            continue
        
        if is_it_engineering_internship(title):
            # Ensure the date field exists
            if 'date' not in internship or not internship['date']:
                # If no date, add today's date
                internship['date'] = datetime.datetime.now().strftime('%Y-%m-%d')
            
            filtered_internships.append(internship)
    
    print(f"Filtered to {len(filtered_internships)} IT engineering internships")
    
    # Remove duplicates
    seen_links = set()
    unique_internships = []
    for internship in filtered_internships:
        link = internship.get('link', '')
        if link and link not in seen_links:
            seen_links.add(link)
            unique_internships.append(internship)
    
    print(f"Found {len(unique_internships)} unique IT engineering internships")
    
    # Filter for recent internships (last 3 days)
    recent_internships = filter_recent_internships(unique_internships, days=3)
    
    # Save the results
    if recent_internships:
        write_csv_data(recent_internships, str(FILTERED_RESULTS_FILE))
        print(f"Successfully wrote {len(recent_internships)} recent IT engineering internships to {FILTERED_RESULTS_FILE}")
    
    print("=" * 60)
    print("ENHANCEMENT COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
