import asyncio
import traceback
import sys
import time
from playwright.async_api import async_playwright
from config import ApplicationConfig, Messages
from utils import ConsoleOutput, ProfileBuilder
from signup_bot import SignupBot

def display_startup_banner(profile):
    sep = "=" * 64
    print(f"\n{sep}")
    print(f"AUTOMATED SIGNUP — authorized-partner.vercel.app")
    print(f"{sep}")
    print(f"  Email     : {profile['user_info']['email_user']}@{ApplicationConfig.EMAIL_DOMAIN}")
    print(f"  Phone     : +977 {profile['user_info']['phone']}")
    print(f"  Agency    : {profile['company_info']['name']}")
    print(f"  Password  : {profile['user_info']['credential']}")

async def execute_automation():
    ConsoleOutput.configure()
    profile = ProfileBuilder.build()
    display_startup_banner(profile)
    
    async with async_playwright() as pw:
        bot = SignupBot(profile)
        await bot.setup_browser(pw)
        await bot.run_workflow()
        ConsoleOutput.final_footer()

def main():
    try:
        asyncio.run(execute_automation())
        print("\nScript execution completed. Exiting in 5 seconds...")
        time.sleep(5)
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\nAutomation interrupted by user.")
        sys.exit(1)
    except Exception as error:
        print(f"\n!!! ERROR !!!\n{error}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
    main()