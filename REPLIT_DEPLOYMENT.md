# Deploying to Replit

This guide will help you deploy and run your IT Internship Scraper on Replit, which will keep it running 24/7 for free.

## Step 1: Create a Replit Account

1. Go to [Replit](https://replit.com/) and sign up for a free account
2. Click "Create Repl" to create a new project
3. Select "Import from GitHub"
4. Enter your GitHub repository URL: `https://github.com/marwaniiwael18/Internship-Scraper.git`
5. Click "Import from GitHub"

## Step 2: Configure Environment Variables

1. In your Repl, click on the padlock icon (🔒) in the sidebar to open the Secrets panel
2. Add the following secrets:
   - Key: `BOT_TOKEN`, Value: `8041545402:AAFvZBdheN74kl6_juAfPPJ-wVNCSi7Yq6k`
   - Key: `CHAT_ID`, Value: `-1002680765834`

## Step 3: Run the Application

1. Click the "Run" button at the top of the Replit interface
2. The application will start and display its status in the console
3. You should see a web server starting and the status page becoming available

## Step 4: Keep the Repl Running 24/7 with UptimeRobot

1. Go to [UptimeRobot](https://uptimerobot.com/) and create a free account
2. Click "Add New Monitor"
3. Select "HTTP(s)" as the monitor type
4. Enter a friendly name like "IT Internship Scraper"
5. For the URL, enter your Replit app URL (will look like `https://internship-scraper.yourusername.repl.co`)
6. Set the monitoring interval to 5 minutes (300 seconds)
7. Click "Create Monitor"

With UptimeRobot configured, your Replit scraper will stay alive 24/7 and continue checking for new internships every 8 hours without going to sleep.

## Checking Your Scraper's Status

1. Visit your Replit app URL to see the live status dashboard
2. The dashboard will show:
   - Current scraper status
   - Time until next run
   - Number of internships found
   - Service uptime
   - Total number of scraping runs

## Troubleshooting

If you encounter any issues:

1. Check the Replit console for error messages
2. Make sure your Telegram BOT_TOKEN and CHAT_ID are correctly set in the Secrets panel
3. Verify that UptimeRobot is successfully connecting to your application

For persistent issues, you can restart your Repl by clicking the "Stop" button and then "Run" again.
5. For the URL, use the URL of your Repl. It will look something like:
   `https://internship-scraper.yourusername.repl.co`
   (You can find this URL in the Replit interface after running your application)
6. Set the monitoring interval to 5 minutes
7. Click "Create Monitor"

## Understanding How It Works

1. **Main Application Logic**:
   - The `main.py` file starts both a web server and the scraper thread
   - The web server keeps the Repl alive by responding to HTTP requests
   - The scraper thread runs every 8 hours to check for new internships

2. **Keeping It Alive**:
   - Replit normally puts applications to sleep after inactivity
   - UptimeRobot pings your application every 5 minutes, preventing it from sleeping
   - This creates a free 24/7 hosting solution

3. **Monitoring**:
   - You can view logs in the Replit console
   - The status page shows if the application is running
   - UptimeRobot will alert you if your application goes down

## Customization

- To change how often the scraper runs, modify the interval in `keep_alive.py`
- To change what internships are scraped, modify the filters in `it_internship.py`
- To modify the Telegram message format, edit `send_to_telegram.py`

Enjoy your automated IT internship scraper running 24/7 on Replit!
