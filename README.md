# VRIT Signup Automation

Automates the signup process for an educational consultancy partner registration form.

## What it does

Fills out a multi-step registration form automatically. It handles account creation, email verification (using Mailinator for temporary OTP codes), agency details, professional experience, and document uploads. Basically saves you from doing the same form 100 times.

## Why I built this

Had to test the signup flow repeatedly and got tired of manually filling everything. So I automated it with Playwright.

## How it works

Pretty simple:

1. Opens the registration page in Chromium
2. Fills out the account form with random data
3. Grabs the OTP from Mailinator inbox
4. Completes the remaining steps (agency info, experience, documents)
5. Submits everything and shows the result

The script adds random delays between actions so it doesn't look robotic. Data like names, agencies, and addresses are picked randomly from lists in `config.py`.

## Requirements

- Python 3.7 or higher
- Playwright (browser automation)
- Chromium browser (installed via Playwright)
- Internet connection (for Mailinator email access)

## Setup

1. Install Python dependencies:

```bash
pip install -r Requirements.txt
```

2. Install Chromium browser:

```bash
playwright install chromium
```

That's it. No API keys or accounts needed.

## Running it

```bash
python main.py
```

The browser will open and you'll see it fill everything out automatically. Takes about 2-3 minutes depending on email delivery.

## Test Data

The script generates random data each run:

- Names: Picked from Nepali names list (Pushkar, Sachin, Niranjan, etc.)
- Emails: Uses Mailinator temporary addresses (autobot{timestamp}@mailinator.com)
- Phone numbers: Random 10-digit Nepal numbers starting with 9841
- Agencies: Randomly combined prefixes and suffixes (e.g., "Himalayan Educational Consultancy")
- Passwords: Auto-generated 14-character secure passwords

All data is throwaway - nothing gets reused. Check `config.py` to see the full data pools or add your own.

## Files

- `main.py` - starts everything
- `signup_bot.py` - does the actual form filling
- `utils.py` - helper stuff (password generation, OTP extraction, etc)
- `config.py` - all the settings and data pools

## Notes

Uses temporary emails from Mailinator. The OTP fetching retries up to 20 times if the email is slow. Sometimes it fails if the email doesn't arrive - just run it again.

You can tweak the delays and data in `config.py` if needed.
