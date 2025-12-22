# AADS Stats V2 - Event-Based Scraping System

## Overview
The AADS Stats platform now supports event-specific scraping for Events 1-6, with a two-stage workflow that separates match results from detailed statistics.

## Architecture

### Event Structure
- **Events 1-6**: Regular AADS tournament events
- **Event 7**: Tournament of Champions (different logic, not yet implemented)

Each event follows the same 27-match structure:
- 1 Final
- 2 Semifinals  
- 4 Quarterfinals
- 10 Group A Round Robin matches
- 10 Group B Round Robin matches

## Two-Stage Scraping Workflow

### Stage 1: Match Results (Basic Data)
**Purpose**: Quickly capture essential match outcomes

**Data Collected**:
- Player names (Player 1 vs Player 2)
- Match score (e.g., "3-2")
- Winner
- Phase (Final, Semifinal, Quarterfinal, Round Robin)
- Group (A or B for round robin)

**API Endpoint**: `/api/scrape_match_result`

**Speed**: ~200ms per match (faster, no detailed parsing)

### Stage 2: Match Details (Statistical Data)
**Purpose**: Extract comprehensive player statistics

**Data Collected**:
- 3-dart average
- Legs played
- 100+ scores count
- 120+ scores count
- 140+ scores count
- 160+ scores count
- 180s count
- Highest checkout
- Doubles hit / Doubles attempted
- Sets played (for knockout matches)

**API Endpoint**: `/api/scrape_match_details`

**Speed**: ~500ms per match (slower, detailed parsing)

**Match Format Handling**:
- **Round Robin**: Best of 5 legs (first to 3)
- **Knockout**: Set play (best of 5 sets, each set first to 3 legs)

## Scraper UI Workflow

### Step 1: Select Event & Find Matches
1. User selects event number from dropdown (Events 1-6)
2. User enters DartConnect event URL
3. Click "Find Matches" button
4. System scrapes event page and finds all 27 match URLs
5. Displays match list with types (RR/KO)

**Download Option**: Save Stage 1 JSON backup of match URLs

### Step 2: Scrape Match Results (Stage 1)
1. Click "Scrape Match Results (Stage 1)" button
2. System loops through all matches, extracting:
   - Player names
   - Scores
   - Winners
3. Real-time progress bar shows completion
4. Each match status updates: Pending → Scraping → Success/Failed
5. Summary shows matches scraped

**Output**: Match results stored in `matchResults` array

### Step 3: Scrape Match Details (Stage 2)
1. Click "Scrape Match Details (Stage 2)" button
2. System loops through matches again, extracting:
   - Detailed player statistics
   - Leg counts
   - Score breakdowns (100+, 120+, 140+, 160+, 180s)
   - Checkout percentages
   - Set information (for knockout)
3. Separate log window for Stage 2 progress
4. Summary shows details scraped

**Output**: Match details stored in `matchDetails` array

### Step 4: Review All Stats Before Sending
1. Merged data from Stage 1 + Stage 2 displayed in comprehensive table
2. Table shows:
   - Match number
   - Player names
   - 3-dart averages (highlighted)
   - Legs played
   - 180s count (gold highlight)
   - Highest checkout (green highlight)
   - Doubles percentage
   - Match result (color-coded)
   - Tournament phase badge
3. Summary statistics:
   - Total matches
   - Total players
   - Average 3-dart average across all players
4. Action buttons:
   - **Send to Admin Control Panel**: Submits to Supabase staging table
   - **Edit Stats**: Placeholder for future inline editing
   - **Discard All**: Clear data and start over

## Database Schema Updates

### Migration: 003_add_event_tracking.sql

