# Signup Automation System

A modular, object-oriented automation framework for educational consultancy partner registration.

## Project Structure

```
signup_automation/
│
├── main.py          # Entry point and orchestration
├── config.py        # Configuration and constants
├── utils.py         # Helper functions and utilities
└── signup_bot.py    # Core automation workflow
```

## Architecture

### **main.py**
- Application entry point
- Initializes the automation workflow
- Handles top-level error management
- Displays startup and completion information

### **config.py**
- Centralized configuration management
- Application constants and settings
- Data pools for realistic profile generation
- Form field identifiers and selectors
- Message templates and patterns

### **utils.py**
- Console output formatting (`ConsoleOutput`)
- Password generation (`PasswordGenerator`)
- Profile building (`ProfileBuilder`)
- Timing management (`DelayController`)
- OTP extraction (`OTPExtractor`)
- File operations (`FileManager`)
- Element discovery (`ElementFinder`)
- Form interactions (`FormInteractor`)
- Email reading (`EmailReader`)

### **signup_bot.py**
- Main workflow orchestration (`SignupBot`)
- Phase-based execution:
  - Phase 0: Terms acceptance
  - Phase 1: Account creation
  - Phase 1b: OTP verification
  - Phase 2: Agency details
  - Phase 3: Professional experience
  - Phase 4: Verification and documents

## Installation

```bash
# Install dependencies
pip install playwright asyncio

# Install browser
playwright install chromium
```

## Usage

```bash
python main.py
```

## Features

- **Modular Design**: Clean separation of concerns
- **Dynamic Element Discovery**: Adapts to form changes
- **Human-like Timing**: Natural delays with variance
- **Randomized Data**: Realistic profile generation
- **Error Handling**: Robust retry mechanisms
- **OTP Automation**: Email verification integration
- **File Management**: Temporary document handling

## Configuration

All settings can be modified in `config.py`:
- Browser dimensions and behavior
- Timing delays and variance
- Retry attempts and intervals
- Data pools for profile generation

## Dependencies

- `playwright` - Browser automation
- `asyncio` - Asynchronous execution
- Python 3.7+

## Error Handling

The system includes comprehensive error handling:
- OTP retrieval retries
- Form element discovery fallbacks
- Verification attempt management
- Resource cleanup on failure

## Security Note

This is an educational automation framework. Generated credentials are temporary and used only for demonstration purposes.