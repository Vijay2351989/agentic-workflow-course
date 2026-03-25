# Resume Upgrade & Naukri Profile Sync

## Goal
Interactively update the user's resume based on their requests, generate a new PDF version, and provide a structured Naukri profile update checklist with recommended values extracted from the resume.

## Inputs
- **Resume PDF**: `docs/Resume_VijayBhatt.pdf` (current version, always read first)
- **Resume LaTeX Source**: `docs/Resume_VijayBhatt.tex` (editable source)
- **User Queries**: Conversational input about what to update

## Tools/Scripts
- Script: `execution/compile_latex.py` (compiles .tex to PDF using Tectonic; auto-installs Tectonic if not found)
- Preserved for future use: `execution/naukri_upload_resume.py`, `execution/naukri_update_profile.py` (Playwright-based, currently unusable due to Naukri's app-only restriction)

## Process

### Phase 1: Resume Update (Conversational Loop)

1. **Read Current Resume**
   - Read `docs/Resume_VijayBhatt.pdf` to understand current content and structure.
   - Read `docs/Resume_VijayBhatt.tex` to have the editable LaTeX source ready.

2. **Ask for Updates**
   - Ask the user: *"What updates would you like to make to your resume?"*
   - Listen for the user's request — it could be about any section:
     - Professional Summary
     - Core Skills / Technical Skills
     - Professional Experience (any company)
     - Key Projects
     - Personal Projects
     - Education
     - Adding new sections
     - Removing/restructuring content

3. **Understand & Apply Changes**
   - Understand the user's intent and identify the relevant section(s) in the `.tex` file.
   - Make the edits to `docs/Resume_VijayBhatt.tex`.
   - Explain what was changed and show the relevant updated section to the user.

4. **Confirmation Loop**
   - Ask the user: *"Are you happy with this update, or would you like any changes?"*
   - **Decision**:
     - **User wants changes**: Go back to step 3, apply revisions.
     - **User wants more updates**: Go back to step 2 for next update.
     - **User confirms (says yes/done/looks good)**: Proceed to Phase 2.

### Phase 2: Version Management & PDF Generation

1. **Rename Old Resume**
   - Rename the current `docs/Resume_VijayBhatt.pdf` to `docs/Resume_VijayBhatt_[YYYY-MM-DD].pdf` (using today's date as the backup suffix).

2. **Generate New PDF**
   - Run `execution/compile_latex.py` to compile the updated `.tex` to PDF:
     ```bash
     python3 "execution/compile_latex.py" --input "docs/Resume_VijayBhatt.tex" --output "docs/Resume_VijayBhatt.pdf"
     ```
   - The script automatically checks for Tectonic (a standalone LaTeX engine) and installs it if not found (via Homebrew on macOS, apt on Linux, or conda as fallback).
   - **On failure**: Check script output for LaTeX errors, fix the `.tex` source, and retry.

3. **Verify New PDF**
   - Read `docs/Resume_VijayBhatt.pdf` to confirm it exists and reflects the updates.

### Phase 3: Naukri Profile Update Checklist (Manual via App)

**Context**: As of March 2026, Naukri.com has moved profile viewing and editing to app-only. Web profile editing shows "COMING SOON" and redirects users to the mobile app. There is no public API for job seekers. Therefore, Naukri updates must be done manually via the Naukri mobile app.

1. **Generate Naukri Update Checklist**
   - Based on the updated resume, generate a structured checklist with pre-filled values:

   ```
   ═══════════════════════════════════════════════════════
   NAUKRI PROFILE UPDATE CHECKLIST
   ═══════════════════════════════════════════════════════

   📄 RESUME UPLOAD
   [ ] Upload new Resume_VijayBhatt.pdf via:
       App → Profile → Resume → Update Resume

   👤 PROFILE FIELDS (auto-extracted from resume)
   [ ] Profile Headline:
       → [extracted from resume header]
   [ ] Current Designation:
       → [from latest experience entry]
   [ ] Current Company:
       → [from latest experience entry]
   [ ] Total Experience:
       → [calculated from resume timeline]
   [ ] Key Skills:
       → [top skills extracted from Core Skills section]
   [ ] Profile Summary:
       → [first 2-3 sentences of Professional Summary]
   ```

2. **Ask Additional Profile Questions**
   - Proactively ask the user about fields that can't be derived from the resume:
     - *"Are you currently serving a notice period? If yes, how long?"*
     - *"What is your current annual salary (CTC)? Would you like to update it on Naukri?"*
     - *"What is your expected annual salary (CTC)?"*
     - *"What is your preferred work location(s)?"*
     - *"Are you open to remote/hybrid/on-site roles?"*
     - *"What is your current employment status — employed, actively looking, or open to opportunities?"*
     - *"Would you like to update your preferred job type — permanent, contract, or both?"*
     - *"Any preferred industry or company type you'd like to highlight?"*

3. **Generate Complete Checklist**
   - Append user's answers to the checklist:

   ```
   💼 ADDITIONAL PROFILE FIELDS
   [ ] Notice Period: → [user's answer]
   [ ] Current Salary: → [user's answer] LPA
   [ ] Expected Salary: → [user's answer] LPA
   [ ] Preferred Location(s): → [user's answer]
   [ ] Work Mode: → [user's answer]
   [ ] Employment Status: → [user's answer]
   [ ] Job Type: → [user's answer]
   [ ] Industry: → [user's answer]

   ═══════════════════════════════════════════════════════
   Open Naukri App → Profile → Edit each field above
   ═══════════════════════════════════════════════════════
   ```

4. **Confirmation Loop**
   - Ask: *"Go through the checklist on the Naukri app. Let me know when done, or if you want to change any values."*
   - **Decision**:
     - **User wants changes**: Update the checklist values and re-present.
     - **User confirms done**: Proceed to completion.

### Phase 4: Completion

1. **Summary**
   - Present a summary of everything that was done:
     - Resume sections updated (list changes)
     - Old resume backed up as `Resume_VijayBhatt_[date].pdf`
     - New resume generated as `Resume_VijayBhatt.pdf`
     - Naukri checklist provided with pre-filled values
   - *"Your resume is updated! Use the checklist above to sync your Naukri profile via the app."*

## Outputs (Deliverables)
- **Updated LaTeX source**: `docs/Resume_VijayBhatt.tex`
- **New PDF resume**: `docs/Resume_VijayBhatt.pdf`
- **Backup of old resume**: `docs/Resume_VijayBhatt_[date].pdf`
- **Naukri update checklist**: Structured checklist with pre-filled values for manual app update

## Edge Cases
- **No LaTeX compiler**: `compile_latex.py` auto-installs Tectonic. If auto-install fails (no brew/apt/conda), the script prints manual install instructions.
- **Resume PDF not found**: Ask user to place it at `docs/Resume_VijayBhatt.pdf`.
- **User provides vague update**: Ask clarifying questions before making changes.
- **Naukri web editing becomes available again**: If Naukri re-enables web profile editing, update this directive to add automated Playwright-based scripts for resume upload and profile field updates. Check `execution/naukri_upload_resume.py` and `execution/naukri_update_profile.py` — they were built for this but are currently unusable due to Naukri's app-only restriction.

## Learnings
- As of March 2026, Naukri.com profile editing is app-only. Web version shows "COMING SOON" for profile viewing & editing.
- Naukri does NOT provide public APIs for job seekers. Enterprise/recruiter APIs exist under commercial contracts only.
- Naukri Android app bypasses system proxy settings and uses certificate pinning, making API interception impractical without rooting or APK patching.
- Resume upload on Naukri accepts PDF format, max 2MB.
- The Playwright-based execution scripts (`naukri_upload_resume.py`, `naukri_update_profile.py`) are preserved in `execution/` for future use if web editing returns.
