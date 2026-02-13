"""
Utility functions and helper classes
"""

import sys
import random
import string
import time
import re
import os
from config import ApplicationConfig, DataPools, Messages, Patterns, Selectors

class ConsoleOutput:
    """Handles console output formatting"""
    
    @staticmethod
    def configure():
        """Enable immediate console output with UTF-8 encoding"""
        # Set UTF-8 encoding for Windows console to support Unicode characters
        if sys.platform == 'win32':
            sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
        else:
            sys.stdout.reconfigure(line_buffering=True)
    
    @staticmethod
    def section(step_id, title):
        """Print formatted section header"""
        sep = "=" * ApplicationConfig.SEPARATOR_LENGTH
        print(f"\n{sep}")
        print(f"  STEP {step_id}  --  {title}")
        print(f"{sep}")
    
    @staticmethod
    def success(message):
        """Print success message"""
        print(f"  [ OK ]  {message}")
    
    @staticmethod
    def info(message):
        """Print info message"""
        print(f"  [INFO]  {message}")
    
    @staticmethod
    def warn(message):
        """Print warning message"""
        print(f"  [WARN]  {message}")
    
    @staticmethod
    def final_header():
        """Print final success header"""
        sep = "═" * ApplicationConfig.SEPARATOR_LENGTH
        print(f"\n{sep}")
        print(f"#  {Messages.FINAL_SUCCESS}")
        print(f"{sep}")
    
    @staticmethod
    def final_footer():
        """Print final footer"""
        sep = "═" * ApplicationConfig.SEPARATOR_LENGTH
        print(f"\n{sep}")
        print(f"  {Messages.FINAL_DONE}")
        print(f"{sep}\n")

class PasswordGenerator:
    """Generates secure passwords"""
    
    @staticmethod
    def generate(length=14):
        """Create a random secure password with complexity requirements"""
        char_sets = {
            'upper': string.ascii_uppercase,
            'lower': string.ascii_lowercase,
            'digits': string.digits,
            'special': "!@#$%&*"
        }
        
        # Ensure at least one character from each set
        required = [
            random.choice(char_sets['upper']),
            random.choice(char_sets['lower']),
            random.choice(char_sets['digits']),
            random.choice(char_sets['special'])
        ]
        
        # Fill remaining length
        all_chars = ''.join(char_sets.values())
        remaining = [random.choice(all_chars) for _ in range(length - len(required))]
        
        # Combine and shuffle
        password_chars = required + remaining
        random.shuffle(password_chars)
        
        return ''.join(password_chars)

class ProfileBuilder:
    """Builds registration profiles with randomized data"""
    
    @staticmethod
    def build():
        """Generate complete registration profile"""
        ts = ApplicationConfig.TIMESTAMP
        
        return {
            'user_info': {
                'given_name': random.choice(DataPools.FIRST_NAMES),
                'family_name': random.choice(DataPools.LAST_NAMES),
                'email_user': f"autobot{ts}",
                'phone': f"9841{random.randint(100000, 999999)}",
                'credential': PasswordGenerator.generate()
            },
            'company_info': {
                'name': f"{random.choice(DataPools.ORGANIZATION_PREFIXES)} {random.choice(DataPools.ORGANIZATION_SUFFIXES)} {ts}",
                'position': random.choice(DataPools.POSITION_TITLES),
                'email': f"agency{ts}@{ApplicationConfig.EMAIL_DOMAIN}",
                'website': f"www.{random.choice(DataPools.DOMAIN_NAMES)}{random.randint(10,99)}.com",
                'address': f"{random.choice(DataPools.STREET_NAMES)}, {random.choice(DataPools.CITY_NAMES)}, Nepal",
                'regions': random.sample(DataPools.OPERATIONAL_REGIONS, k=random.randint(1, 3))
            },
            'background': {
                'years': random.choice(DataPools.EXPERIENCE_YEARS),
                'students': str(random.randint(20, 500)),
                'specialty': random.choice(DataPools.SPECIALIZATION_AREAS),
                'success': str(random.randint(70, 99)),
                'services': random.sample(DataPools.SERVICE_TYPES, k=random.randint(2, len(DataPools.SERVICE_TYPES)))
            },
            'validation': {
                'reg_num': f"BRN-{ts}",
                'countries': random.sample(DataPools.DESTINATION_COUNTRIES, k=random.randint(1, 3)),
                'institutions': DataPools.INSTITUTION_CATEGORIES,
                'certs': ", ".join(random.sample(DataPools.CERTIFICATIONS, k=random.randint(2, 4)))
            }
        }

