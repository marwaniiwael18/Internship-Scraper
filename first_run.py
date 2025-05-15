#!/usr/bin/env python3
"""
First Run Script for Replit Deployment
-------------------------------------
This script performs initial setup for the IT Internship Scraper on Replit.
It creates necessary directories and runs an initial scrape.
"""
import os
import subprocess
import sys
import time
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
        logging.FileHandler("logs/setup.log")
    ]
)

def check_environment():
    """Check if we're running on Replit."""
    return "REPLIT_DB_URL" in os.environ

def create_directories():
    """Create necessary directories."""
    logging.info("Creating necessary directories...")
    os.makedirs("output", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

def install_dependencies():
    """Install dependencies."""
    logging.info("Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

def run_initial_scrape():
    """Run an initial scrape to populate data."""
    logging.info("Running initial scrape (this may take a few minutes)...")
    try:
        subprocess.run([sys.executable, "it_internship.py", "--scrape", "--days=3"], 
                     check=True, timeout=300)
        logging.info("Initial scrape completed successfully!")
        return True
    except (subprocess.SubprocessError, subprocess.TimeoutExpired) as e:
        logging.error(f"Error during initial scrape: {e}")
        return False

def verify_telegram_config():
    """Verify Telegram configuration."""
    logging.info("Verifying Telegram configuration...")
    bot_token = os.environ.get("BOT_TOKEN", "")
    chat_id = os.environ.get("CHAT_ID", "")
    
    if not bot_token or not chat_id:
        logging.warning("Telegram configuration not found in environment variables.")
        logging.warning("Please set BOT_TOKEN and CHAT_ID in Replit Secrets.")
        return False
    
    logging.info("Telegram configuration found!")
    return True

def start_main_app():
    """Start the main application."""
    logging.info("Starting main application...")
    subprocess.run([sys.executable, "main.py"])

def main():
    """Main execution function."""
    print("=" * 60)
    print("IT INTERNSHIP SCRAPER - REPLIT FIRST RUN SETUP")
    print("=" * 60)
    
    create_directories()
    install_dependencies()
    
    if check_environment():
        logging.info("Running on Replit environment.")
        telegram_configured = verify_telegram_config()
        if not telegram_configured:
            logging.warning("Proceeding without verified Telegram configuration.")
    
    scrape_success = run_initial_scrape()
    if not scrape_success:
        logging.warning("Initial scrape had issues, but we'll continue setup.")
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETE! Starting main application...")
    print("=" * 60 + "\n")
    
    time.sleep(2)  # Small delay to let user read messages
    start_main_app()

if __name__ == "__main__":
    main()
