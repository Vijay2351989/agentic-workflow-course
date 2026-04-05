#!/usr/bin/env python3
"""YouTube Playlist Management - Execution Script

CLI tool for managing YouTube playlists via the YouTube Data API v3.
Uses OAuth 2.0 for authentication.

Usage:
    python3 execution/youtube_playlist.py list-playlists
    python3 execution/youtube_playlist.py list-videos --playlist "Name"
    python3 execution/youtube_playlist.py create --title "Name" [--description "Desc"] [--privacy private]
    python3 execution/youtube_playlist.py delete --playlist "Name"
    python3 execution/youtube_playlist.py add-video --playlist "Name" --video-url "URL"
    python3 execution/youtube_playlist.py remove-video --playlist "Name" --video-url "URL"
    python3 execution/youtube_playlist.py move-videos --from "Source" --to "Target" [--video-urls "url1,url2"] [--all]
    python3 execution/youtube_playlist.py copy-playlist --source "Source" --title "New Name" [--privacy private]
"""

import argparse
import re
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/youtube"]
BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"


def get_authenticated_service():
    """Authenticate and return a YouTube API service object."""
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print(f"Error: credentials.json not found at {CREDENTIALS_FILE}", file=sys.stderr)
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())
    return build("youtube", "v3", credentials=creds)


def extract_video_id(url_or_id):
    """Extract video ID from a YouTube URL or return as-is if already an ID."""
    patterns = [
        r"(?:youtube\.com/watch\?.*v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/)([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    if re.match(r"^[a-zA-Z0-9_-]{11}$", url_or_id):
        return url_or_id
    print(f"Error: Could not extract video ID from '{url_or_id}'", file=sys.stderr)
    sys.exit(1)


def resolve_playlist_id(youtube, name_or_id):
    """Resolve a playlist name to its ID. If it looks like an ID, return as-is."""
    if name_or_id.startswith("PL") or name_or_id.startswith("UU") or name_or_id.startswith("FL"):
        return name_or_id
    playlists = get_all_playlists(youtube)
    matches = [p for p in playlists if p["title"].lower() == name_or_id.lower()]
    if not matches:
        print(f"Error: Playlist '{name_or_id}' not found.", file=sys.stderr)
        print("Available playlists:", file=sys.stderr)
        for p in playlists:
            print(f"  - {p['title']}", file=sys.stderr)
        sys.exit(1)
    if len(matches) > 1:
        print(f"Warning: Multiple playlists named '{name_or_id}'. Using the first one.", file=sys.stderr)
    return matches[0]["id"]


def get_all_playlists(youtube):
    """Fetch all playlists for the authenticated user."""
    playlists = []
    request = youtube.playlists().list(part="snippet,contentDetails", mine=True, maxResults=50)
    while request:
        response = request.execute()
        for item in response.get("items", []):
            playlists.append({
                "id": item["id"],
                "title": item["snippet"]["title"],
                "description": item["snippet"].get("description", ""),
                "privacy": item["snippet"].get("privacyStatus", "unknown") if "status" in item else "unknown",
                "video_count": item["contentDetails"]["itemCount"],
            })
        request = youtube.playlists().list_next(request, response)
    return playlists


def get_all_playlist_items(youtube, playlist_id):
    """Fetch all videos in a playlist with pagination."""
    items = []
    request = youtube.playlistItems().list(
        part="snippet,contentDetails", playlistId=playlist_id, maxResults=50
    )
    while request:
        response = request.execute()
        for item in response.get("items", []):
            video_id = item["contentDetails"]["videoId"]
            items.append({
                "playlist_item_id": item["id"],
                "video_id": video_id,
                "title": item["snippet"]["title"],
                "position": item["snippet"]["position"],
                "url": f"https://youtube.com/watch?v={video_id}",
            })
        request = youtube.playlistItems().list_next(request, response)
    return items


# ── Commands ──────────────────────────────────────────────────────────────────


def cmd_list_playlists(args):
    youtube = get_authenticated_service()
    playlists = get_all_playlists(youtube)
    if not playlists:
        print("No playlists found.")
        return
    print(f"Found {len(playlists)} playlist(s):\n")
    for i, p in enumerate(playlists, 1):
        print(f"  {i}. {p['title']}  ({p['video_count']} videos)  [ID: {p['id']}]")
        if p["description"]:
            print(f"     {p['description'][:100]}")
    print()


def cmd_list_videos(args):
    youtube = get_authenticated_service()
    playlist_id = resolve_playlist_id(youtube, args.playlist or args.playlist_id)
    items = get_all_playlist_items(youtube, playlist_id)
    if not items:
        print("Playlist is empty.")
        return
    print(f"Found {len(items)} video(s):\n")
    for i, v in enumerate(items, 1):
        print(f"  {i}. {v['title']}")
        print(f"     {v['url']}")
    print()


def cmd_create(args):
    youtube = get_authenticated_service()
    body = {
        "snippet": {
            "title": args.title,
            "description": args.description or "",
        },
        "status": {
            "privacyStatus": args.privacy,
        },
    }
    response = youtube.playlists().insert(part="snippet,status", body=body).execute()
    print(f"Created playlist: {response['snippet']['title']}")
    print(f"  ID: {response['id']}")
    print(f"  Privacy: {response['status']['privacyStatus']}")
    print(f"  URL: https://youtube.com/playlist?list={response['id']}")


def cmd_delete(args):
    youtube = get_authenticated_service()
    playlist_id = resolve_playlist_id(youtube, args.playlist or args.playlist_id)
    youtube.playlists().delete(id=playlist_id).execute()
    print(f"Deleted playlist: {args.playlist or args.playlist_id}")


def cmd_add_video(args):
    youtube = get_authenticated_service()
    playlist_id = resolve_playlist_id(youtube, args.playlist or args.playlist_id)
    video_id = extract_video_id(args.video_url or args.video_id)
    body = {
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id,
            },
        },
    }
    response = youtube.playlistItems().insert(part="snippet", body=body).execute()
    print(f"Added video '{response['snippet']['title']}' to playlist.")


