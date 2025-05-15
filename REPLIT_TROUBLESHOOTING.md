# Replit Troubleshooting Guide

This document provides solutions to common issues that may arise when running the IT Internship Scraper on Replit.

## Common Issues and Solutions

### 1. Logs Directory Error

**Problem**: Error related to missing logs directory.

**Solution**: 
- The application is designed to automatically create the logs directory on startup.
- If you still encounter this error, manually create the logs directory:
  1. In the Replit file explorer, right-click on the main project folder
  2. Select "Add Folder"
  3. Name it "logs"

### 2. Environment Variables Not Working

**Problem**: The scraper can't find BOT_TOKEN or CHAT_ID.

**Solution**:
- Verify that you've added the secrets correctly in Replit:
  1. Click on the padlock icon (🔒) in the sidebar
  2. Check that you have both `BOT_TOKEN` and `CHAT_ID` added
  3. Make sure there are no leading or trailing spaces in the values
  4. If needed, regenerate your bot token in BotFather and create a new value

### 3. Application Stops Running

**Problem**: The application stops running after some time.

**Solution**:
- Make sure UptimeRobot is configured correctly:
  1. Verify that the URL points to your Replit project (should be https://your-project-name.your-username.repl.co)
  2. Check that the monitoring interval is set to 5 minutes
  3. Confirm that UptimeRobot is showing the monitor as "UP"
- Alternatively, upgrade to Replit Hacker Plan for more reliable hosting

### 4. Scraper Not Finding Any Jobs

**Problem**: The scraper runs but doesn't find any jobs.

**Solution**:
- Check the logs for any API errors by viewing logs/scraper.log
- LinkedIn might be blocking the scraper. Try:
  1. Running the scraper less frequently (edit the interval in keep_alive.py)
  2. Updating the jobpilot package: run `pip install -U jobpilot` in the Replit Shell

### 5. Telegram Messages Not Being Sent

**Problem**: The scraper finds jobs but no messages are sent to Telegram.

**Solution**:
- Verify your bot permissions:
  1. Make sure your bot is added to your target channel/group
  2. Ensure the bot has admin privileges in the channel/group
  3. Test the bot with a simple message using the Telegram API

### 6. Package Installation Errors

**Problem**: Dependencies fail to install properly.

**Solution**:
- Run the following commands in the Replit Shell:
  ```bash
  pip install --upgrade pip
  pip install -r requirements.txt
  ```
- If jobpilot specifically is failing, try:
  ```bash
  pip install jobpilot --no-deps
  pip install requests beautifulsoup4 selenium
  ```

### 7. Memory or CPU Limit Errors

**Problem**: Replit shows resource limit errors.

**Solution**: 
- Optimize the scraper by reducing the number of jobs it processes at once
- Edit the MAX_ENTRIES variable in send_to_telegram.py
- Consider upgrading to a paid Replit plan for more resources

## Getting Help

If you encounter issues not covered in this guide:

1. Check the logs for specific error messages
2. Search the error message on GitHub Issues or Stack Overflow
3. Create a GitHub Issue in the project repository with:
   - The exact error message
   - Steps to reproduce
   - Any relevant log output
