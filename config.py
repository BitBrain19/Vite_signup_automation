import time
import random

class ApplicationConfig:
    TARGET_URL = "https://authorized-partner.vercel.app"
    TIMESTAMP = int(time.time())
    MIN_DELAY_MS = 800
    MAX_DELAY_MS = 2400
    DELAY_VARIANCE = 400
    BROWSER_WIDTH = 1280
    BROWSER_HEIGHT = 900
    SLOW_MOTION_MS = 200
    MAX_OTP_RETRIES = 20
    OTP_RETRY_INTERVAL = 3
    MAX_VERIFICATION_ATTEMPTS = 3
    EMAIL_DOMAIN = "mailinator.com"
    MAILINATOR_INBOX_URL = "https://www.mailinator.com/v4/public/inboxes.jsp?to="
    SEPARATOR_LENGTH = 64

class DataPools:
    FIRST_NAMES = ["Pushkar", "Sachin", "Niranjan", "Raj", "Nabin"]
    LAST_NAMES = ["Jha", "Bhatta", "Chaudhary", "Ghimire"]
    
    ORGANIZATION_PREFIXES = ["Himalayan", "Everest", "Kathmandu", "Nepal", "Bright"]
    ORGANIZATION_SUFFIXES = [
        "Education Foundation", "International Education", "Educational Consultancy",
        "Study Center", "Abroad Studies"
    ]
    
    POSITION_TITLES = [
        "Director", "Managing Director", "Senior Counselor", "Education Manager", "CEO"
    ]
    
    DOMAIN_NAMES = ["nepalstudy", "himalayanedu", "ktmedc", "brightfuture"]
    STREET_NAMES = ["Putalisadak", "New Baneshwor", "Dillibazar", "Kamaladi"]
    CITY_NAMES = ["Kathmandu", "Lalitpur", "Bhaktapur", "Pokhara"]
    OPERATIONAL_REGIONS = ["Australia", "Europe", "North America", "Asia"]
    EXPERIENCE_YEARS = ["1 Year", "2 Years", "3 Years", "5 Years"]
    
    SPECIALIZATION_AREAS = [
        "Student Visa Services and Documentation",
        "University Placements and Admissions",
        "Standardized Test Preparation (IELTS/PTE)",
        "Scholarship Assistance and Financial Guidance"
    ]
    
    CERTIFICATIONS = [
        "QEAC Certified Agent",
        "ICEF Agency Status",
        "Education New Zealand Trained Agent",
        "British Council Certified Agent"
    ]
    
    DESTINATION_COUNTRIES = [
        "Australia", "Canada", "United Kingdom", "United States", "New Zealand"
    ]
    
    SERVICE_TYPES = ["Career Counseling", "Admission Applications", "Visa Processing", "Test Preparation"]
    INSTITUTION_CATEGORIES = ["Universities", "Colleges"]

class FieldNames:
    FIRST_NAME = "firstName"
    LAST_NAME = "lastName"
    EMAIL = "email"
    PHONE_NUMBER = "phoneNumber"
    PASSWORD = "password"
    CONFIRM_PASSWORD = "confirmPassword"
    AGENCY_NAME = "agency_name"
    ROLE_IN_AGENCY = "role_in_agency"
    AGENCY_EMAIL = "agency_email"
    AGENCY_WEBSITE = "agency_website"
    AGENCY_ADDRESS = "agency_address"
    STUDENTS_RECRUITED = "number_of_students_recruited_annually"
    FOCUS_AREA = "focus_area"
    SUCCESS_METRICS = "success_metrics"
    BUSINESS_REG_NUMBER = "business_registration_number"
    CERTIFICATION_DETAILS = "certification_details"

class Selectors:
    CHECKBOX_BUTTON = "button[role='checkbox']"
    COMBOBOX_BUTTON = "button[role='combobox']"
    SUBMIT_BUTTON = "button[type='submit']"
    ROLE_DIALOG = "[role='dialog']"
    ROLE_OPTION = "[role='option']"
    FILE_INPUT = "input[type='file']"
    CONTINUE_BUTTON = "button:has-text('Continue')"
    OTP_INPUT = "input[inputmode='numeric']"
    ADD_DOCUMENTS_BUTTON = "button:has-text('Add Documents')"
    FINAL_SUBMIT_BUTTON = "button[type='submit']:has-text('Submit')"
    ERROR_ALERT = "[role='alert'], .text-red, .text-destructive, .error"
    RESEND_BUTTON = "button:has-text('Resend'), button:has-text('resend'), a:has-text('Resend'), a:has-text('resend')"
    EMAIL_IFRAME = "#html_msg_body"
    BODY_ELEMENT = "body"
    TABLE_ROWS = "table tbody tr"
    LABEL_ELEMENT = "label"

