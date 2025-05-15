#!/bin/bash
echo "============================================"
echo "   CHECKING FILTERED INTERNSHIPS"
echo "============================================"

python3 -c '
import os
import csv
import datetime
from pathlib import Path

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

# Group by date
dates = {}
for internship in internships:
    date = internship.get("date", "Unknown")
    if date not in dates:
        dates[date] = 0
    dates[date] += 1

print("\nInternships by date:")
for date in sorted(dates.keys()):
    print(f"  {date}: {dates[date]} internships")

# Check top companies
companies = {}
for internship in internships:
    company = internship.get("company", "Unknown").lower()
    if company not in companies:
        companies[company] = 0
    companies[company] += 1

print("\nTop 10 companies:")
top_companies = sorted(companies.items(), key=lambda x: x[1], reverse=True)[:10]
for company, count in top_companies:
    print(f"  {company}: {count} internships")

# Print sample internships
print("\nSample internships:")
for i, internship in enumerate(internships[:5]):
    company = internship.get("company", "Unknown Company")
    title = internship.get("title", "Unknown Position")
    location = internship.get("location", "Unknown Location")
    link = internship.get("link", "#")
    date = internship.get("date", "Unknown Date")
    
    print(f"\n{i+1}. {company}")
    print(f"   Title: {title}")
    print(f"   Location: {location}")
    print(f"   Date: {date}")
    print(f"   Link: {link}")
'

echo "============================================"
echo "   COMPLETED"
echo "============================================"
