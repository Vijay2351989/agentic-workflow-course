# YouTube Playlist Management

## Goal
Manage YouTube playlists conversationally — list, create, delete, move videos between playlists, copy playlists, and more. Understand natural language requests and translate them into the correct sequence of operations.

## Inputs
- **User Queries**: Natural language requests about playlist operations (e.g., "move all videos from Watch Later to my Music playlist", "create a playlist called Travel Vlogs")
- **YouTube URLs**: Video or playlist URLs provided by the user
- **Playlist Names/IDs**: Can be referenced by name (case-insensitive) or YouTube playlist ID

## Tools/Scripts
- Script: `execution/youtube_playlist.py` — CLI tool for all YouTube playlist operations
- Auth: `credentials.json` (OAuth client) and `token.json` (auto-generated on first run)

### Available Commands
```bash
# List all playlists
python3 "Agentic Workflows/execution/youtube_playlist.py" list-playlists

# List videos in a playlist
python3 "Agentic Workflows/execution/youtube_playlist.py" list-videos --playlist "Playlist Name"

# Create a playlist
python3 "Agentic Workflows/execution/youtube_playlist.py" create --title "Name" --description "Desc" --privacy private

# Delete a playlist
python3 "Agentic Workflows/execution/youtube_playlist.py" delete --playlist "Name"

# Add a video to a playlist
python3 "Agentic Workflows/execution/youtube_playlist.py" add-video --playlist "Name" --video-url "https://youtube.com/watch?v=xxx"

# Remove a video from a playlist
python3 "Agentic Workflows/execution/youtube_playlist.py" remove-video --playlist "Name" --video-url "https://youtube.com/watch?v=xxx"

# Move videos between playlists (all or specific)
python3 "Agentic Workflows/execution/youtube_playlist.py" move-videos --from "Source" --to "Target" --all
python3 "Agentic Workflows/execution/youtube_playlist.py" move-videos --from "Source" --to "Target" --video-urls "url1,url2"

# Copy an entire playlist
python3 "Agentic Workflows/execution/youtube_playlist.py" copy-playlist --source "Source" --title "New Name" --privacy private
```

## Process

### Phase 1: Understand Intent

1. **Parse the User's Request**
   - Identify the operation: list, create, delete, add, remove, move, copy, reorder
   - Identify the playlist(s) involved (by name or URL)
   - Identify the video(s) involved (by URL, title description, or "all")
   - If ambiguous, ask for clarification before proceeding.

2. **Gather Context (if needed)**
   - If the user references a playlist by name but you're unsure which one, run `list-playlists` to show options.
   - If the user says "move those videos" without specifics, run `list-videos` on the source playlist and ask which ones.

### Phase 2: Confirm Destructive Actions

Before executing any of the following, **always confirm with the user**:
- **Deleting a playlist** — show playlist name and video count, ask "Are you sure?"
- **Removing videos** — show video titles being removed
- **Moving all videos** — show count and source/target playlists
- **Overwriting** — if target playlist already has videos, mention it

Non-destructive actions (listing, creating, adding, copying) can proceed without confirmation.

### Phase 3: Execute

1. **Run the appropriate command(s)** from `execution/youtube_playlist.py`
2. **Handle multi-step operations**:
   - "Move these 3 videos from A to B" → single `move-videos` command
   - "Create a playlist and add these videos" → `create` then `add-video` for each
   - "Copy playlist A but rename to B" → `copy-playlist`
3. **Report results** — show what was done (videos moved, playlist created, etc.)

### Phase 4: Follow-up

- Ask if the user wants to do anything else with their playlists.
- If an operation partially failed (e.g., 8/10 videos moved), report failures and ask if they want to retry.

## Interpreting Natural Language

Map common phrasings to operations:

| User Says | Operation |
|-----------|-----------|
| "show me my playlists" | `list-playlists` |
| "what's in my Music playlist" | `list-videos --playlist "Music"` |
| "create a playlist called X" | `create --title "X"` |
| "delete the X playlist" | `delete --playlist "X"` (confirm first!) |
| "add this video to X" | `add-video --playlist "X" --video-url "..."` |
| "remove this from X" | `remove-video --playlist "X" --video-url "..."` |
| "move everything from X to Y" | `move-videos --from "X" --to "Y" --all` |
| "move these videos from X to Y" | `move-videos --from "X" --to "Y" --video-urls "..."` |
| "duplicate playlist X as Y" | `copy-playlist --source "X" --title "Y"` |
| "make a backup of playlist X" | `copy-playlist --source "X" --title "X (backup)"` |

## Outputs
- Terminal output showing results of each operation
- Playlist URLs for newly created/copied playlists

## Edge Cases
- **First run / no token.json**: The script will open a browser for OAuth consent. Let the user know this will happen.
- **Token expired**: The script auto-refreshes tokens. If refresh fails, delete `token.json` and re-authenticate.
- **Playlist not found**: The script lists available playlists on error. Use this to help the user pick the right one.
- **Video already in playlist**: YouTube allows duplicates. Before adding, optionally check with `list-videos` if the user might not want duplicates.
- **API quota exceeded**: YouTube Data API has a daily quota (10,000 units). Listing is cheap (1 unit), but inserts/deletes cost more (50 units each). If quota is hit, inform the user to wait until the next day (quota resets at midnight Pacific Time).
- **Video unavailable**: Some videos may be private, deleted, or region-locked. The API will return an error for these — report and skip.
- **Large playlists**: The script handles pagination automatically. For playlists with 200+ videos, operations may take a moment.

## Learnings
- YouTube Data API v3 daily quota is 10,000 units. A single playlist item insert costs 50 units. Moving 100 videos = ~10,000 units (50 insert + 50 delete each = 100 per video... actually insert=50, delete=50, so 100 videos would exceed quota). For bulk operations with 50+ videos, warn the user about quota limits.
- Playlist names are NOT unique on YouTube. If a user has two playlists with the same name, the script uses the first match and warns.
- The "Watch Later" and "Liked videos" playlists are special system playlists and may have restrictions on certain API operations.
