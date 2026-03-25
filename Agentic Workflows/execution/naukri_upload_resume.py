"""
Naukri Resume Upload Script
Uploads a resume PDF to the user's Naukri.com profile using Playwright browser automation.

Usage:
    python3 execution/naukri_upload_resume.py --resume "docs/Resume_VijayBhatt.pdf"

Environment Variables Required:
    NAUKRI_EMAIL    - Naukri login email
    NAUKRI_PASSWORD - Naukri login password
"""

import argparse
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


def login(page):
    """Login to Naukri.com"""
    print("[1/4] Navigating to Naukri login page...")
    page.goto(NAUKRI_LOGIN_URL, wait_until="domcontentloaded", timeout=30000)
    time.sleep(2)

    print("[2/4] Entering credentials...")
    page.fill('input[placeholder="Enter your active Email ID / Username"]', NAUKRI_EMAIL)
    page.fill('input[placeholder="Enter your password"]', NAUKRI_PASSWORD)
    page.click('button[type="submit"]')

    # Wait for login to complete - check for redirect or profile element
    try:
        page.wait_for_url("**/mnjuser/homepage*", timeout=15000)
        print("       Login successful (redirected to homepage).")
    except PlaywrightTimeout:
        # Check if OTP is required
        if page.locator('text="Enter OTP"').count() > 0 or page.locator('input[placeholder*="OTP"]').count() > 0:
            print("\n⚠️  OTP/2FA required. Please enter the OTP manually in the browser.")
            print("    Waiting up to 120 seconds for OTP completion...")
            try:
                page.wait_for_url("**/mnjuser/homepage*", timeout=120000)
                print("       OTP verified, login successful.")
            except PlaywrightTimeout:
                print("ERROR: OTP timeout. Login failed.")
                sys.exit(1)
        else:
            # Check if we're already logged in (sometimes redirect differs)
            if "nlogin" not in page.url:
                print("       Login appears successful.")
            else:
                print("ERROR: Login failed. Check credentials in .env")
                sys.exit(1)


def upload_resume(page, resume_path):
    """Navigate to profile and upload resume"""
    print("[3/4] Navigating to profile page...")
    page.goto(NAUKRI_PROFILE_URL, wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)

    print("[4/4] Uploading resume...")

    # Naukri has a file input for resume upload - find it
    # The resume upload section typically has an input[type="file"] element
    file_input = page.locator('input[type="file"]').first

    if file_input.count() == 0:
        # Try clicking the "Update Resume" button first to reveal the file input
        update_btn = page.locator('text="Update resume"').or_(
            page.locator('text="Upload Resume"')
        ).or_(
            page.locator('[class*="resume"] input[type="file"]')
        ).or_(
            page.locator('#attachCV')
        )

        if update_btn.count() > 0:
            update_btn.first.click()
            time.sleep(2)
            file_input = page.locator('input[type="file"]').first

    if file_input.count() == 0:
        print("ERROR: Could not find resume upload input on profile page.")
        print("       Naukri UI may have changed. Update selectors in this script.")
        sys.exit(1)

    # Upload the file
    absolute_path = str(Path(resume_path).resolve())
    file_input.set_input_files(absolute_path)
    time.sleep(5)  # Wait for upload to process

    # Check for success indicators
    success_indicators = [
        page.locator('text="Resume uploaded successfully"'),
        page.locator('text="Resume updated successfully"'),
        page.locator('text="updated"'),
    ]

    upload_confirmed = False
    for indicator in success_indicators:
        if indicator.count() > 0:
            upload_confirmed = True
            break

    if upload_confirmed:
        print("\n✅ Resume uploaded successfully to Naukri!")
    else:
        # Upload may have succeeded without a visible toast — check if file name appears
        print("\n✅ Resume file submitted. Please verify on your Naukri profile.")


def main():
    parser = argparse.ArgumentParser(description="Upload resume to Naukri.com")
    parser.add_argument("--resume", required=True, help="Path to resume PDF file")
    parser.add_argument("--headless", action="store_true", default=False,
                        help="Run browser in headless mode (default: visible for OTP)")
    args = parser.parse_args()

    # Validate inputs
    if not NAUKRI_EMAIL or not NAUKRI_PASSWORD:
        print("ERROR: NAUKRI_EMAIL and NAUKRI_PASSWORD must be set in .env")
        sys.exit(1)

    resume_path = Path(args.resume)
    if not resume_path.exists():
        print(f"ERROR: Resume file not found: {resume_path}")
        sys.exit(1)

    if resume_path.stat().st_size > 2 * 1024 * 1024:
        print("ERROR: Resume file exceeds 2MB limit for Naukri upload.")
        sys.exit(1)

    print(f"Resume: {resume_path} ({resume_path.stat().st_size // 1024}KB)")
    print(f"Account: {NAUKRI_EMAIL}")
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
            upload_resume(page, args.resume)
        except Exception as e:
            print(f"\nERROR: {e}")
            # Save screenshot for debugging
            screenshot_path = ".tmp/naukri_error.png"
            os.makedirs(".tmp", exist_ok=True)
            page.screenshot(path=screenshot_path)
            print(f"       Screenshot saved: {screenshot_path}")
            sys.exit(1)
        finally:
            browser.close()


if __name__ == "__main__":
    main()
