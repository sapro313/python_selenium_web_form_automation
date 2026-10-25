# QA Practice Forms — Python + Selenium

This project uses **Python, Selenium WebDriver, and `unittest`** to automate eight test cases on:

https://www.qapractice.com/practice-forms

The supplied email is `crao78689@gmail.com`. The other registration details are dummy test data.

## Requirements
- Python 3.10+
- Google Chrome installed
- Internet access

Selenium 4.6+ normally manages the compatible ChromeDriver automatically through Selenium Manager.

## Setup

Windows PowerShell:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run all tests
```bash
python -m unittest discover -s tests -v
```

## Show the browser
Windows PowerShell:
```powershell
$env:HEADLESS="0"
python -m unittest discover -s tests -v
```

macOS/Linux:
```bash
HEADLESS=0 python -m unittest discover -s tests -v
```

## Included cases
- TC01: Valid form submission
- TC02: Empty form validation
- TC03: Invalid email validation
- TC04: Invalid joining date format
- TC05: Missing communication preference
- TC06: Country dropdown options
- TC07: Clear/reset form
- TC08: Communication radio-button exclusivity

## Important
The selectors and expected validation messages are based on the previously outlined test cases; the tests have not been run against the current live website. If the page's markup or messages differ, update the relevant locator or expected text. Browser-native validation may also affect how invalid values are handled.
