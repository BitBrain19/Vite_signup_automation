import sys
import random
import string
import time
import re
import os
from config import ApplicationConfig, DataPools, Messages, Patterns, Selectors

class ConsoleOutput:
    @staticmethod
    def configure():
        if sys.platform == 'win32':
            sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
        else:
            sys.stdout.reconfigure(line_buffering=True)
    
    @staticmethod
    def section(step_id, title):
        sep = "=" * ApplicationConfig.SEPARATOR_LENGTH
        print(f"\n{sep}")
        print(f"  STEP {step_id}  --  {title}")
        print(f"{sep}")
    
    @staticmethod
    def success(message):
        print(f"  [ OK ]  {message}")
    
    @staticmethod
    def info(message):
        print(f"  [INFO]  {message}")
    
    @staticmethod
    def warn(message):
        print(f"  [WARN]  {message}")
    
    @staticmethod
    def final_header():
        sep = "═" * ApplicationConfig.SEPARATOR_LENGTH
        print(f"\n{sep}")
        print(f"#  {Messages.FINAL_SUCCESS}")
        print(f"{sep}")
    
    @staticmethod
    def final_footer():
        sep = "═" * ApplicationConfig.SEPARATOR_LENGTH
        print(f"\n{sep}")
        print(f"  {Messages.FINAL_DONE}")
        print(f"{sep}\n")

def generate_password(length=14):
    chars_upper = string.ascii_uppercase
    chars_lower = string.ascii_lowercase
    chars_digits = string.digits
    chars_special = "!@#$%&*"
    
    password = [
        random.choice(chars_upper),
        random.choice(chars_lower),
        random.choice(chars_digits),
        random.choice(chars_special)
    ]
    
    all_chars = chars_upper + chars_lower + chars_digits + chars_special
    for i in range(length - 4):
        password.append(random.choice(all_chars))
    
    random.shuffle(password)
    return ''.join(password)

class ProfileBuilder:
    @staticmethod
    def build():
        ts = ApplicationConfig.TIMESTAMP
        
        return {
            'user_info': {
                'given_name': random.choice(DataPools.FIRST_NAMES),
                'family_name': random.choice(DataPools.LAST_NAMES),
                'email_user': f"autobot{ts}",
                'phone': f"9841{random.randint(100000, 999999)}",
                'credential': generate_password()
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
    @staticmethod
    async def natural_wait(page, base_ms=None):
        if base_ms is None:
            base_ms = random.randint(ApplicationConfig.MIN_DELAY_MS, ApplicationConfig.MAX_DELAY_MS)
        
        variance = random.randint(-200, ApplicationConfig.DELAY_VARIANCE)
        final_delay = max(100, base_ms + variance)
        await page.wait_for_timeout(final_delay)

class OTPExtractor:
    @staticmethod
    def find_code(text):
        match = re.search(Patterns.OTP_PATTERN, text)
        return match.group(1) if match else None
    
    @staticmethod
    def has_keywords(text):
        text_lower = text.lower()
        return any(kw in text_lower for kw in Patterns.EMAIL_KEYWORDS)

class FileManager:
    @staticmethod
    def create_temp_document(profile):
        doc_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_temp_business_doc.txt")
        
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
        try:
            os.remove(file_path)
        except OSError:
            pass

class ElementFinder:
    @staticmethod
    async def find_dialog_options(page, trigger):
        await trigger.click()
        await DelayController.natural_wait(page, 1000)
        
        dialog = page.locator(Selectors.ROLE_DIALOG)
        await dialog.wait_for(state="visible", timeout=5000)
        
        options = []
        spans = dialog.locator("span")
        count = await spans.count()
        
        for i in range(count):
            text = (await spans.nth(i).inner_text()).strip()
            if text and text not in options:
                options.append(text)
        
        await page.keyboard.press("Escape")
        await DelayController.natural_wait(page, 500)
        
        return options
    
    @staticmethod
    async def find_dropdown_options(page, trigger):
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
    @staticmethod
    async def select_dialog_items(page, trigger, selections):
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
    @staticmethod
    async def fetch_otp(browser, username):
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
                    ConsoleOutput.info(f"Attempt {attempt}: inbox empty, retrying in {ApplicationConfig.OTP_RETRY_INTERVAL}s")
                    await DelayController.natural_wait(page, ApplicationConfig.OTP_RETRY_INTERVAL * 1000)
                    continue
                
                target_row = None
                for idx in range(1, row_count):
                    row_text = await rows.nth(idx).inner_text()
                    
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
                    email_body = await (page.frame_locator(Selectors.EMAIL_IFRAME).locator(Selectors.BODY_ELEMENT).inner_text(timeout=10000))
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