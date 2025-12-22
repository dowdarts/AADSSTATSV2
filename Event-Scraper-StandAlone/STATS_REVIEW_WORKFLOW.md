# Stats Review Workflow

## Overview
The Event Scraper now includes a **3-step workflow** with a comprehensive stats review table before sending data to the Admin Control Panel.

## Workflow Steps

### Step 1: Find Matches from Event
1. Enter DartConnect event URL (e.g., `https://tv.dartconnect.com/eventmenu/mt_joe6163l_1`)
2. Click **"Find Matches"**
3. System scrapes the event page and finds all match URLs
4. Displays match count and types (Round Robin vs Knockout)
5. Option to download Stage 1 data (match URLs) as JSON backup

### Step 2: Scrape Match Statistics
1. Click **"Scrape All Stats"** to extract player statistics from each match
2. Progress bar shows real-time scraping status
3. Each match displays:
   - Match number and type (RR or KO)
   - Scraping status (Pending → Scraping → Success/Failed)
   - Number of players added
4. Statistics extracted for each player:
   - Player name
   - 3-dart average
   - Legs played
   - 180s count
   - Highest checkout
   - Doubles hit/attempted
   - Match result (Won/Lost)
   - Tournament phase (Final, Semifinal, Quarterfinal, Group A, Group B)
5. Option to download Stage 2 data (full stats) as JSON backup

### Step 3: Review Stats Before Sending ⭐ NEW FEATURE
After scraping completes, a **comprehensive review table** appears showing:

#### Summary Statistics
- **Total Matches**: Number of matches scraped
- **Total Players**: Number of player entries
- **Avg 3DA**: Average 3-dart average across all players

#### Stats Table
Displays all scraped player statistics in a sortable table:
- Match number
- Player name
- 3-dart average (highlighted in red)
- Legs played
- 180s count (highlighted in gold)
- Highest checkout (highlighted in green)
- Doubles percentage (hit/attempted)
- Match result (Won in green, Lost in red)
- Tournament phase (badge display)

#### Actions Available
1. **✓ Send to Admin Control Panel (Staging)**
   - Sends all stats to Supabase `staging_matches` table
   - Shows confirmation dialog before sending
   - Displays success message with match/player count
   - Auto-resets scraper after successful send

2. **✏️ Edit Stats**
   - Placeholder for future inline editing
   - Currently shows instructions for manual editing via JSON

3. **✗ Discard All**
   - Clears the review table
   - Requires confirmation
   - Returns to Step 2 for re-scraping

## Data Flow Architecture

```
DartConnect Event
      ↓
[Step 1: Find Matches]
      ↓
Match URLs Extracted → Stage 1 JSON (backup)
      ↓
[Step 2: Scrape Stats]
      ↓
Player Stats Extracted → Stage 2 JSON (backup)
      ↓
[Step 3: Review Table] ⭐ LOCAL REVIEW CHECKPOINT
      ↓
User Confirms Data
      ↓
Supabase staging_matches Table
      ↓
Admin Control Panel
      ↓
Admin Reviews & Edits ⭐ ADMIN REVIEW CHECKPOINT
      ↓
Admin Approves
      ↓
Production Tables (event_standings, series_leaderboard)
      ↓
Public Display (GitHub Pages)
```

## Review Checkpoints

### Checkpoint 1: Scraper Review Table (This Feature)
- **Location**: Event Scraper UI (localhost:5000)
- **Purpose**: Verify data extraction accuracy before database submission
- **Actions**: Send, Edit (future), or Discard
- **User**: Tournament Admin / Data Entry Operator

### Checkpoint 2: Admin Control Panel
- **Location**: Admin Panel (localhost:8001)
- **Purpose**: Final review with inline editing before going live
- **Actions**: Edit any field, Approve, or Reject
- **User**: Tournament Admin

### Checkpoint 3: Public Display
- **Location**: GitHub Pages (public)
- **Purpose**: Live stats for tournament participants and fans
- **Read-only**: No editing capability

## Benefits of Review Table

### Data Quality Control
- Catch scraping errors before database submission
- Verify player names, averages, and stats
- Identify missing or incorrect data early

### Workflow Efficiency
- Review all stats at once in tabular format
- Summary statistics provide quick validation
- Download/upload JSON for offline review or backup

### Error Prevention
- Reduces bad data entering Supabase
- Minimizes admin panel corrections needed
- Prevents incorrect stats going live

## JSON Backup System

### Stage 1 JSON (Match URLs)
```json
{
  "version": "1.0",
  "stage": 1,
  "event_id": "mt_joe6163l_1",
  "timestamp": "2025-12-22T16:56:12.000Z",
  "matches": [
    {
      "url": "https://tv.dartconnect.com/history/...",
      "title": "Match 1",
      "match_number": 1,
      "match_type": "Knockout"
    }
  ],
  "match_count": 27
}
```

### Stage 2 JSON (Player Stats)
```json
{
  "version": "1.0",
  "stage": 2,
  "event_id": "mt_joe6163l_1",
  "timestamp": "2025-12-22T17:00:00.000Z",
  "stats": [
    {
      "match_url": "...",
      "match_title": "Match 1",
      "players_added": 2,
      "players": [
        {
          "player_name": "John Doe",
          "3_dart_average": 85.42,
          "legs_played": 5,
          "180s": 3,
          "highest_checkout": 121,
          "doubles_hit": 5,
          "doubles_attempted": 12,
          "match_won": true,
          "phase": "final"
        }
      ],
      "scraped_at": "2025-12-22T17:00:00.000Z"
    }
  ],
  "total_matches": 27,
  "total_players": 54
}
```

## Usage Tips

1. **Always Review Before Sending**
   - Check for unusual averages (too high/low)
   - Verify player name spellings
   - Confirm phase assignments are correct

2. **Use JSON Backups**
   - Download Stage 1 after finding matches
   - Download Stage 2 after scraping stats
   - Upload JSON to resume work or share data

3. **Monitor the Log**
   - Watch for scraping errors in real-time
   - Check progress messages for issues
   - Note any failed matches for re-scraping

4. **Confirmation Dialogs**
   - Always read confirmation messages carefully
   - They show exactly what will be sent
   - Cancel if anything looks wrong

## Troubleshooting

### Review Table Not Appearing
- Ensure scraping completed successfully
- Check that matches were found in Step 1
- Verify Stage 2 stats were scraped

### Stats Look Wrong
- Click **"Discard All"** to clear table
- Return to Step 2 and re-scrape
- Check DartConnect source page for accuracy

### Send to Admin Panel Fails
- Verify Flask server is running (localhost:5000)
- Check Supabase credentials in `.env`
- Review network errors in browser console

### Missing Player Data
- Some fields may be empty if not available from DartConnect
- Doubles % shows 0.0% if no checkout attempts recorded
- Highest checkout is 0 if no checkouts achieved

## Future Enhancements

### Inline Editing (Planned)
- Click any cell to edit value
- Validate input before saving
- Real-time average recalculation

### Sorting & Filtering (Planned)
- Click column headers to sort
- Filter by phase, player name, or stats range
- Search functionality

### Export Options (Planned)
- Export as CSV for spreadsheet review
- Print-friendly view
- Email stats summary

---

**Last Updated**: December 22, 2025  
**Version**: 1.0  
**Author**: AADS Stats V2 Development Team
