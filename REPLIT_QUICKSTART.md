# Deploying IT Internship Scraper on Replit - Step by Step Guide

This guide will walk you through deploying your IT internship scraper on Replit for 24/7 operation.

## Prerequisites

- A Telegram bot token (get one from [@BotFather](https://t.me/botfather))
- A Telegram channel or group ID where notifications will be sent
- A free Replit account

## Deployment Steps

### 1. Fork the GitHub Repository (Optional)

If you want to make your own version of the project:
1. Fork the repository on GitHub
2. Make any desired customizations (filters, keywords, etc.)
3. Commit your changes

### 2. Create a New Replit Project

1. Go to [Replit](https://replit.com) and sign in
2. Click the **+ Create** button
3. Choose **Import from GitHub**
4. Enter the repository URL (either the original or your fork)
5. Click **Import from GitHub**

### 3. Configure Environment Variables

1. In your Replit project, click on the **Secrets** (lock icon) in the left sidebar
2. Add the following secrets:
   - Key: `BOT_TOKEN`, Value: Your Telegram bot token
   - Key: `CHAT_ID`, Value: Your Telegram channel/group ID

### 4. Run the Application

1. Click the **Run** button at the top of the Replit interface
2. The start script will:
   - Create necessary directories
   - Run the first-time setup
   - Start the main application

3. You should see output showing:
   - The web server starting
   - The scraper initializing

### 5. View the Status Dashboard

Once the application is running:
1. Click on the **Web** tab in the Replit interface (or the small browser icon)
2. You should see the scraper status dashboard showing:
   - Current uptime
   - Next scheduled run time
   - Number of jobs found
   - Current status

### 6. Keep It Running 24/7 with UptimeRobot

To prevent Replit from sleeping:
1. Go to [UptimeRobot](https://uptimerobot.com/) and create a free account
2. Click **Add New Monitor**
3. Set the monitor type to **HTTP(S)**
4. Enter a friendly name like "IT Internship Scraper"
5. In the URL field, enter your Replit project URL (copy from the Web tab)
6. Set the monitoring interval to **5 minutes**
7. Click **Create Monitor**

## Customizing the Scraper

You can modify these files to customize the scraper behavior:
- `it_internship.py` - Main scraper logic and filtering criteria
- `keep_alive.py` - Schedule timing and server settings
- `send_to_telegram.py` - Message formatting and delivery

## Troubleshooting

If you encounter any issues, refer to the `REPLIT_TROUBLESHOOTING.md` file for solutions to common problems.

## Next Steps

- Consider setting up a backup notification method (email, Discord, etc.)
- Customize the filters to match your specific job interests
- Consider upgrading to Replit's paid plan for more reliable hosting
