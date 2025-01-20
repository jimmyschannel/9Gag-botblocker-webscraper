# 9gag Bot Blocker Tool

This is a tool built using Selenium that automatically blocks users who frequently post on 9gag. It scrapes the "Fresh" feed on 9gag, identifies users with a high frequency of posts, and blocks them to reduce spam.

This tool is for educational purposes only. Use at your own risk. I am not responsible for any legal consequences resulting from using this tool.

Important: It only works with Chrome and with an adblocker active, otherwise it gets stuck in a loop.

## Features

- Scrapes posts from the "Fresh" feed on 9gag.
- Tracks creators and blocks users who appear in multiple posts.
- Automatically blocks users based on configurable criteria (e.g., 4+ posts).
- Uses Selenium WebDriver with a pre-configured browser profile.

## Requirements

- Python 3.x
- Selenium
- Chrome WebDriver
- `webdriver_manager` for automatic ChromeDriver installation.

## Installation & How to use

To use this tool, follow these steps:

1. Clone the repository 
2. Instal Selenium with pip: pip install -U selenium | pip install selenium webdriver-manager
3. Change the 'YOURUSERNAME' in the script to your username path.
4. Change the 'Profile 1' in the script to the right Google Chrome Profile. (Usually: "Default" or "Profile 1".
5. Be sure to be logged in into your 9Gag account, have an adblocker active and then Close Google Chrome.
6. Run the script
 