class DelayController:
    """Manages timing and delays"""
    
    @staticmethod
    async def natural_wait(page, base_ms=None):
        """Apply human-like delay with variance"""
        if base_ms is None:
            base_ms = random.randint(
                ApplicationConfig.MIN_DELAY_MS, 
                ApplicationConfig.MAX_DELAY_MS
            )
        
        variance = random.randint(
            -ApplicationConfig.DELAY_VARIANCE // 2, 
            ApplicationConfig.DELAY_VARIANCE
        )
        
        final_delay = max(100, base_ms + variance)
        await page.wait_for_timeout(final_delay)

class OTPExtractor:
    """Extracts OTP codes from email"""
    
    @staticmethod
    def find_code(text):
        """Extract 6-digit OTP from text"""
        match = re.search(Patterns.OTP_PATTERN, text)
        return match.group(1) if match else None
    
    @staticmethod
    def has_keywords(text):
        """Check if text contains OTP-related keywords"""
        text_lower = text.lower()
        return any(kw in text_lower for kw in Patterns.EMAIL_KEYWORDS)

class FileManager:
    """Manages temporary file operations"""
    
    @staticmethod
    def create_temp_document(profile):
        """Create temporary business document"""
        doc_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "_temp_business_doc.txt"
        )
        
        with open(doc_path, "w") as f:
            f.write(
                f"Business Registration Document\n"
                f"Agency: {profile['company_info']['name']}\n"
                f"Registration No: {profile['validation']['reg_num']}\n"
                f"Date: {time.strftime('%Y-%m-%d')}\n"
            )
        
        return doc_path
    
    @staticmethod
    def cleanup(file_path):
        """Remove temporary file"""
        try:
            os.remove(file_path)
        except OSError:
            pass

class ElementFinder:
    """Discovers form elements dynamically"""
    
    @staticmethod
    async def find_dialog_options(page, trigger):
        """Extract options from modal dialog"""
        await trigger.click()
        await DelayController.natural_wait(page, 1000)
        
        dialog = page.locator(Selectors.ROLE_DIALOG)
        await dialog.wait_for(state="visible", timeout=5000)
        
        options = []
        spans = dialog.locator("div[role='option'] span, label span, [data-value] span, span")
        count = await spans.count()
        
        for i in range(count):
            text = (await spans.nth(i).inner_text()).strip()
            if text and text not in options and len(text) > 1:
                options.append(text)
        
        await page.keyboard.press("Escape")
        await DelayController.natural_wait(page, 500)
        
        return options
    
    @staticmethod
    async def find_dropdown_options(page, trigger):
        """Extract options from dropdown"""
        await trigger.click()
        await DelayController.natural_wait(page, 1000)
        
        options = []
        items = page.locator(Selectors.ROLE_OPTION)
        count = await items.count()
        
        for i in range(count):
            text = (await items.nth(i).inner_text()).strip()
            if text and text not in options:
                options.append(text)
        
        await page.keyboard.press("Escape")
        await DelayController.natural_wait(page, 500)
        
        return options
    
    @staticmethod
    async def find_checkbox_options(page):
        """Extract checkbox labels"""
        options = []
        labels = page.locator(Selectors.LABEL_ELEMENT)
        count = await labels.count()
        
        for i in range(count):
            parent = labels.nth(i).locator("..")
            checkbox = parent.locator(Selectors.CHECKBOX_BUTTON)
            
            if await checkbox.count() > 0:
                text = (await labels.nth(i).inner_text()).strip()
                if text:
                    options.append(text)
        
        return options

