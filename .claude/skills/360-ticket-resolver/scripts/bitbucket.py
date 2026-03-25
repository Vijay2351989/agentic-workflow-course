#!/usr/bin/env python3
"""
Bitbucket Cloud CLI helper for the 360-ticket-resolver skill.

Non-secret config — read from ../config.yml:
  bitbucket.base_url   e.g. https://bitbucket.org
  bitbucket.workspace  e.g. syncappinc

Secret — set in ~/.zshrc:
  BITBUCKET_API_TOKEN   (granular token with repository:read, pullrequest:read+write scopes)

Repo slug is auto-detected from the current git remote (no config needed).

Usage:
  python bitbucket.py create-pr --title "..." --body "..." --source BRANCH --target BRANCH
  python bitbucket.py get-pr PR-NUMBER
  python bitbucket.py list-prs [--state open|merged|declined]
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


# ---------------------------------------------------------------------------
# Config — load from ../config.yml
# ---------------------------------------------------------------------------

def _load_config() -> dict:
    config_path = Path(__file__).parent.parent / "config.yml"
    result = {"jira": {}, "bitbucket": {}}
    if not config_path.exists():
        return result
    section = None
    with open(config_path) as f:
        for line in f:
            line = line.rstrip()
            if line.startswith("jira:"):
                section = "jira"
            elif line.startswith("bitbucket:"):
                section = "bitbucket"
            elif section and ":" in line and not line.strip().startswith("#"):
                key, _, val = line.strip().partition(":")
                result[section][key.strip()] = val.strip().strip('"').strip("'")
    return result


def _detect_repo_slug() -> str:
    """Parse repo slug from git remote origin URL."""
    try:
        url = subprocess.check_output(
            ["git", "remote", "get-url", "origin"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        # Handles https://bitbucket.org/workspace/repo.git and git@bitbucket.org:workspace/repo.git
        match = re.search(r"[/:]([\w.-]+)/([\w.-]+?)(?:\.git)?$", url)
        if match:
            return match.group(2)
    except Exception:
        pass
    return ""


_CONFIG    = _load_config()
BASE_URL   = _CONFIG.get("bitbucket", {}).get("base_url", "https://bitbucket.org").rstrip("/")
WORKSPACE  = _CONFIG.get("bitbucket", {}).get("workspace", "")
USERNAME   = _CONFIG.get("jira", {}).get("username", "")
REPO_SLUG  = _detect_repo_slug()
API_TOKEN  = os.environ.get("BITBUCKET_API_TOKEN", "")


def _check_config():
    errors = []
    if not WORKSPACE:
        errors.append("  bitbucket.workspace missing in config.yml")
    if not REPO_SLUG:
        errors.append("  Could not detect repo slug from git remote — run inside the project directory")
    if not API_TOKEN:
        errors.append("  BITBUCKET_API_TOKEN not set in ~/.zshrc (granular token with Bitbucket scopes)")
    if errors:
        print("ERROR: missing configuration:\n" + "\n".join(errors), file=sys.stderr)
        sys.exit(1)


def _auth_header() -> str:
    token = base64.b64encode(f"{USERNAME}:{API_TOKEN}".encode()).decode()
    return f"Basic {token}"


def _api_url(path: str) -> str:
    return f"https://api.bitbucket.org/2.0/repositories/{WORKSPACE}/{REPO_SLUG}{path}"


def _request(method: str, path: str, body=None):
    url  = _api_url(path)
    data = json.dumps(body).encode() if body is not None else None
    req  = urllib.request.Request(
        url, data=data, method=method,
        headers={
            "Authorization": _auth_header(),
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} {e.reason}: {e.read().decode(errors='replace')}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_create_pr(title: str, body: str, source: str, target: str, close_source: bool = False, draft: bool = False):
    payload = {
        "title": title,
        "description": body,
        "source": {"branch": {"name": source}},
        "destination": {"branch": {"name": target}},
        "close_source_branch": close_source,
    }
    if draft:
        payload["draft"] = True
    data = _request("POST", "/pullrequests", payload)
    pr_id  = data.get("id")
    pr_url = data.get("links", {}).get("html", {}).get("href", "")
    print(f"PR created successfully!\n  ID: #{pr_id}\n  {source} → {target}\n  URL: {pr_url}")
    print(f"\nPR_URL={pr_url}")


def cmd_get_pr(pr_number: int):
    data   = _request("GET", f"/pullrequests/{pr_number}")
    source = data.get("source", {}).get("branch", {}).get("name", "")
    target = data.get("destination", {}).get("branch", {}).get("name", "")
    print(f"""
══════════════════════════════════════════════════════
PULL REQUEST #{data.get("id")}
══════════════════════════════════════════════════════
Title:  {data.get("title", "")}
State:  {data.get("state", "")}
Author: {data.get("author", {}).get("display_name", "")}
Branch: {source} → {target}
URL:    {data.get("links", {}).get("html", {}).get("href", "")}

Description:
{data.get("description", "")}
══════════════════════════════════════════════════════
""".strip())


def cmd_list_prs(state: str = "OPEN"):
    params = urllib.parse.urlencode({"state": state.upper(), "pagelen": 25})
    req    = urllib.request.Request(
        _api_url(f"/pullrequests?{params}"),
        headers={"Authorization": _auth_header(), "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)

    prs = data.get("values", [])
    if not prs:
        print(f"No {state.upper()} pull requests found.")
        return

    print(f"\n{'ID':<6} {'State':<10} {'Author':<20} {'Title'}")
    print("-" * 70)
    for pr in prs:
        pr_url = pr.get("links", {}).get("html", {}).get("href", "")
        print(f"#{pr.get('id', ''):<5} {pr.get('state', ''):<10} "
              f"{pr.get('author', {}).get('display_name', '')[:18]:<20} "
              f"{pr.get('title', '')[:45]}")
        print(f"       {pr_url}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    _check_config()

    parser = argparse.ArgumentParser(description="Bitbucket helper for 360-ticket-resolver skill")
    sub    = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("create-pr")
    p.add_argument("--title",        required=True)
    p.add_argument("--body",         required=True)
    p.add_argument("--source",       required=True)
    p.add_argument("--target",       required=True)
    p.add_argument("--close-source", action="store_true")
    p.add_argument("--draft",        action="store_true")

    p = sub.add_parser("get-pr");   p.add_argument("pr_number", type=int)
    p = sub.add_parser("list-prs"); p.add_argument("--state", default="open",
                                                    choices=["open", "merged", "declined", "superseded"])

    args = parser.parse_args()

    if args.command == "create-pr":
        cmd_create_pr(args.title, args.body, args.source, args.target, args.close_source, args.draft)
    elif args.command == "get-pr":
        cmd_get_pr(args.pr_number)
    elif args.command == "list-prs":
        cmd_list_prs(args.state)


if __name__ == "__main__":
    main()
