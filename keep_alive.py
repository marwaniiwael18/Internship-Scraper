from flask import Flask
from threading import Thread
import time
import datetime
import subprocess
import os
import logging

# Create necessary directories before setting up logging
os.makedirs("logs", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/scraper.log")
    ]
)

# Global variables for tracking status
start_time = time.time()
next_run_seconds = 28800  # 8 hours in seconds
last_run_time = datetime.datetime.now() - datetime.timedelta(hours=9) 
run_count = 0
scraper_status = "Initializing"

app = Flask('')

@app.route('/')
def home():
    try:
        with open('status.html', 'r') as file:
            html_template = file.read()
            
        # Get stats for dynamic insertion
        now = datetime.datetime.now()
        uptime = time.time() - start_time
        days, remainder = divmod(uptime, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # Get job counts if available
        job_count = 0
        try:
            if os.path.exists('output/it_internships.csv'):
                with open('output/it_internships.csv', 'r') as f:
                    job_count = sum(1 for _ in f) - 1  # Subtract header
        except:
            pass
            
        # Format uptime string
        uptime_str = f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"
        
        # Replace placeholders in the HTML
        html_content = html_template.replace('{{CURRENT_TIME}}', now.strftime("%Y-%m-%d %H:%M:%S"))
        html_content = html_content.replace('{{UPTIME}}', uptime_str)
        html_content = html_content.replace('{{NEXT_RUN}}', (now + datetime.timedelta(seconds=next_run_seconds)).strftime("%Y-%m-%d %H:%M:%S"))
        html_content = html_content.replace('{{JOB_COUNT}}', str(job_count))
        html_content = html_content.replace('{{RUN_COUNT}}', str(run_count))
        html_content = html_content.replace('{{STATUS}}', "Running")
        
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
    # Directories are already created at module initialization
    global last_run_time, run_count, scraper_status
    
    while True:
        try:
            now = datetime.datetime.now()
            time_since_last_run = now - last_run_time
            
            # Run every 8 hours
            if time_since_last_run.total_seconds() >= 28800:  # 8 hours in seconds
                scraper_status = "Running scraper..."
                logging.info("Starting scheduled scraping run")
                
                # Run the scraper with 3-day filter
                logging.info("Running IT internship scraper...")
                subprocess.run(["python", "it_internship.py", "--scrape", "--days=3"], 
                              check=True)
                
                # Run the Telegram sender
                logging.info("Sending results to Telegram...")
                subprocess.run(["python", "send_to_telegram.py"], 
                              check=True)
                
                # Update status
                run_count += 1
                last_run_time = now
                scraper_status = "Idle"
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