class Messages:
    HEADER_TERMS = "TERMS & CONDITIONS"
    HEADER_ACCOUNT = "ACCOUNT SETUP"
    HEADER_OTP = "OTP VERIFICATION  (via Mailinator)"
    HEADER_AGENCY = "AGENCY DETAILS"
    HEADER_EXPERIENCE = "PROFESSIONAL EXPERIENCE"
    HEADER_VERIFICATION = "VERIFICATION & PREFERENCES"
    SUCCESS_CLICKED = "Clicked"
    SUCCESS_AGREED = "Agreed to Terms & Conditions"
    SUCCESS_CONTINUE = "Clicked Continue"
    SUCCESS_SUBMITTED = "Account form submitted — waiting for OTP screen …"
    SUCCESS_OTP_APPEARED = "OTP input field appeared"
    SUCCESS_OTP_TYPED = "Typed OTP"
    SUCCESS_VERIFICATION_SUBMITTED = "Verification submitted"
    SUCCESS_AGENCY_SUBMITTED = "Agency details submitted"
    SUCCESS_EXPERIENCE_SUBMITTED = "Professional experience submitted"
    SUCCESS_RESEND_CLICKED = "Clicked Resend OTP"
    SUCCESS_DOCUMENTS_CLICKED = "Clicked 'Add Documents'"
    SUCCESS_FINAL_SUBMIT = "FINAL SUBMIT clicked — Signup complete!"
    INFO_NAVIGATING = "Navigating to"
    INFO_SCANNING_LINKS = "Scanning page for visible registration links …"
    INFO_CLICKING = "Clicking:"
    INFO_WAITING_EMAIL = "Waiting 5 s for email delivery …"
    INFO_DISCOVERING_REGIONS = "Discovering available Regions of Operation …"
    INFO_DISCOVERING_EXPERIENCE = "Discovering Years of Experience options …"
    INFO_DISCOVERING_SERVICES = "Discovering available services …"
    INFO_DISCOVERING_COUNTRIES = "Discovering available Preferred Countries …"
    INFO_DISCOVERING_INSTITUTIONS = "Discovering available Institution Types …"
    INFO_UPLOADING_DOCS = "Uploading business documents …"
    INFO_OPENING_EMAIL = "Opening email message …"
    INFO_POST_VERIFICATION = "Post-verification URL:"
    INFO_SELECTED_REGIONS = "Selected regions:"
    INFO_SELECTED_SERVICES = "Selected services:"
    INFO_SELECTED_COUNTRIES = "Selected countries:"
    INFO_SELECTED_INSTITUTIONS = "Selected institution types:"
    INFO_SELECTING = "Selecting:"
    INFO_AVAILABLE_REGIONS = "Available regions:"
    INFO_AVAILABLE_EXPERIENCE = "Available experience options:"
    INFO_AVAILABLE_SERVICES = "Available services:"
    INFO_AVAILABLE_COUNTRIES = "Available countries:"
    INFO_AVAILABLE_INSTITUTIONS = "Available institution types:"
    WARN_CHECKBOX_NOT_FOUND = "checkbox '{text}' not found"
    WARN_OPTION_NOT_FOUND = "option '{text}' not found in dialog"
    WARN_NO_OTP = "email body found but no 6-digit OTP"
    WARN_EMPTY_BODY = "email clicked but body is empty"
    WARN_NO_IFRAME = "Could not read iframe:"
    WARN_ERROR_DETECTED = "Page error detected:"
    WARN_OTP_INVALID = "OTP expired or invalid — attempting to resend …"
    WARN_NO_RESEND = "No resend button found — retrying fetch anyway"
    ERROR_NO_REG_LINK = "Could not discover a visible registration link on the homepage."
    ERROR_NO_OTP = "Could not retrieve OTP after maximum retries — aborting."
    ERROR_VERIFICATION_FAILED = "OTP verification failed after all retry attempts."
    ERROR_VERIFICATION_NO_SUCCESS = "OTP verification did not succeed."
    FINAL_SUCCESS = "SIGNUP AUTOMATION FINISHED  (SUCCESS)"
    FINAL_URL = "Final URL :"
    FINAL_CONTENT = "Page content (first lines):"
    FINAL_DONE = "Done. All resources released."

class Patterns:
    OTP_PATTERN = r"\b(\d{6})\b"
    EMAIL_KEYWORDS = ["otp", "signup", "verif", "confirm", "code"]
    ERROR_KEYWORDS = ["expired", "invalid"]