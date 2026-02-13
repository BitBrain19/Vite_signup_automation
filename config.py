"""
Configuration module containing all constants and data pools
"""

import time
import random

# Application configuration
class ApplicationConfig:
    """Core application settings"""
    TARGET_URL = "https://authorized-partner.vercel.app"
    TIMESTAMP = int(time.time())
    
    # Timing configuration
    MIN_DELAY_MS = 800
    MAX_DELAY_MS = 2400
    DELAY_VARIANCE = 400
    
    # Browser settings
    BROWSER_WIDTH = 1280
    BROWSER_HEIGHT = 900
    SLOW_MOTION_MS = 200
    
    # OTP retrieval settings
    MAX_OTP_RETRIES = 20
    OTP_RETRY_INTERVAL = 3
    MAX_VERIFICATION_ATTEMPTS = 3
    
    # Email configuration
    EMAIL_DOMAIN = "mailinator.com"
    MAILINATOR_INBOX_URL = "https://www.mailinator.com/v4/public/inboxes.jsp?to="
    
    # Output settings
    SEPARATOR_LENGTH = 64

class DataPools:
    """Realistic data pools for generating registration information"""
    
    FIRST_NAMES = [
        "Pushkar", "Sachin", "Niranjan", "Raj", "Nabin"
    ]
    
    LAST_NAMES = [
        "Jha", "Bhatta", "Chaudhary", "Ghimire", "Subedi"
    ]
    
    ORGANIZATION_PREFIXES = [
        "Himalayan", "Everest", "Kathmandu", "Nepal", "Gorkha", "Lumbini",
        "Sagarmatha", "Annapurna", "National", "NextGen", "Bright", "Future",
        "Sunrise", "Kantipur", "Bagmati", "Gandaki", "Karnali"
    ]
    
    ORGANIZATION_SUFFIXES = [
        "Education Foundation", "International Education", "Educational Consultancy",
        "Study Center", "Abroad Studies", "Education Network", "Foundation",
        "Consulting Pvt Ltd", "Group of Education", "Academic Center"
    ]
    
    POSITION_TITLES = [
        "Director", "Managing Director", "Senior Counselor", "Education Manager",
        "Chief Executive Officer", "Head of Operations", "Senior Advisor",
        "Founder", "Academic Head", "Business Development Manager"
    ]
    
    DOMAIN_NAMES = [
        "nepalstudy", "himalayanedu", "ktmedc", "brightfuture",
        "studyabroadnepal", "nextgenedu", "globalmigration", "careerpathway",
        "futurestudy", "abroaddreams", "dreamconsult"
    ]
    
    STREET_NAMES = [
        "Putalisadak", "New Baneshwor", "Dillibazar", "Bagbazar",
        "Kamaladi", "Hattisar", "Tripureshwor", "Kupandole",
        "Jhamsikhel", "Lazimpat", "Durbar Marg", "Sundhara"
    ]
    
    CITY_NAMES = [
        "Kathmandu", "Lalitpur", "Bhaktapur", "Pokhara",
        "Chitwan", "Biratnagar", "Butwal", "Dharan",
        "Nepalgunj", "Hetauda"
    ]
    
    OPERATIONAL_REGIONS = [
        "Australia", "Europe", "North America", "Asia", "Middle East",
        "United Kingdom", "South America", "Africa"
    ]
    
    EXPERIENCE_YEARS = ["1 Year", "2 Years", "3 Years", "5 Years", "10 Years"]
    
    SPECIALIZATION_AREAS = [
        "Student Visa Services and Documentation",
        "University Placements and Admissions",
        "Standardized Test Preparation (IELTS/PTE)",
        "Scholarship Assistance and Financial Guidance",
        "Migration Services and PR Pathways",
        "Career Counseling and Course Selection",
        "Pre-departure Briefing and Accommodation"
    ]
    
    CERTIFICATIONS = [
        "QEAC Certified Agent",
        "ICEF Agency Status",
        "Education New Zealand Trained Agent",
        "British Council Certified Agent",
        "UniAgent Certified",
        "TITI Certified Counselor",
        "ISANA Member"
    ]
    
    DESTINATION_COUNTRIES = [
        "Australia", "Canada", "United Kingdom", "United States",
        "New Zealand", "Germany", "Japan", "South Korea"
    ]
    
    SERVICE_TYPES = [
        "Career Counseling",
        "Admission Applications",
        "Visa Processing",
        "Test Preparation"
    ]
    
    INSTITUTION_CATEGORIES = ["Universities", "Colleges"]

