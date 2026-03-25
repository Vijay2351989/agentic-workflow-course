"""
Naukri Profile Update Script
Updates individual fields on the user's Naukri.com profile using Playwright browser automation.

Usage:
    python3 execution/naukri_update_profile.py --field "headline" --value "Principal Architect | AI & Distributed Systems"
    python3 execution/naukri_update_profile.py --field "key_skills" --value "Python,Node.js,LangChain,RAG,Microservices"
    python3 execution/naukri_update_profile.py --field "notice_period" --value "1 Month"
    python3 execution/naukri_update_profile.py --field "current_salary" --value "25"
    python3 execution/naukri_update_profile.py --field "expected_salary" --value "35"

Supported Fields:
    headline, key_skills, current_designation, current_company, total_experience,
    notice_period, current_salary, expected_salary, preferred_location, work_mode,
    employment_status, job_type, industry

Environment Variables Required:
    NAUKRI_EMAIL    - Naukri login email
    NAUKRI_PASSWORD - Naukri login password
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

load_dotenv()

NAUKRI_EMAIL = os.getenv("NAUKRI_EMAIL")
NAUKRI_PASSWORD = os.getenv("NAUKRI_PASSWORD")
NAUKRI_LOGIN_URL = "https://www.naukri.com/nlogin/login"
NAUKRI_PROFILE_URL = "https://www.naukri.com/mnjuser/profile"

# Mapping of field names to their Naukri profile section and edit strategy
FIELD_CONFIG = {
    "headline": {
        "section": "Resume Headline",
        "type": "text",
        "description": "Profile headline / resume title"
    },
    "key_skills": {
        "section": "Key Skills",
        "type": "tags",
        "description": "Comma-separated list of skills"
    },
    "current_designation": {
        "section": "Employment",
        "type": "text",
        "description": "Current job title"
    },
    "current_company": {
        "section": "Employment",
        "type": "text",
        "description": "Current employer name"
    },
    "total_experience": {
        "section": "Basic Details",
        "type": "dropdown",
        "description": "Total years of experience (e.g., '15 Years')"
    },
    "notice_period": {
        "section": "Basic Details",
        "type": "dropdown",
        "description": "Notice period (e.g., '1 Month', '2 Months', '3 Months', 'Serving Notice Period', 'Immediately Available')"
    },
    "current_salary": {
        "section": "Basic Details",
        "type": "text",
        "description": "Current annual salary in Lakhs (e.g., '25')"
    },
    "expected_salary": {
        "section": "Basic Details",
        "type": "text",
        "description": "Expected annual salary in Lakhs (e.g., '35')"
    },
    "preferred_location": {
        "section": "Basic Details",
        "type": "tags",
        "description": "Preferred work locations (comma-separated)"
    },
    "work_mode": {
        "section": "Basic Details",
        "type": "dropdown",
        "description": "Work mode preference (e.g., 'Remote', 'Hybrid', 'On-site')"
    },
    "employment_status": {
        "section": "Basic Details",
        "type": "dropdown",
        "description": "Current status (e.g., 'Currently Employed', 'Actively Looking')"
    },
    "job_type": {
        "section": "Basic Details",
        "type": "dropdown",
        "description": "Job type (e.g., 'Permanent', 'Contractual', 'Both')"
    },
    "industry": {
        "section": "Basic Details",
        "type": "text",
        "description": "Preferred industry"
    },
}


def login(page):
    """Login to Naukri.com"""
    print("[1/4] Navigating to Naukri login page...")
    page.goto(NAUKRI_LOGIN_URL, wait_until="domcontentloaded", timeout=30000)
    time.sleep(2)

    print("[2/4] Entering credentials...")
    page.fill('input[placeholder="Enter your active Email ID / Username"]', NAUKRI_EMAIL)
    page.fill('input[placeholder="Enter your password"]', NAUKRI_PASSWORD)
    page.click('button[type="submit"]')

    try:
        page.wait_for_url("**/mnjuser/homepage*", timeout=15000)
        print("       Login successful.")
    except PlaywrightTimeout:
        if page.locator('text="Enter OTP"').count() > 0 or page.locator('input[placeholder*="OTP"]').count() > 0:
            print("\n⚠️  OTP/2FA required. Please enter the OTP manually in the browser.")
            print("    Waiting up to 120 seconds for OTP completion...")
            try:
                page.wait_for_url("**/mnjuser/homepage*", timeout=120000)
                print("       OTP verified, login successful.")
            except PlaywrightTimeout:
                print("ERROR: OTP timeout. Login failed.")
                sys.exit(1)
        elif "nlogin" not in page.url:
            print("       Login appears successful.")
        else:
            print("ERROR: Login failed. Check credentials in .env")
            sys.exit(1)


def navigate_to_profile(page):
    """Navigate to the profile editing page"""
    print("[3/4] Navigating to profile page...")
    page.goto(NAUKRI_PROFILE_URL, wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)


def find_and_click_edit(page, section_name):
    """Find a section on the profile page and click its edit button"""
    # Naukri profile sections have edit icons/buttons near section headers
    # Try multiple strategies to find the edit button

    # Strategy 1: Find section header and click nearby edit icon
    section = page.locator(f'text="{section_name}"').first
    if section.count() > 0:
        # Look for edit icon near this section
        parent = section.locator("xpath=ancestor::div[contains(@class,'widgetHead') or contains(@class,'sectionHead')]").first
        if parent.count() > 0:
            edit_btn = parent.locator('[class*="edit"], [class*="Edit"], .editIcon, span.edit').first
            if edit_btn.count() > 0:
                edit_btn.click()
                time.sleep(2)
                return True

    # Strategy 2: Find by edit pencil icon within the section container
    section_containers = page.locator(f'//*[contains(text(),"{section_name}")]/ancestor::section | //*[contains(text(),"{section_name}")]/ancestor::div[contains(@class,"widget")]')
    if section_containers.count() > 0:
        container = section_containers.first
        edit_icon = container.locator('.edit, .editWidget, [data-ga-track*="edit"], span[class*="edit"]').first
        if edit_icon.count() > 0:
            edit_icon.click()
            time.sleep(2)
            return True

    # Strategy 3: Direct click on section text (some sections open editor on click)
    if section.count() > 0:
        section.click()
        time.sleep(2)
        return True

    print(f"       Warning: Could not find edit button for section '{section_name}'")
    return False


def update_text_field(page, field_name, value, config):
    """Update a text-based field"""
    section = config["section"]
    if not find_and_click_edit(page, section):
        return False

    # Try to find and update the text input/textarea
    # Look for input fields within the open editor modal/section
    editor = page.locator('.modal, .editSection, [class*="editWidget"], [class*="overlay"]').first
    if editor.count() > 0:
        text_input = editor.locator('input[type="text"], textarea').first
        if text_input.count() > 0:
            text_input.fill("")
            text_input.fill(value)
            time.sleep(1)

            # Click save button
            save_btn = editor.locator('button:text("Save"), button:text("save"), button[type="submit"]').first
            if save_btn.count() > 0:
                save_btn.click()
                time.sleep(3)
                return True

    print(f"       Warning: Could not update {field_name}. UI structure may have changed.")
    return False


def update_tags_field(page, field_name, value, config):
    """Update a tag/chip-based field (like skills)"""
    section = config["section"]
    if not find_and_click_edit(page, section):
        return False

    tags = [t.strip() for t in value.split(",")]

    editor = page.locator('.modal, .editSection, [class*="editWidget"], [class*="overlay"]').first
    if editor.count() > 0:
        tag_input = editor.locator('input[type="text"]').first
        if tag_input.count() > 0:
            for tag in tags:
                tag_input.fill(tag)
                time.sleep(0.5)
                # Press Enter to add tag, or click suggestion
                tag_input.press("Enter")
                time.sleep(0.5)

            # Click save
            save_btn = editor.locator('button:text("Save"), button:text("save"), button[type="submit"]').first
            if save_btn.count() > 0:
                save_btn.click()
                time.sleep(3)
                return True

    print(f"       Warning: Could not update {field_name} tags. UI structure may have changed.")
    return False


def update_dropdown_field(page, field_name, value, config):
    """Update a dropdown/select field"""
    section = config["section"]
    if not find_and_click_edit(page, section):
        return False

    editor = page.locator('.modal, .editSection, [class*="editWidget"], [class*="overlay"]').first
    if editor.count() > 0:
        # Try clicking dropdown and selecting value
        dropdown = editor.locator('select, [class*="dropdown"], [class*="select"]').first
        if dropdown.count() > 0:
            dropdown.click()
            time.sleep(1)
            option = page.locator(f'text="{value}"').first
            if option.count() > 0:
                option.click()
                time.sleep(1)

                save_btn = editor.locator('button:text("Save"), button:text("save"), button[type="submit"]').first
                if save_btn.count() > 0:
                    save_btn.click()
                    time.sleep(3)
                    return True

    print(f"       Warning: Could not update {field_name} dropdown. UI structure may have changed.")
    return False


def update_field(page, field_name, value):
    """Route to the appropriate update function based on field type"""
    config = FIELD_CONFIG[field_name]
    field_type = config["type"]

    print(f"[4/4] Updating {field_name}: {value}")

    if field_type == "text":
        success = update_text_field(page, field_name, value, config)
    elif field_type == "tags":
        success = update_tags_field(page, field_name, value, config)
    elif field_type == "dropdown":
        success = update_dropdown_field(page, field_name, value, config)
    else:
        print(f"ERROR: Unknown field type '{field_type}' for field '{field_name}'")
        return False

    if success:
        print(f"\n✅ Successfully updated {field_name} to: {value}")
    else:
        print(f"\n⚠️  Update may not have completed for {field_name}. Please verify on Naukri profile.")

    return success


def main():
    parser = argparse.ArgumentParser(description="Update Naukri.com profile fields")
    parser.add_argument("--field", required=True, choices=list(FIELD_CONFIG.keys()),
                        help="Profile field to update")
    parser.add_argument("--value", required=True, help="New value for the field")
    parser.add_argument("--headless", action="store_true", default=False,
                        help="Run browser in headless mode (default: visible for OTP)")
    args = parser.parse_args()

    if not NAUKRI_EMAIL or not NAUKRI_PASSWORD:
        print("ERROR: NAUKRI_EMAIL and NAUKRI_PASSWORD must be set in .env")
        sys.exit(1)

    config = FIELD_CONFIG[args.field]
    print(f"Field:       {args.field} ({config['description']})")
    print(f"New Value:   {args.value}")
    print(f"Section:     {config['section']}")
    print(f"Account:     {NAUKRI_EMAIL}")
    print("-" * 50)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            login(page)
            navigate_to_profile(page)
            update_field(page, args.field, args.value)
        except Exception as e:
            print(f"\nERROR: {e}")
            screenshot_path = ".tmp/naukri_profile_error.png"
            os.makedirs(".tmp", exist_ok=True)
            page.screenshot(path=screenshot_path)
            print(f"       Screenshot saved: {screenshot_path}")
            sys.exit(1)
        finally:
            browser.close()


if __name__ == "__main__":
    main()
