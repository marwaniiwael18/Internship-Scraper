import threading
import logging
import os

# Create necessary directories before importing keep_alive
os.makedirs("logs", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Now import after directory creation
from keep_alive import keep_alive, run_scraper

logging.info("Starting IT Internship Scraper Service")

# Start the web server to keep the Repl alive
keep_alive()
logging.info("Keep alive server started")

# Start the scraper in a separate thread
logging.info("Initializing scraper thread")
scraper_thread = threading.Thread(target=run_scraper)
scraper_thread.daemon = True  # Make the thread exit when the main thread exits
scraper_thread.start()
logging.info("Scraper thread started")

# Print startup message
print("IT Internship Scraper is now running!")
print("The web server is active to keep the repl alive.")
print("The scraper will run every 8 hours and send results to Telegram.")

try:
    # Keep the main thread alive
    scraper_thread.join()
except KeyboardInterrupt:
    logging.info("Service interrupted manually")
    print("Service stopped manually")
except Exception as e:
    logging.error(f"Error in main thread: {e}")
    print(f"An error occurred: {e}")