def cmd_remove_video(args):
    youtube = get_authenticated_service()
    playlist_id = resolve_playlist_id(youtube, args.playlist or args.playlist_id)
    video_id = extract_video_id(args.video_url or args.video_id)
    items = get_all_playlist_items(youtube, playlist_id)
    match = [item for item in items if item["video_id"] == video_id]
    if not match:
        print(f"Error: Video {video_id} not found in playlist.", file=sys.stderr)
        sys.exit(1)
    youtube.playlistItems().delete(id=match[0]["playlist_item_id"]).execute()
    print(f"Removed video '{match[0]['title']}' from playlist.")


def cmd_move_videos(args):
    youtube = get_authenticated_service()
    source_id = resolve_playlist_id(youtube, args.source)
    target_id = resolve_playlist_id(youtube, args.target)
    source_items = get_all_playlist_items(youtube, source_id)

    if args.all:
        to_move = source_items
    elif args.video_urls:
        video_ids = [extract_video_id(u.strip()) for u in args.video_urls.split(",")]
        to_move = [item for item in source_items if item["video_id"] in video_ids]
        if len(to_move) != len(video_ids):
            found_ids = {item["video_id"] for item in to_move}
            missing = [vid for vid in video_ids if vid not in found_ids]
            print(f"Warning: {len(missing)} video(s) not found in source playlist: {missing}", file=sys.stderr)
    else:
        print("Error: Specify --video-urls or --all", file=sys.stderr)
        sys.exit(1)

    if not to_move:
        print("No videos to move.")
        return

    print(f"Moving {len(to_move)} video(s) from '{args.source}' to '{args.target}'...\n")
    for item in to_move:
        try:
            body = {
                "snippet": {
                    "playlistId": target_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": item["video_id"],
                    },
                },
            }
            youtube.playlistItems().insert(part="snippet", body=body).execute()
            youtube.playlistItems().delete(id=item["playlist_item_id"]).execute()
            print(f"  Moved: {item['title']}")
        except HttpError as e:
            print(f"  Failed to move '{item['title']}': {e}", file=sys.stderr)

    print(f"\nDone. Moved {len(to_move)} video(s).")


