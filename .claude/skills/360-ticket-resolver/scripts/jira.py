#!/usr/bin/env python3
"""
Jira CLI helper for the 360-ticket-resolver skill.

Non-secret config — read from ../config.yml:
  jira.base_url   e.g. https://antbrains.atlassian.net
  jira.username   e.g. vijay.bhatt@kristasoft.com

Secret — set in ~/.zshrc:
  JIRA_API_TOKEN   (granular token with read:jira-work, write:jira-work, read:jira-user scopes)

Usage:
  python jira.py get-issue TICKET-123
  python jira.py add-comment TICKET-123 "your comment"
  python jira.py get-transitions TICKET-123
  python jira.py transition TICKET-123 TRANSITION-ID
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path


# ---------------------------------------------------------------------------
# Config — load from ../config.yml (no third-party deps required)
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


_CONFIG   = _load_config()
BASE_URL  = _CONFIG.get("jira", {}).get("base_url", "").rstrip("/")
USERNAME  = _CONFIG.get("jira", {}).get("username", "")
API_TOKEN = os.environ.get("JIRA_API_TOKEN", "")


def _check_config():
    errors = []
    if not BASE_URL:
        errors.append("  jira.base_url missing in config.yml")
    if not USERNAME:
        errors.append("  jira.username missing in config.yml")
    if not API_TOKEN:
        errors.append("  JIRA_API_TOKEN not set in ~/.zshrc (classic API token)")
    if errors:
        print("ERROR: missing configuration:\n" + "\n".join(errors), file=sys.stderr)
        sys.exit(1)


def _auth_header() -> str:
    token = base64.b64encode(f"{USERNAME}:{API_TOKEN}".encode()).decode()
    return f"Basic {token}"


def _request(method: str, path: str, body=None):
    url = f"{BASE_URL}/rest/api/3{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
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

def cmd_get_issue(ticket: str):
    data   = _request("GET", f"/issue/{ticket}")
    fields = data.get("fields", {})

    print(f"""
══════════════════════════════════════════════════════
JIRA TICKET: {ticket}
══════════════════════════════════════════════════════
URL:        {BASE_URL}/browse/{ticket}
Summary:    {fields.get("summary", "")}
Status:     {fields.get("status", {}).get("name", "")}
Priority:   {fields.get("priority", {}).get("name", "")}
Assignee:   {(fields.get("assignee") or {}).get("displayName", "Unassigned")}
Reporter:   {(fields.get("reporter") or {}).get("displayName", "")}
Labels:     {", ".join(fields.get("labels", [])) or "none"}
Components: {", ".join(c["name"] for c in fields.get("components", [])) or "none"}

Description:
{_adf_to_text(fields.get("description") or {})}
══════════════════════════════════════════════════════
""".strip())


def cmd_add_comment(ticket: str, comment: str):
    _request("POST", f"/issue/{ticket}/comment", {
        "body": {
            "type": "doc", "version": 1,
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": comment}]}],
        }
    })
    print(f"Comment added to {ticket}")


def cmd_get_transitions(ticket: str):
    data = _request("GET", f"/issue/{ticket}/transitions")
    print(f"Available transitions for {ticket}:")
    for t in data.get("transitions", []):
        print(f"  ID={t['id']}  Name={t['name']}")


def cmd_transition(ticket: str, transition_id: str):
    _request("POST", f"/issue/{ticket}/transitions", {"transition": {"id": transition_id}})
    print(f"Transitioned {ticket} using transition ID {transition_id}")


# ---------------------------------------------------------------------------
# ADF → plain text
# ---------------------------------------------------------------------------

def _adf_to_text(node: dict) -> str:
    if not node:
        return ""
    parts = ([node["text"]] if "text" in node else []) + [_adf_to_text(c) for c in node.get("content", [])]
    result = "".join(parts)
    if node.get("type") in ("paragraph", "heading", "bulletList", "orderedList",
                             "listItem", "codeBlock", "blockquote", "rule"):
        result = result.strip() + "\n"
    return result


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    _check_config()

    parser = argparse.ArgumentParser(description="Jira helper for 360-ticket-resolver skill")
    sub    = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("get-issue");       p.add_argument("ticket")
    p = sub.add_parser("add-comment");     p.add_argument("ticket"); p.add_argument("comment")
    p = sub.add_parser("get-transitions"); p.add_argument("ticket")
    p = sub.add_parser("transition");      p.add_argument("ticket"); p.add_argument("transition_id")

    args = parser.parse_args()
    {"get-issue":        lambda: cmd_get_issue(args.ticket),
     "add-comment":      lambda: cmd_add_comment(args.ticket, args.comment),
     "get-transitions":  lambda: cmd_get_transitions(args.ticket),
     "transition":       lambda: cmd_transition(args.ticket, args.transition_id),
    }[args.command]()


if __name__ == "__main__":
    main()
