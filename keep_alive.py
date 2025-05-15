from flask import Flask
from threading import Thread
import time
import datetime
import subprocess
import os
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/scraper.log")
    ]
)

app = Flask('')

@app.route('/')
def home():
    try:
        with open('status.html', 'r') as file:
            html_content = file.read()
        return html_content
    except Exception as e:
        logging.error(f"Error reading status page: {e}")
        return "IT Internship Scraper is alive and running! Last check: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
    logging.info("Web server started")

def run_scraper():
    # Create necessary directories
    os.makedirs("output", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Track when we last ran the scraper
    last_run_time = datetime.datetime.now() - datetime.timedelta(hours=9)
    
    while True:
        try:
            now = datetime.datetime.now()
            time_since_last_run = now - last_run_time
            
            # Run every 8 hours
            if time_since_last_run.total_seconds() >= 28800:  # 8 hours in seconds
                logging.info("Starting scheduled scraping run")
                
                # Run the scraper with 3-day filter
                logging.info("Running IT internship scraper...")
                subprocess.run(["python", "it_internship.py", "--scrape", "--days=3"], 
                              check=True)
                
                # Run the Telegram sender
                logging.info("Sending results to Telegram...")
                subprocess.run(["python", "send_to_telegram.py"], 
                              check=True)
                
                # Update the last run time
                last_run_time = now
                logging.info(f"Scraping completed successfully at {now.strftime('%Y-%m-%d %H:%M:%S')}")
                logging.info(f"Next run scheduled for: {(now + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Log status every hour
            elif now.minute < 5:  # First 5 minutes of the hour
                hours_until_next_run = 8 - (time_since_last_run.total_seconds() / 3600)
                logging.info(f"Bot is alive. Next run in approximately {hours_until_next_run:.1f} hours")
            
            # Sleep for 5 minutes before checking time again
            time.sleep(300)
            
        except Exception as e:
            logging.error(f"Error in run_scraper: {e}")
            # Sleep for a minute before retrying
            time.sleep(60)