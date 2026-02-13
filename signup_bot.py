import random
from config import ApplicationConfig, FieldNames, Selectors, Messages, DataPools, Patterns
from utils import ConsoleOutput, DelayController, ElementFinder, FormInteractor, EmailReader, FileManager

class SignupBot:
    def __init__(self, profile):
        self.profile = profile
        self.browser = None
        self.context = None
        self.page = None
    
    async def setup_browser(self, playwright):
        self.browser = await playwright.chromium.launch(headless=False, slow_mo=ApplicationConfig.SLOW_MOTION_MS)
        self.context = await self.browser.new_context(viewport={"width": ApplicationConfig.BROWSER_WIDTH, "height": ApplicationConfig.BROWSER_HEIGHT})
        self.page = await self.context.new_page()
    
    async def teardown(self):
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
    
    async def phase_0_accept_terms(self):
        ConsoleOutput.section(0, Messages.HEADER_TERMS)
        
        ConsoleOutput.info(f"{Messages.INFO_NAVIGATING} {ApplicationConfig.TARGET_URL} …")
        await self.page.goto(ApplicationConfig.TARGET_URL, wait_until="networkidle", timeout=30000)
        await DelayController.natural_wait(self.page, 2000)
        
        links = self.page.locator("a[href]")
        link_count = await links.count()
        reg_link = None
        
        for i in range(link_count):
            link = links.nth(i)
            href = await link.get_attribute("href")
            if href and "register" in href:
                if await link.is_visible():
                    reg_link = link
                    break
        
        if reg_link is None:
            raise RuntimeError(Messages.ERROR_NO_REG_LINK)
        
        await reg_link.scroll_into_view_if_needed()
        await DelayController.natural_wait(self.page, 1000)
        await reg_link.click()
        ConsoleOutput.success(f"{Messages.SUCCESS_CLICKED} registration link")
        await DelayController.natural_wait(self.page, 3000)
        
        await self.page.locator(Selectors.CHECKBOX_BUTTON).click()
        ConsoleOutput.success(Messages.SUCCESS_AGREED)
        
        await self.page.locator(Selectors.CONTINUE_BUTTON).click()
        ConsoleOutput.success(Messages.SUCCESS_CONTINUE)
        await DelayController.natural_wait(self.page, 2000)
    
    async def phase_1_create_account(self):
        ConsoleOutput.section(1, Messages.HEADER_ACCOUNT)
        
        user = self.profile['user_info']
        
        await self.page.fill(f"input[name='{FieldNames.FIRST_NAME}']", user['given_name'])
        ConsoleOutput.success(f"{FieldNames.FIRST_NAME} = {user['given_name']}")
        
        await self.page.fill(f"input[name='{FieldNames.LAST_NAME}']", user['family_name'])
        ConsoleOutput.success(f"{FieldNames.LAST_NAME} = {user['family_name']}")
        
        email = f"{user['email_user']}@{ApplicationConfig.EMAIL_DOMAIN}"
        await self.page.fill(f"input[name='{FieldNames.EMAIL}']", email)
        ConsoleOutput.success(f"{FieldNames.EMAIL} = {email}")
        
        await self.page.fill(f"input[name='{FieldNames.PHONE_NUMBER}']", user['phone'])
        ConsoleOutput.success(f"{FieldNames.PHONE_NUMBER} = {user['phone']}")
        
        await self.page.fill(f"input[name='{FieldNames.PASSWORD}']", user['credential'])
        ConsoleOutput.success(f"{FieldNames.PASSWORD} = {user['credential']}")
        
        await self.page.fill(f"input[name='{FieldNames.CONFIRM_PASSWORD}']", user['credential'])
        ConsoleOutput.success(f"{FieldNames.CONFIRM_PASSWORD} = {user['credential']}")
        
        await self.page.locator(Selectors.SUBMIT_BUTTON).click()
        ConsoleOutput.success(Messages.SUCCESS_SUBMITTED)
        await DelayController.natural_wait(self.page, 3000)
        
        otp_field = self.page.locator(Selectors.OTP_INPUT)
        await otp_field.wait_for(state="visible", timeout=30000)
        ConsoleOutput.success(Messages.SUCCESS_OTP_APPEARED)
    
    async def phase_1b_verify_otp(self):
        ConsoleOutput.section("1b", Messages.HEADER_OTP)
        
        verified = False
        
        for attempt in range(1, ApplicationConfig.MAX_VERIFICATION_ATTEMPTS + 1):
            ConsoleOutput.info(f"OTP attempt {attempt}")
            ConsoleOutput.info(Messages.INFO_WAITING_EMAIL)
            await DelayController.natural_wait(self.page, 5000)
            
            code = await EmailReader.fetch_otp(self.browser, self.profile['user_info']['email_user'])
            
            otp_field = self.page.locator(Selectors.OTP_INPUT)
            await otp_field.first.wait_for(state="visible", timeout=10000)
            
            await otp_field.first.click()
            await DelayController.natural_wait(self.page, 300)
            
            for digit in code:
                await self.page.keyboard.press(digit)
                await DelayController.natural_wait(self.page, 150)
            
            ConsoleOutput.success(f"{Messages.SUCCESS_OTP_TYPED}: {code}")
            
            await self.page.locator(Selectors.SUBMIT_BUTTON).click()
            ConsoleOutput.success(Messages.SUCCESS_VERIFICATION_SUBMITTED)
            await DelayController.natural_wait(self.page, 4000)
            
            error_elem = self.page.locator(Selectors.ERROR_ALERT)
            if await error_elem.count() > 0:
                try:
                    error = await error_elem.first.inner_text(timeout=2000)
                    ConsoleOutput.warn(f"{Messages.WARN_ERROR_DETECTED} {error}")
                    
                    if "expired" in error.lower() or "invalid" in error.lower():
                        if attempt < ApplicationConfig.MAX_VERIFICATION_ATTEMPTS:
                            ConsoleOutput.info(Messages.WARN_OTP_INVALID)
                            resend = self.page.locator(Selectors.RESEND_BUTTON)
                            if await resend.count() > 0:
                                await resend.first.click()
                                ConsoleOutput.success(Messages.SUCCESS_RESEND_CLICKED)
                                await DelayController.natural_wait(self.page, 3000)
                            continue
                        else:
                            raise RuntimeError(Messages.ERROR_VERIFICATION_FAILED)
                except:
                    pass
            
            verified = True
            break
        
        if not verified:
            raise RuntimeError(Messages.ERROR_VERIFICATION_NO_SUCCESS)
        
        ConsoleOutput.info(f"{Messages.INFO_POST_VERIFICATION} {self.page.url}")
    
    async def phase_2_agency_details(self):
        ConsoleOutput.section(2, Messages.HEADER_AGENCY)
        
        await self.page.wait_for_selector(f"input[name='{FieldNames.AGENCY_NAME}']", state="visible", timeout=30000)
        
        company = self.profile['company_info']
        
        await self.page.fill(f"input[name='{FieldNames.AGENCY_NAME}']", company['name'])
        ConsoleOutput.success(f"{FieldNames.AGENCY_NAME} = {company['name']}")
        
        await self.page.fill(f"input[name='{FieldNames.ROLE_IN_AGENCY}']", company['position'])
        ConsoleOutput.success(f"{FieldNames.ROLE_IN_AGENCY} = {company['position']}")
        
        await self.page.fill(f"input[name='{FieldNames.AGENCY_EMAIL}']", company['email'])
        ConsoleOutput.success(f"{FieldNames.AGENCY_EMAIL} = {company['email']}")
        
        await self.page.fill(f"input[name='{FieldNames.AGENCY_WEBSITE}']", company['website'])
        ConsoleOutput.success(f"{FieldNames.AGENCY_WEBSITE} = {company['website']}")
        
        await self.page.fill(f"input[name='{FieldNames.AGENCY_ADDRESS}']", company['address'])
        ConsoleOutput.success(f"{FieldNames.AGENCY_ADDRESS} = {company['address']}")
        
        ConsoleOutput.info(Messages.INFO_DISCOVERING_REGIONS)
        region_combo = self.page.locator(Selectors.COMBOBOX_BUTTON)
        available = await ElementFinder.find_dialog_options(self.page, region_combo)
        
        if available:
            count = random.randint(1, min(3, len(available)))
            selected = random.sample(available, k=count)
        else:
            selected = company['regions']
        
        ConsoleOutput.info(f"{Messages.INFO_SELECTED_REGIONS} {selected}")
        await FormInteractor.select_dialog_items(self.page, region_combo, selected)
        
        await self.page.locator(Selectors.SUBMIT_BUTTON).click()
        ConsoleOutput.success(Messages.SUCCESS_AGENCY_SUBMITTED)
        await DelayController.natural_wait(self.page, 5000)
    
    async def phase_3_professional_experience(self):
        ConsoleOutput.section(3, Messages.HEADER_EXPERIENCE)
        
        ConsoleOutput.info(Messages.INFO_DISCOVERING_EXPERIENCE)
        exp_combo = self.page.locator(Selectors.COMBOBOX_BUTTON).first
        available = await ElementFinder.find_dropdown_options(self.page, exp_combo)
        
        background = self.profile['background']
        
        if available:
            selected_exp = random.choice(available)
        else:
            selected_exp = background['years']
        
        ConsoleOutput.info(f"{Messages.INFO_SELECTING} {selected_exp}")
        await exp_combo.click()
        await DelayController.natural_wait(self.page, 1000)
        
        exp_option = self.page.locator(f"[role='option']:has-text('{selected_exp}')")
        if await exp_option.count() > 0:
            await exp_option.first.click()
        else:
            await self.page.get_by_text(selected_exp, exact=False).first.click()
        
        ConsoleOutput.success(f"Years of Experience = {selected_exp}")
        await DelayController.natural_wait(self.page, 500)
        
        await self.page.fill(f"input[name='{FieldNames.STUDENTS_RECRUITED}']", background['students'])
        ConsoleOutput.success(f"{FieldNames.STUDENTS_RECRUITED} = {background['students']}")
        
        await self.page.fill(f"input[name='{FieldNames.FOCUS_AREA}']", background['specialty'])
        ConsoleOutput.success(f"{FieldNames.FOCUS_AREA} = {background['specialty']}")
        
        await self.page.fill(f"input[name='{FieldNames.SUCCESS_METRICS}']", background['success'])
        ConsoleOutput.success(f"{FieldNames.SUCCESS_METRICS} = {background['success']}")
        
        ConsoleOutput.info(Messages.INFO_DISCOVERING_SERVICES)
        available_services = await ElementFinder.find_checkbox_options(self.page)
        
        if available_services:
            count = random.randint(2, len(available_services))
            selected_services = random.sample(available_services, k=count)
        else:
            selected_services = background['services']
        
        ConsoleOutput.info(f"{Messages.INFO_SELECTED_SERVICES} {selected_services}")
        await FormInteractor.check_boxes(self.page, selected_services)
        
        await self.page.locator(Selectors.SUBMIT_BUTTON).click()
        ConsoleOutput.success(Messages.SUCCESS_EXPERIENCE_SUBMITTED)
        await DelayController.natural_wait(self.page, 5000)
    
    async def phase_4_verification(self):
        ConsoleOutput.section(4, Messages.HEADER_VERIFICATION)
        
        await self.page.wait_for_selector(f"input[name='{FieldNames.BUSINESS_REG_NUMBER}']", state="visible", timeout=15000)
        
        validation = self.profile['validation']
        
        await self.page.fill(f"input[name='{FieldNames.BUSINESS_REG_NUMBER}']", validation['reg_num'])
        ConsoleOutput.success(f"{FieldNames.BUSINESS_REG_NUMBER} = {validation['reg_num']}")
        
        ConsoleOutput.info(Messages.INFO_DISCOVERING_COUNTRIES)
        country_combo = self.page.locator(Selectors.COMBOBOX_BUTTON)
        available = await ElementFinder.find_dialog_options(self.page, country_combo)
        
        if available:
            count = random.randint(1, min(3, len(available)))
            selected = random.sample(available, k=count)
        else:
            selected = validation['countries']
        
        ConsoleOutput.info(f"{Messages.INFO_SELECTED_COUNTRIES} {selected}")
        await FormInteractor.select_dialog_items(self.page, country_combo, selected)
        
        ConsoleOutput.info(Messages.INFO_DISCOVERING_INSTITUTIONS)
        available_inst = await ElementFinder.find_checkbox_options(self.page)
        
        if available_inst:
            count = random.randint(1, len(available_inst))
            selected_inst = random.sample(available_inst, k=count)
        else:
            selected_inst = validation['institutions']
        
        ConsoleOutput.info(f"{Messages.INFO_SELECTED_INSTITUTIONS} {selected_inst}")
        await FormInteractor.check_boxes(self.page, selected_inst)
        
        await self.page.fill(f"input[name='{FieldNames.CERTIFICATION_DETAILS}']", validation['certs'])
        ConsoleOutput.success(f"{FieldNames.CERTIFICATION_DETAILS} = {validation['certs']}")
        
        ConsoleOutput.info(Messages.INFO_UPLOADING_DOCS)
        doc_path = FileManager.create_temp_document(self.profile)
        
        file_inputs = self.page.locator(Selectors.FILE_INPUT)
        input_count = await file_inputs.count()
        
        for i in range(input_count):
            await file_inputs.nth(i).set_input_files(doc_path)
            ConsoleOutput.success(f"    file input #{i + 1} ← _temp_business_doc.txt")
            await DelayController.natural_wait(self.page, 500)
        
        add_docs = self.page.locator(Selectors.ADD_DOCUMENTS_BUTTON)
        if await add_docs.count() > 0 and await add_docs.is_visible():
            await add_docs.click()
            ConsoleOutput.success(Messages.SUCCESS_DOCUMENTS_CLICKED)
            await DelayController.natural_wait(self.page, 1000)
        
        submit = self.page.locator(Selectors.FINAL_SUBMIT_BUTTON)
        if await submit.count() == 0:
            submit = self.page.locator(Selectors.SUBMIT_BUTTON).last
        
        await submit.click()
        ConsoleOutput.success(Messages.SUCCESS_FINAL_SUBMIT)
        await DelayController.natural_wait(self.page, 5000)
        
        final_url = self.page.url
        content = await self.page.locator(Selectors.BODY_ELEMENT).inner_text()
        
        ConsoleOutput.final_header()
        print(f"  {Messages.FINAL_URL} {final_url}")
        print(f"  {Messages.FINAL_CONTENT}")
        
        for line in content.strip().splitlines()[:10]:
            stripped = line.strip()
            if stripped:
                print(f"    │ {stripped}")
        
        FileManager.cleanup(doc_path)
    
    async def run_workflow(self):
        try:
            await self.phase_0_accept_terms()
            await self.phase_1_create_account()
            await self.phase_1b_verify_otp()
            await self.phase_2_agency_details()
            await self.phase_3_professional_experience()
            await self.phase_4_verification()
        finally:
            await self.teardown()