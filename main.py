import asyncio
import traceback
from playwright.async_api import async_playwright
from config import ApplicationConfig, Messages
from utils import ConsoleOutput, ProfileBuilder
from signup_bot import SignupBot

def display_startup_banner(profile):
    """Display initial configuration information"""
    sep = "=" * ApplicationConfig.SEPARATOR_LENGTH
    
    print(f"\n{sep}")
    print(f"AUTOMATED SIGNUP — authorized-partner.vercel.app")
    print(f"{sep}")
    print(f"  Email     : {profile['user_info']['email_user']}@{ApplicationConfig.EMAIL_DOMAIN}")
    print(f"  Phone     : +977 {profile['user_info']['phone']}")
    print(f"  Agency    : {profile['company_info']['name']}")
    print(f"  Password  : {profile['user_info']['credential']}")

async def execute_automation():
    """Main execution function"""
    ConsoleOutput.configure()
    
    # Generate registration profile
    profile = ProfileBuilder.build()
    
    # Display startup information
    display_startup_banner(profile)
    
    # Initialize and run bot
    async with async_playwright() as pw:
        bot = SignupBot(profile)
        await bot.setup_browser(pw)
        await bot.run_workflow()
    
    # Display completion message
    ConsoleOutput.final_footer()

def main():
    """Entry point"""
    try:
        asyncio.run(execute_automation())
    except KeyboardInterrupt:
        print("\n\nAutomation interrupted by user.")
    except Exception as error:
        print(f"\n!!! ERROR !!!\n{error}")
        traceback.print_exc()

if __name__ == "__main__":
    main()