#### New Columns in `staging_matches`
```sql
event_number INTEGER CHECK (event_number BETWEEN 1 AND 7)
player_1_100_plus INTEGER DEFAULT 0
player_1_120_plus INTEGER DEFAULT 0
player_1_140_plus INTEGER DEFAULT 0
player_1_160_plus INTEGER DEFAULT 0
player_2_100_plus INTEGER DEFAULT 0
player_2_120_plus INTEGER DEFAULT 0
player_2_140_plus INTEGER DEFAULT 0
player_2_160_plus INTEGER DEFAULT 0
player_1_doubles_hit INTEGER DEFAULT 0
player_1_doubles_attempted INTEGER DEFAULT 0
player_2_doubles_hit INTEGER DEFAULT 0
player_2_doubles_attempted INTEGER DEFAULT 0
is_knockout BOOLEAN DEFAULT FALSE
scrape_stage VARCHAR(20) CHECK (scrape_stage IN ('match_results', 'match_details', 'complete'))
```

#### New Columns in `matches` (Production)
Same columns as staging (except `scrape_stage`)

#### New Indexes
```sql
idx_staging_matches_event_number
idx_matches_event_number
idx_staging_matches_scrape_stage
```

#### Updated View: `event_standings`
Now includes `event_number` column for filtering by specific event

## API Endpoints

### POST /api/scrape_event
Find all match URLs from an event page

**Request**:
```json
{
  "event_url": "https://tv.dartconnect.com/eventmenu/mt_joe6163l_1",
  "event_number": 1
}
```

**Response**:
```json
{
  "success": true,
  "event_id": "mt_joe6163l_1",
  "event_number": 1,
  "matches": [...],
  "progress_log": [...]
}
```

### POST /api/scrape_match_result
Stage 1: Scrape basic match result

**Request**:
```json
{
  "recap_url": "https://tv.dartconnect.com/history/...",
  "event_id": "mt_joe6163l_1",
  "event_number": 1,
  "match_index": 0
}
```

**Response**:
```json
{
  "success": true,
  "player1": "John Doe",
  "player2": "Jane Smith",
  "score": "3-2",
  "winner": "John Doe",
  "phase": "final",
  "group": null,
  "players_added": 2
}
```

### POST /api/scrape_match_details
Stage 2: Scrape detailed statistics

**Request**:
```json
{
  "recap_url": "https://tv.dartconnect.com/history/...",
  "event_id": "mt_joe6163l_1",
  "event_number": 1,
  "match_number": 1,
  "phase": "final"
}
```

**Response**:
```json
{
  "success": true,
  "players": [
    {
      "player_name": "John Doe",
      "three_dart_average": 85.42,
      "legs_played": 5,
      "count_100_plus": 12,
      "count_120_plus": 8,
      "count_140_plus": 5,
      "count_160_plus": 2,
      "count_180s": 3,
      "highest_checkout": 121,
      "doubles_hit": 5,
      "doubles_attempted": 12,
      "match_won": true
    },
    {...}
  ],
  "is_knockout": true,
  "sets_played": 3,
  "match_number": 1
}
```

### POST /api/send_to_admin
Send complete scraped data to Supabase staging table

**Request**:
```json
{
  "event_number": 1,
  "event_id": "mt_joe6163l_1",
  "matches": [...],
  "total_matches": 27,
  "total_players": 54,
  "timestamp": "2025-12-22T17:00:00.000Z"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Event 1 data sent to staging",
  "matches_processed": 27,
  "event_number": 1
}
```

## Admin Control Panel Integration

### Staging Table View
The admin panel now displays:
- Event number (e.g., "Event 1", "Event 2")
- Match phase (Final, Semifinal, etc.)
- Player names (inline editable)
- Scores (inline editable)
- Averages
- Status badges
- Approve/Reject buttons

### Event Filtering
Admins can filter staging matches by:
- Event number (1-6)
- Phase (Round Robin, Knockout)
- Status (Pending, Approved, Rejected)
- Date range

### Data Review Workflow
1. **Scraper** sends data to `staging_matches` table with `event_number`
2. **Admin Panel** loads staging data, grouped by event
3. **Admin** reviews and edits any incorrect data (inline editing)
4. **Admin** approves match → Data moves to production `matches` table
5. **Public Display** reads from production `matches` table, filtered by event

