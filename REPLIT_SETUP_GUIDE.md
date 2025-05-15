# Deploying Your IT Internship Scraper on Replit

These step-by-step instructions will help you deploy your IT internship scraper on Replit for free 24/7 hosting.

## Step 1: Create a Replit Account

1. Go to [Replit](https://replit.com/) and sign up for a free account
2. Verify your email address

## Step 2: Import Your GitHub Repository

1. Click the "+ Create" button in the top-right corner
2. Select "Import from GitHub"
3. In the "GitHub URL" field, enter: `https://github.com/marwaniiwael18/Internship-Scraper.git`
4. Click "Import from GitHub"
5. Wait for Replit to clone your repository

## Step 3: Configure Environment Variables

1. Once the repository is imported, click on the padlock icon (🔒) in the left sidebar
2. Add the following environment variables:
   - Key: `BOT_TOKEN`, Value: `8041545402:AAFvZBdheN74kl6_juAfPPJ-wVNCSi7Yq6k`
   - Key: `CHAT_ID`, Value: `-1002680765834`
   - Key: `MAX_ENTRIES`, Value: `20`
3. Click "Add new secret" for each variable
4. Make sure each secret has been added correctly

## Step 4: Launch Your Scraper

1. Click the "Run" button at the top of the Replit interface
2. Watch the console to verify that the scraper starts correctly
3. You should see messages like:
   - "Starting IT Internship Scraper Service"
   - "Web server started"
   - "Scraper thread started"

## Step 5: Configure UptimeRobot to Keep Your Repl Alive

1. Create a free account on [UptimeRobot](https://uptimerobot.com/)
2. Click "Add New Monitor"
3. Configure the monitor:
   - Monitor Type: HTTP(s)
   - Friendly Name: IT Internship Scraper
   - URL: Your Replit app URL (e.g., `https://internship-scraper-username.replit.app`)
   - Monitoring Interval: Every 5 minutes
4. Click "Create Monitor"

## Step 6: Verify Your Setup

1. Visit your Replit app URL to see the status dashboard
2. You should see:
   - Service status indicator
   - Last check time
   - Uptime counter
   - Next scheduled run time
   - Number of internships found

## Step 7: Check Your Telegram Channel

1. Open Telegram and navigate to your channel
2. You should start receiving internship listings within a few hours

## Troubleshooting

If you encounter issues:

1. **Application not running:**
   - Check the Replit console for error messages
   - Click "Stop" and then "Run" again

2. **No messages in Telegram:**
   - Verify your BOT_TOKEN and CHAT_ID are correct
   - Check the console logs for any errors related to sending messages

3. **Replit going to sleep:**
   - Confirm UptimeRobot is correctly monitoring your application
   - Check that the URL in UptimeRobot matches your Replit app URL

4. **Scraper not finding internships:**
   - Check the console logs for errors during scraping
   - Verify that the output directory is being created properly

For more assistance, refer to the REPLIT_DEPLOYMENT.md file in your repository.