class FieldNames:
    """Form field identifiers"""
    
    # Step 1: Account Setup
    FIRST_NAME = "firstName"
    LAST_NAME = "lastName"
    EMAIL = "email"
    PHONE_NUMBER = "phoneNumber"
    PASSWORD = "password"
    CONFIRM_PASSWORD = "confirmPassword"
    
    # Step 2: Agency Details
    AGENCY_NAME = "agency_name"
    ROLE_IN_AGENCY = "role_in_agency"
    AGENCY_EMAIL = "agency_email"
    AGENCY_WEBSITE = "agency_website"
    AGENCY_ADDRESS = "agency_address"
    
    # Step 3: Professional Experience
    STUDENTS_RECRUITED = "number_of_students_recruited_annually"
    FOCUS_AREA = "focus_area"
    SUCCESS_METRICS = "success_metrics"
    
    # Step 4: Verification
    BUSINESS_REG_NUMBER = "business_registration_number"
    CERTIFICATION_DETAILS = "certification_details"

class Selectors:
    """CSS/XPath selectors for UI elements"""
    
    # Common
    CHECKBOX_BUTTON = "button[role='checkbox']"
    COMBOBOX_BUTTON = "button[role='combobox']"
    SUBMIT_BUTTON = "button[type='submit']"
    ROLE_DIALOG = "[role='dialog']"
    ROLE_OPTION = "[role='option']"
    FILE_INPUT = "input[type='file']"
    
    # Specific elements
    CONTINUE_BUTTON = "button:has-text('Continue')"
    OTP_INPUT = "input[inputmode='numeric']"
    ADD_DOCUMENTS_BUTTON = "button:has-text('Add Documents')"
    FINAL_SUBMIT_BUTTON = "button[type='submit']:has-text('Submit')"
    
    # Error elements
    ERROR_ALERT = "[role='alert'], .text-red, .text-destructive, .error"
    
    # Resend button
    RESEND_BUTTON = "button:has-text('Resend'), button:has-text('resend'), a:has-text('Resend'), a:has-text('resend')"
    
    # Email iframe
    EMAIL_IFRAME = "#html_msg_body"
    BODY_ELEMENT = "body"
    
    # Table elements
    TABLE_ROWS = "table tbody tr"
    
    # Labels
    LABEL_ELEMENT = "label"

class Messages:
    """Log messages and output strings"""
    
    # Headers
    HEADER_TERMS = "TERMS & CONDITIONS"
    HEADER_ACCOUNT = "ACCOUNT SETUP"
    HEADER_OTP = "OTP VERIFICATION  (via Mailinator)"
    HEADER_AGENCY = "AGENCY DETAILS"
    HEADER_EXPERIENCE = "PROFESSIONAL EXPERIENCE"
    HEADER_VERIFICATION = "VERIFICATION & PREFERENCES"
    
    # Success messages
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
    
    # Info messages
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
    
    # Warning messages
    WARN_CHECKBOX_NOT_FOUND = "checkbox '{text}' not found"
    WARN_OPTION_NOT_FOUND = "option '{text}' not found in dialog"
    WARN_NO_OTP = "email body found but no 6-digit OTP"
    WARN_EMPTY_BODY = "email clicked but body is empty"
    WARN_NO_IFRAME = "Could not read iframe:"
    WARN_ERROR_DETECTED = "Page error detected:"
    WARN_OTP_INVALID = "OTP expired or invalid — attempting to resend …"
    WARN_NO_RESEND = "No resend button found — retrying fetch anyway"
    
    # Error messages
    ERROR_NO_REG_LINK = "Could not discover a visible registration link on the homepage."
    ERROR_NO_OTP = "Could not retrieve OTP after maximum retries — aborting."
    ERROR_VERIFICATION_FAILED = "OTP verification failed after all retry attempts."
    ERROR_VERIFICATION_NO_SUCCESS = "OTP verification did not succeed."
    
    # Final output
    FINAL_SUCCESS = "SIGNUP AUTOMATION FINISHED  (SUCCESS)"
    FINAL_URL = "Final URL :"
    FINAL_CONTENT = "Page content (first lines):"
    FINAL_DONE = "Done. All resources released."

class Patterns:
    """Regular expression patterns"""
    
    OTP_PATTERN = r"\b(\d{6})\b"
    
    # Keywords for email detection
    EMAIL_KEYWORDS = ["otp", "signup", "verif", "confirm", "code"]
    
    # Error keywords
    ERROR_KEYWORDS = ["expired", "invalid"]