class FormInteractor:
    """Interacts with form elements"""
    
    @staticmethod
    async def select_dialog_items(page, trigger, selections):
        """Select items from modal dialog"""
        await trigger.click()
        await DelayController.natural_wait(page, 1000)
        
        dialog = page.locator(Selectors.ROLE_DIALOG)
        await dialog.wait_for(state="visible", timeout=5000)
        
        for item in selections:
            elem = dialog.locator(f"span:text-is('{item}')")
            if await elem.count() == 0:
                elem = dialog.get_by_text(item, exact=False)
            
            if await elem.count() > 0:
                await elem.first.click()
                ConsoleOutput.success(f"    [x] {item}")
                await DelayController.natural_wait(page, 300)
            else:
                ConsoleOutput.warn(Messages.WARN_OPTION_NOT_FOUND.format(text=item))
        
        await page.keyboard.press("Escape")
        await DelayController.natural_wait(page, 500)
    
    @staticmethod
    async def check_boxes(page, selections):
        """Check checkbox elements"""
        for item in selections:
            label = page.locator(f"label:has-text('{item}')").first
            
            if await label.count() == 0:
                ConsoleOutput.warn(Messages.WARN_CHECKBOX_NOT_FOUND.format(text=item))
                continue
            
            parent = label.locator("..")
            checkbox = parent.locator(Selectors.CHECKBOX_BUTTON)
            
            if await checkbox.count() > 0:
                await checkbox.click()
            else:
                await label.click()
            
            ConsoleOutput.success(f"    [x] {item}")
            await DelayController.natural_wait(page, 300)

class EmailReader:
    """Reads emails from Mailinator"""
    
    @staticmethod
    async def fetch_otp(browser, username):
        """Retrieve OTP from email inbox"""
        inbox_url = f"{ApplicationConfig.MAILINATOR_INBOX_URL}{username}"
        context = await browser.new_context()
        page = await context.new_page()
        code = None
        
        for attempt in range(1, ApplicationConfig.MAX_OTP_RETRIES + 1):
            try:
                await page.goto(inbox_url, wait_until="networkidle", timeout=20000)
                await DelayController.natural_wait(page, 2000)
                
                rows = page.locator(Selectors.TABLE_ROWS)
                row_count = await rows.count()
                
                if row_count < 2:
                    ConsoleOutput.info(
                        f"Attempt {attempt}/{ApplicationConfig.MAX_OTP_RETRIES}: "
                        f"inbox empty ({row_count} rows) — retrying in "
                        f"{ApplicationConfig.OTP_RETRY_INTERVAL}s …"
                    )
                    await DelayController.natural_wait(page, ApplicationConfig.OTP_RETRY_INTERVAL * 1000)
                    continue
                
                target_row = None
                for idx in range(1, row_count):
                    row_text = await rows.nth(idx).inner_text()
                    ConsoleOutput.info(f"  Row {idx}: {row_text[:100]}")
                    
                    if OTPExtractor.has_keywords(row_text):
                        target_row = rows.nth(idx)
                        break
                
                if target_row is None:
                    target_row = rows.nth(1)
                
                ConsoleOutput.info(Messages.INFO_OPENING_EMAIL)
                await target_row.click()
                await DelayController.natural_wait(page, 5000)
                
                email_body = ""
                try:
                    email_body = await (
                        page.frame_locator(Selectors.EMAIL_IFRAME)
                            .locator(Selectors.BODY_ELEMENT)
                            .inner_text(timeout=10000)
                    )
                    ConsoleOutput.info(f"  iframe body (first 200): {email_body[:200]}")
                except Exception as e:
                    ConsoleOutput.warn(f"{Messages.WARN_NO_IFRAME} {e}")
                
                if not email_body:
                    for frame in page.frames:
                        try:
                            text = await frame.locator(Selectors.BODY_ELEMENT).inner_text(timeout=3000)
                            if OTPExtractor.has_keywords(text):
                                email_body = text
                                break
                        except:
                            continue
                
                if email_body:
                    code = OTPExtractor.find_code(email_body)
                    if code:
                        ConsoleOutput.success(f"OTP retrieved: {code}")
                        break
                    else:
                        ConsoleOutput.warn(f"Attempt {attempt}: {Messages.WARN_NO_OTP}")
                else:
                    ConsoleOutput.warn(f"Attempt {attempt}: {Messages.WARN_EMPTY_BODY}")
            
            except Exception as e:
                ConsoleOutput.info(f"Attempt {attempt}: {str(e)[:100]}")
            
            await DelayController.natural_wait(page, ApplicationConfig.OTP_RETRY_INTERVAL * 1000)
        
        await context.close()
        
        if code is None:
            raise RuntimeError(Messages.ERROR_NO_OTP)
        
        return code