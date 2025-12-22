# AADS Stats V2 - Complete User Guide

**Step-by-Step Instructions for Event Management**

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Event Scraping Workflow](#event-scraping-workflow)
3. [Admin Review Process](#admin-review-process)
4. [Public Display Management](#public-display-management)
5. [Advanced Features](#advanced-features)
6. [Troubleshooting](#troubleshooting)

---

## Getting Started

### First-Time Setup

#### 1. Install Event Scraper

```bash
# Navigate to scraper directory
cd Event-Scraper-StandAlone

# Install Python dependencies
pip install -r requirements.txt

# Start the server
python api_server.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

#### 2. Configure Supabase

Open `aads-stats-v2/.env` and add your credentials:
```
SUPABASE_URL=https://yppxkvbmffcvdxuswsbf.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
```

Update these same values in:
- `aads-stats-v2/admin/control-panel.html` (line 49-50)
- `aads-stats-v2/public/index.html` (line 24-25)

#### 3. Create Admin User

In Supabase SQL Editor:
```sql
INSERT INTO admin_users (email, role, is_active)
VALUES ('your-email@example.com', 'super_admin', true);
```

---

## Event Scraping Workflow

### Overview: 4-Step Process

The event scraper uses a **two-stage scraping workflow** that separates match results from detailed statistics for faster, more reliable data extraction.

**Time Estimates:**
- Stage 1 (Match Results): 5-10 seconds per match
- Stage 2 (Match Details): 10-20 seconds per match
- Total: ~6-8 minutes for 27 matches

---

### Step 1: Select Event & Find Matches

![Step 1](docs/images/step1-screenshot.png)

1. **Open Event Scraper**: http://localhost:5000

2. **Select Event Number** (dropdown):
   - Event 1
   - Event 2
   - Event 3
   - Event 4
   - Event 5
   - Event 6
   - *Event 7 (Tournament of Champions) - Coming Soon*

3. **Enter DartConnect Event URL**:
   ```
   Example: https://www.dartconnect.com/history/event/eventid/mt_joe6163l_1
   ```

4. **Click "Find Matches"**

**Expected Result:**
```
✓ Found 27 matches:
  - 1 Final
  - 2 Semifinals  
  - 4 Quarterfinals
  - 10 Group A Round Robin
  - 10 Group B Round Robin
```

**Progress Bar**: Green bar fills as matches are discovered.

---

### Step 2: Scrape Match Results (Stage 1)

![Step 2](docs/images/step2-screenshot.png)

This stage extracts **basic match information only**:
- Player 1 name
- Player 2 name
- Winner
- Score (legs/sets)
- Match phase (Final, SF, QF, Round Robin)
- Group assignment (A or B for Round Robin)

**Why Stage 1 is Fast:**
- No detailed stats extraction
- Simple DOM parsing
- Minimal wait times
- 5-10 seconds per match

**Instructions:**

1. **Click "Scrape Match Results (Stage 1)"**

2. **Watch Progress**:
   - Progress bar updates per match
   - Status shows: "Scraping match 1 of 27..."
   - ETA displayed

3. **Review Results Table** (appears automatically):
   - Match number
   - Player names
   - Scores
   - Winners
   - Phase/Group

**What You'll See:**
```
Match 1:  John Smith vs Jane Doe → John Smith (5-3) - Final
Match 2:  Bob Jones vs Mary White → Bob Jones (3-1) - Semifinal
Match 3:  ... (and so on for all 27 matches)
```

**Troubleshooting:**
- ❌ "Match not found" → DartConnect URL may be wrong
- ❌ "Timeout" → Slow internet, try again
- ✓ "Success" → Proceed to Stage 2

---

### Step 3: Scrape Match Details (Stage 2)

![Step 3](docs/images/step3-screenshot.png)

This stage extracts **detailed statistics**:
- 3-Dart Average
- Legs won (per player)
- Highest checkout
- 100+ scores
- 120+ scores  
- 140+ scores
- 160+ scores
- 180s
- Doubles hit/attempted

**Why Stage 2 is Slower:**
- Complex stat parsing
- Multiple data tables
- JavaScript-heavy pages
- 10-20 seconds per match

**Match Type Detection:**

The scraper automatically detects match format:

**Round Robin** (Best of 5 Legs):
- No set structure
- First to 3 legs wins
- Matches 8-27 (Groups A & B)

**Knockout** (Set Play):
- Multiple sets
- Legs within each set
- Matches 1-7 (Finals, SF, QF)

**Instructions:**

1. **Click "Scrape Match Details (Stage 2)"**

2. **Watch Progress**:
   - Progress bar updates per match
   - Status shows: "Scraping details for match 1 of 27..."
   - Significantly slower than Stage 1 (this is normal)

3. **Review Comprehensive Stats Table** (appears automatically):
   - All Stage 1 data PLUS
   - 3-Dart averages
   - 180s counts
   - Highest checkouts
   - Doubles percentages
   - Legs breakdown

**What You'll See:**
```
Match 1: John Smith (92.34 avg, 5 legs, 4x180s) vs Jane Doe (88.12 avg, 3 legs, 2x180s)
Match 2: Bob Jones (85.67 avg, 3 sets) vs Mary White (82.45 avg, 1 set)
```

**Troubleshooting:**
- ⚠️ "Partial data" → Some stats missing (DartConnect issue)
- ❌ "Failed" → Click "Retry" button
- ✓ "Complete" → All 27 matches scraped successfully

---

### Step 4: Review All Stats

![Step 4](docs/images/step4-screenshot.png)

Before sending to admin panel, **verify data accuracy**.

**Comprehensive Stats Table Columns:**
1. **Match #** - Sequential number (1-27)
2. **Player 1/2** - Names
3. **Score** - Legs or Sets (format auto-detected)
4. **Winner** - Winning player name
5. **3DA** - 3-Dart Average (both players)
6. **Legs** - Legs won (both players)
7. **180s** - Maximum score counts
8. **Hi CO** - Highest checkout
9. **Doubles** - Hit/Attempted ratio
10. **Phase** - Tournament stage
11. **Group** - A or B (Round Robin only)

**Manual Edits:**

Click any cell to edit:
- Fix typos in names
- Correct miscalculated averages
- Update checkout values

**Actions:**

- ✏️ **Edit**: Click cell, type new value, press Enter
- 🗑️ **Delete**: Remove individual matches
- 🔄 **Retry**: Re-scrape failed matches
- ✅ **Send to Admin**: Submit all data for review

**Click "Send to Admin Control Panel"**

**Expected Result:**
```
✓ Successfully sent 27 matches to admin panel
✓ Data available at: http://localhost:8001/admin/control-panel.html
```

---

## Admin Review Process

### Accessing Admin Panel

1. **Open Admin Panel**: http://localhost:8001/admin/control-panel.html

2. **Login** with admin credentials (configured in Supabase)

3. **Dashboard Overview**:
   - Total staging matches
   - Event breakdown
   - Recent activity

---

### Review Workflow

#### 1. View Staging Matches

**Filter by Event:**
- Dropdown: "All Events" or specific event (1-6)
- Click "Filter" to apply

**Staging Table Columns:**
- Event #
- Match Phase
- Player Names
- Score
- 3-Dart Average
- 180s
- Highest Checkout
- Doubles %

#### 2. Inline Editing

**Click any cell to edit:**

**Example: Fix Player Name**
1. Click "John Smit" (typo)
2. Type "John Smith"
3. Press Enter
4. Changes saved automatically

**Example: Correct Average**
1. Click "92.34"
2. Type "93.45"
3. Press Enter
4. Recalculates standings

**Editable Fields:**
- Player 1/2 names
- Scores (legs/sets)
- 3-Dart averages
- 100+/120+/140+/160+/180s counts
- Highest checkouts
- Doubles hit/attempted

**Auto-Save:**
- ✓ Changes saved to staging_matches table
- ✓ Does NOT affect production yet
- ✓ Can edit multiple times

#### 3. Approval Actions

**Approve Match:**
1. Click "✓ Approve" button
2. Confirmation: "Move to production?"
3. Match deleted from staging
4. Match inserted into matches table
5. Public display updates automatically

**Reject Match:**
1. Click "✗ Reject" button
2. Confirmation: "Delete this match?"
3. Match deleted from staging
4. Does NOT go to production

**Bulk Actions:**
1. Select multiple matches (checkbox)
2. Click "Approve Selected" or "Reject Selected"
3. Confirm bulk action

---

### Best Practices

**✅ DO:**
- Review ALL matches before approving
- Check for duplicate player names (typos)
- Verify averages are reasonable (60-100 range)
- Confirm 180s counts match video footage
- Double-check knockout vs round robin format

**❌ DON'T:**
- Approve matches with obvious errors
- Skip verification steps
- Delete matches without reason
- Edit production data directly (use staging)

---

## Public Display Management

### Viewing Public Stats

1. **Open Public Display**: `aads-stats-v2/public/index.html`

2. **Navigation Menu**:
   - **Home** - Hero banner
   - **Standings** - Series leaderboard
   - **Events** - Event-specific standings
   - **Champions** - Past winners
   - **Statistics** - Records & achievements
   - **Players** - Search directory

---

### Sections Explained

#### Series Leaderboard

**Displays:**
- Player rank
- Total points (calculated from event placements)
- Events played
- Best finish
- Win %

**Calculation:**
```
Points = Sum of placement points across all events
- 1st: 100 points
- 2nd: 75 points
- 3rd-4th: 50 points
- 5th-8th: 25 points
- 9th-16th: 10 points
```

#### Event Standings

**Displays:**
- Event-specific group standings (A & B)
- Wins / Losses
- Legs for / against
- Point differential
- Head-to-head records

**Group Stage Rules:**
- 10 matches per group (5 players each)
- Round robin format (everyone plays everyone)
- Top 2 from each group advance to knockouts

#### Knockout Brackets

**Displays:**
- Tournament bracket (Final, SF, QF)
- Match results
- Player paths through bracket

**Visual:**
```
        FINAL
    ┌─────┴─────┐
   SF1         SF2
  ┌─┴─┐      ┌─┴─┐
 QF1 QF2    QF3 QF4
```

#### Statistics Dashboard

**Leaderboards:**
- Highest 3-Dart Average (minimum 5 matches)
- Most 180s (single match)
- Highest Checkout (verified)
- Best Doubles % (minimum 10 attempts)

**Filters:**
- All events vs single event
- Knockout vs round robin
- Date range

---

### Updating Public Display

**Automatic Updates:**

When you approve matches in admin panel:
1. Data moves to `matches` table
2. Supabase triggers recalculate views
3. `event_standings` view updates
4. `series_leaderboard` view updates
5. Public display fetches new data (on refresh)

**Manual Refresh:**

If public display doesn't update:
1. Open browser console (F12)
2. Clear cache (Ctrl+Shift+Delete)
3. Hard reload (Ctrl+Shift+R)

**GitHub Pages Deployment:**

Push changes to trigger auto-deploy:
```bash
git add .
git commit -m "Update stats"
git push origin main
```

Live site updates in 1-2 minutes: https://dowdarts.github.io/AADSSTATSV2/

---

## Advanced Features

### Event Management

#### Creating New Event

In Supabase SQL Editor:
```sql
INSERT INTO events (event_number, name, date, venue, status)
VALUES (7, 'Tournament of Champions', '2025-01-15', 'TD Convention Center', 'upcoming');
```

#### Updating Event Status

```sql
UPDATE events
SET status = 'in_progress'
WHERE event_number = 1;
```

#### Archiving Event

```sql
UPDATE events
SET status = 'completed'
WHERE event_number = 1;
```

---

### Player Management

#### Adding New Player

```sql
INSERT INTO players (name, email, phone, skill_level)
VALUES ('John Smith', 'john@example.com', '555-1234', 'intermediate');
```

#### Merging Duplicate Players

1. Find duplicates:
```sql
SELECT * FROM players WHERE name ILIKE '%john smith%';
```

2. Update matches to use correct player_id:
```sql
UPDATE matches
SET player_1_id = 123  -- correct ID
WHERE player_1_id = 456;  -- duplicate ID
```

3. Delete duplicate:
```sql
DELETE FROM players WHERE id = 456;
```

---

### Data Export

#### Export Event Results (CSV)

```sql
COPY (
  SELECT * FROM matches WHERE event_number = 1
) TO '/tmp/event1_results.csv' WITH CSV HEADER;
```

#### Export Leaderboard

```sql
COPY (
  SELECT * FROM series_leaderboard ORDER BY rank
) TO '/tmp/leaderboard.csv' WITH CSV HEADER;
```

---

### Backup & Restore

#### Backup Staging Data

```bash
cd Event-Scraper-StandAlone/data/event_data
# JSON backups created automatically during scraping
# Files: matches_YYYYMMDD_HHMMSS.json
```

#### Restore from Backup

```bash
python scripts/data_migration.py restore \
  --file data/event_data/mt_joe6163l_1/matches_20251222_164421.json \
  --event 1
```

---

## Troubleshooting

### Common Issues

#### Issue: Scraper Won't Start

**Symptoms:**
- `python api_server.py` fails
- "Module not found" errors

**Solutions:**
```bash
# Check Python version
python --version  # Must be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Use virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

#### Issue: Selenium TimeoutException

**Symptoms:**
- "Timeout waiting for page to load"
- Matches fail to scrape

**Solutions:**
```bash
# Update ChromeDriver
pip install webdriver-manager --upgrade

# Increase timeout in scraper.py:
# Change TIMEOUT = 30 to TIMEOUT = 60
```

---

#### Issue: Missing Stats (Partial Data)

**Symptoms:**
- 180s showing as 0 when you know there were some
- Averages blank
- Checkouts missing

**Cause:** DartConnect page didn't fully load

**Solutions:**
1. Click "Retry" for that specific match
2. Manually enter stats in Step 4 review table
3. Edit in admin panel after sending

---

#### Issue: Admin Panel Login Fails

**Symptoms:**
- "Not authorized" error
- Can't access staging table

**Solutions:**
```sql
-- Check if admin user exists
SELECT * FROM admin_users WHERE email = 'your-email@example.com';

-- Create admin if missing
INSERT INTO admin_users (email, role, is_active)
VALUES ('your-email@example.com', 'super_admin', true);

-- Verify RLS policy
SELECT * FROM pg_policies WHERE tablename = 'staging_matches';
```

---

#### Issue: Public Display Shows Old Data

**Symptoms:**
- Approved matches don't appear
- Leaderboard not updating

**Solutions:**
```sql
-- Refresh materialized views (if you have any)
REFRESH MATERIALIZED VIEW series_leaderboard;

-- Check matches table
SELECT COUNT(*) FROM matches WHERE event_number = 1;

-- Verify triggers are active
SELECT * FROM pg_trigger WHERE tgname LIKE '%event%';
```

```javascript
// Clear browser cache
// Chrome: Ctrl+Shift+Delete → Clear cache
// Hard reload: Ctrl+Shift+R
```

---

#### Issue: Duplicate Matches in Staging

**Symptoms:**
- Same match appears multiple times
- Scraped same event twice

**Solutions:**
```sql
-- Find duplicates
SELECT match_url, COUNT(*) 
FROM staging_matches 
GROUP BY match_url 
HAVING COUNT(*) > 1;

-- Delete duplicates (keep latest)
DELETE FROM staging_matches
WHERE id NOT IN (
  SELECT MAX(id)
  FROM staging_matches
  GROUP BY match_url
);
```

---

### Getting Help

**Check Logs:**

Event Scraper:
```bash
# Terminal where you ran python api_server.py
# Errors appear in console
```

Supabase:
```sql
-- Check recent errors
SELECT * FROM logs ORDER BY created_at DESC LIMIT 10;
```

Browser Console:
```
F12 → Console tab
Look for red error messages
```

**Contact Support:**
- GitHub Issues: https://github.com/dowdarts/AADSSTATSV2/issues
- Email: admin@aadsstats.com

---

## Workflow Cheat Sheet

### Quick Reference

**1. Scrape Event (5-10 min)**
```
localhost:5000 → Select Event → Enter URL → Find Matches → 
Scrape Results → Scrape Details → Review → Send to Admin
```

**2. Admin Review (2-5 min)**
```
localhost:8001/admin/control-panel.html → Filter Event → 
Review Data → Edit Errors → Approve All
```

**3. Publish (Automatic)**
```
Approved matches → Production DB → Public display updates
```

**4. Deploy (If needed)**
```
git add . → git commit → git push → GitHub Pages deploys
```

---

## Keyboard Shortcuts

**Event Scraper:**
- `Ctrl+Enter` - Start scraping
- `Esc` - Cancel scraping

**Admin Panel:**
- `Enter` - Save inline edit
- `Esc` - Cancel inline edit
- `Ctrl+A` - Select all matches
- `Delete` - Reject selected

**Public Display:**
- `/` - Focus search
- `Esc` - Clear search

---

## Best Practices Summary

✅ **Always scrape in order**: Stage 1 → Stage 2
✅ **Review before sending**: Check Step 4 table
✅ **Edit in admin panel**: Don't skip review
✅ **Backup regularly**: JSON files in data/event_data/
✅ **Test on local**: Before pushing to GitHub Pages
✅ **Keep Supabase updated**: Run migrations when available

---

**Last Updated**: December 22, 2025  
**Version**: 2.0.0