def cmd_copy_playlist(args):
    youtube = get_authenticated_service()
    source_id = resolve_playlist_id(youtube, args.source)
    source_items = get_all_playlist_items(youtube, source_id)

    body = {
        "snippet": {
            "title": args.title,
            "description": args.description or f"Copy of {args.source}",
        },
        "status": {
            "privacyStatus": args.privacy,
        },
    }
    new_playlist = youtube.playlists().insert(part="snippet,status", body=body).execute()
    new_id = new_playlist["id"]
    print(f"Created playlist: {args.title} [ID: {new_id}]")

    print(f"Copying {len(source_items)} video(s)...\n")
    for item in source_items:
        try:
            add_body = {
                "snippet": {
                    "playlistId": new_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": item["video_id"],
                    },
                },
            }
            youtube.playlistItems().insert(part="snippet", body=add_body).execute()
            print(f"  Copied: {item['title']}")
        except HttpError as e:
            print(f"  Failed to copy '{item['title']}': {e}", file=sys.stderr)

    print(f"\nDone. Copied {len(source_items)} video(s) to '{args.title}'.")
    print(f"URL: https://youtube.com/playlist?list={new_id}")


# ── CLI Parser ────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="YouTube Playlist Management")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list-playlists
    subparsers.add_parser("list-playlists", help="List all your playlists")

    # list-videos
    lv = subparsers.add_parser("list-videos", help="List videos in a playlist")
    lv_group = lv.add_mutually_exclusive_group(required=True)
    lv_group.add_argument("--playlist", help="Playlist name")
    lv_group.add_argument("--playlist-id", help="Playlist ID")

    # create
    cr = subparsers.add_parser("create", help="Create a new playlist")
    cr.add_argument("--title", required=True, help="Playlist title")
    cr.add_argument("--description", default="", help="Playlist description")
    cr.add_argument("--privacy", default="private", choices=["public", "private", "unlisted"])

    # delete
    dl = subparsers.add_parser("delete", help="Delete a playlist")
    dl_group = dl.add_mutually_exclusive_group(required=True)
    dl_group.add_argument("--playlist", help="Playlist name")
    dl_group.add_argument("--playlist-id", help="Playlist ID")

    # add-video
    av = subparsers.add_parser("add-video", help="Add a video to a playlist")
    av_group = av.add_mutually_exclusive_group(required=True)
    av_group.add_argument("--playlist", help="Playlist name")
    av_group.add_argument("--playlist-id", help="Playlist ID")
    av_vid = av.add_mutually_exclusive_group(required=True)
    av_vid.add_argument("--video-url", help="YouTube video URL")
    av_vid.add_argument("--video-id", help="YouTube video ID")

    # remove-video
    rv = subparsers.add_parser("remove-video", help="Remove a video from a playlist")
    rv_group = rv.add_mutually_exclusive_group(required=True)
    rv_group.add_argument("--playlist", help="Playlist name")
    rv_group.add_argument("--playlist-id", help="Playlist ID")
    rv_vid = rv.add_mutually_exclusive_group(required=True)
    rv_vid.add_argument("--video-url", help="YouTube video URL")
    rv_vid.add_argument("--video-id", help="YouTube video ID")

    # move-videos
    mv = subparsers.add_parser("move-videos", help="Move videos between playlists")
    mv.add_argument("--from", dest="source", required=True, help="Source playlist name")
    mv.add_argument("--to", dest="target", required=True, help="Target playlist name")
    mv.add_argument("--video-urls", help="Comma-separated video URLs to move")
    mv.add_argument("--all", action="store_true", help="Move all videos")

    # copy-playlist
    cp = subparsers.add_parser("copy-playlist", help="Copy a playlist")
    cp.add_argument("--source", required=True, help="Source playlist name")
    cp.add_argument("--title", required=True, help="New playlist title")
    cp.add_argument("--description", default="", help="New playlist description")
    cp.add_argument("--privacy", default="private", choices=["public", "private", "unlisted"])

    args = parser.parse_args()

    command_map = {
        "list-playlists": cmd_list_playlists,
        "list-videos": cmd_list_videos,
        "create": cmd_create,
        "delete": cmd_delete,
        "add-video": cmd_add_video,
        "remove-video": cmd_remove_video,
        "move-videos": cmd_move_videos,
        "copy-playlist": cmd_copy_playlist,
    }

    try:
        command_map[args.command](args)
    except HttpError as e:
        print(f"YouTube API error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
