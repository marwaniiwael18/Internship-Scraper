# IT Engineering Internship Scraper

A powerful tool for finding IT engineering internships and alternances across Europe and sending them directly to your Telegram channel.

## Overview

This project has been optimized to focus specifically on IT engineering internships and alternances within the last 3 days only. Multiple scripts work together to ensure you get the latest offerings delivered instantly.

## Features

- **IT Engineering Focus**: Strictly targets software, IT, engineering positions with enhanced filtering
- **Internships & Alternances**: Finds both internship opportunities and alternance programs
- **Fresh Listings**: Only includes posts from the last 3 days maximum
- **Real-time Alerts**: Runs hourly checks during business hours to catch new postings
- **European Coverage**: Searches across major European tech hubs
- **Telegram Integration**: Sends results directly to your Telegram channel
- **Automated Updates**: Scheduled to run every 6 hours with hourly checks during business hours
- **Dependency-Free Notifications**: Telegram integration works without external libraries

## Setup

```bash
# Install dependencies using Poetry
poetry env use python3.11
poetry install --sync
poetry shell
```

## Usage

### Quick Start

The recommended way to use the tool is with the new daily scraper script:

```bash
# Complete workflow: scrape, filter to IT only & last 3 days, and send to Telegram
./daily_it_scraper.sh
```

### Alternative Options

You can also use the individual components:

```bash
# Enhanced filtering only (process existing data)
python3 enhance_filtering.py

# Send filtered results to Telegram
python3 send_to_telegram.py

# Use the traditional script with 3-day filtering
./run_it_scraper.sh --recent 3
```

### Automated Setup

Set up automatic hourly checks and 6-hourly full scrapes:

```bash
./setup_cron.sh
```

### Advanced Usage

For more control, use the individual Python scripts directly:

```bash
# Send existing filtered results to Telegram
python it_internship.py --send

# Scrape new internships
python it_internship.py --scrape

# Run the complete workflow
python it_internship.py --all

# Only include today's internships
python it_internship.py --send --today

# Specify the number of days to look back
python it_internship.py --send --days 7  # Last 7 days
python it_internship.py --all

# Specify the maximum number of entries to send
python it_internship.py --send --max_entries 15
```



## 24/7 Deployment Options

### Replit (Free)
This project can be deployed on Replit to run 24/7 for free with no credit card required. The setup includes:

- **Web Dashboard**: Visual status monitoring of your scraper
- **Automatic Scheduling**: Runs every 8 hours without manual intervention
- **UptimeRobot Integration**: Keeps your Replit project running 24/7
- **Environment Variables**: Securely stores your Telegram credentials

For step-by-step setup instructions:
- Quick overview: [REPLIT_DEPLOYMENT.md](REPLIT_DEPLOYMENT.md)
- Detailed guide: [REPLIT_SETUP_GUIDE.md](REPLIT_SETUP_GUIDE.md)

## Automation

To automatically run the scraper daily, add this to your crontab:

```bash
# Edit crontab
crontab -e

# Add this line to run at 9 AM daily:
0 9 * * * cd /Users/macbook/Desktop/internship-scraper && ./run_it_scraper.sh --scrape
```

## Automated Daily Updates

To set up automatic daily updates:

```bash
# Set up daily updates at 9 AM (scrape new listings) and 5 PM (send today's listings)
./setup_cron.sh
```

This will:
1. Run a full scrape every morning at 9 AM
2. Send only today's new internships at 5 PM
3. Store logs in the `logs` directory

To view or modify the scheduled tasks:

```bash
crontab -l  # View all cron jobs
crontab -e  # Edit the cron jobs
```

## Internship Keywords

The tool searches for positions matching these criteria:

### IT Keywords:
- Software Development
- Engineering
- Computer Science
- Programming
- Web/Mobile Development
- DevOps/Cloud
- Fullstack/Backend/Frontend
- And many more technical fields

### Internship Terms:
- Intern/Internship
- Alternance
- Trainee
- Stage

### Target Companies:
- Google, Microsoft, Amazon, Apple
- IBM, Oracle, SAP, Cisco
- Other major tech companies

## File Structure

- `it_internship.py` - Main script that handles everything
- `run_it_scraper.sh` - Convenient shell script for running the tool
- `output/it_internships.csv` - Filtered IT internship data

## Customization

You can adjust the search criteria in `it_internship.py` by modifying:
- `IT_KEYWORDS` - Keywords for IT positions
- `INTERNSHIP_KEYWORDS` - Keywords for internships/alternances
- `EU_COUNTRIES` - Target countries for the search
- `TECH_COMPANIES` - Companies to specifically target

Enjoy finding your perfect IT engineering internship or alternance!