## File Structure
```
AADSSTATSV2/
├── Event-Scraper-StandAlone/
│   ├── api_server.py                 # Flask API with new endpoints
│   ├── event_scraper.html            # 4-step UI with event selection
│   ├── src/
│   │   ├── scraper.py                # Enhanced with Stage 1/2 methods
│   │   ├── event_data_manager.py     # Event data persistence
│   │   └── database_manager.py       # Database operations
│   └── data/
│       └── event_data/               # JSON/CSV backups per event
│
├── aads-stats-v2/
│   ├── admin/
│   │   └── control-panel.html        # Admin dashboard (event-aware)
│   ├── public/
│   │   └── index.html                # Public stats display
│   └── supabase/
│       └── migrations/
│           ├── 001_create_schema.sql
│           ├── 002_rls_policies.sql
│           └── 003_add_event_tracking.sql  # NEW: Event columns
│
└── README.md
```

## Usage Example

### Scraping Event 2
```bash
# 1. Start the API server
cd Event-Scraper-StandAlone
python api_server.py

# 2. Open browser to http://localhost:5000
# 3. Select "Event 2" from dropdown
# 4. Enter DartConnect URL
# 5. Click "Find Matches" → Wait for 27 matches
# 6. Click "Scrape Match Results (Stage 1)" → Wait ~5-10 seconds
# 7. Click "Scrape Match Details (Stage 2)" → Wait ~10-20 seconds
# 8. Review stats table
# 9. Click "Send to Admin Control Panel"

# 10. Open Admin Panel at http://localhost:8001/admin/control-panel.html
# 11. Login with admin credentials
# 12. Review Event 2 matches in staging table
# 13. Edit any incorrect data (click cells)
# 14. Click "Approve" for each match
# 15. Data now visible on public display
```

## Benefits of Two-Stage Approach

### 1. Speed
- Stage 1 completes in ~5 seconds for 27 matches
- Users see match results immediately
- Stage 2 runs in background if needed

### 2. Reliability
- If Stage 2 fails, Stage 1 data is preserved
- Can retry detailed scraping without losing results
- Incremental progress saves

### 3. Flexibility
- Can scrape results now, details later
- Different scraping logic per stage
- Easier to debug and maintain

### 4. Data Quality
- Two review checkpoints: scraper preview + admin panel
- Separate basic vs detailed data
- Easier to identify scraping issues

## Next Steps

### Immediate
- [x] Event selection dropdown (1-6)
- [x] Two-stage scraping UI
- [x] Database migration for event tracking
- [x] API endpoints for staged scraping
- [x] Admin panel event display

### Short-Term
- [ ] Run migration 003 in Supabase
- [ ] Test full workflow with real event
- [ ] Add inline editing in scraper preview table
- [ ] Implement Event 7 (Tournament of Champions) logic

### Long-Term
- [ ] Auto-detect match format (set play vs legs)
- [ ] Bulk approve/reject in admin panel
- [ ] Event comparison views
- [ ] Export event statistics to CSV/PDF
- [ ] Player performance tracking across events

## Technical Notes

### Match Index Classification
The system uses match position to determine phase/group:
- Match 1: Final
- Matches 2-3: Semifinals
- Matches 4-7: Quarterfinals
- Matches 8-17: Group A Round Robin
- Matches 18-27: Group B Round Robin

### Set Play Detection
For knockout matches:
- System looks for "Set 1", "Set 2", etc. headers
- Extracts total sets played
- Stores in `sets_played` column

### Doubles Percentage Calculation
```javascript
doublesPercent = (doublesHit / doublesAttempted) * 100
```

### Round Robin vs Knockout
- **Round Robin**: `is_knockout = FALSE`, `sets_played = 0`
- **Knockout**: `is_knockout = TRUE`, `sets_played = N`

---

**Last Updated**: December 22, 2025  
**Version**: 2.0  
**Author**: AADS Development Team
