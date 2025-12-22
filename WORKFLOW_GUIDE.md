# AADS Event Scraper - Complete Workflow Guide

## 🎯 Overview

The AADS Event Scraper now features a complete workflow with:
- **Group standings tables** displayed after Stage 1
- **Download functionality** to save data locally (Stage 1 & 2)
- **Push to Admin** to send data directly to admin panel
- **Admin upload** to manually import downloaded files

---

## 📋 Complete Workflow

### Step 1: Start the Server
```
Double-click: START-SERVER-DESKTOP.bat
```
- Opens green terminal window
- Runs Flask API server at `localhost:5000`
- Leave this window open while scraping

### Step 2: Open Event Scraper
```
Double-click: 2-EVENT-SCRAPER.bat
```
- Opens `http://localhost:5000` in your browser

### Step 3: Scrape Event Matches (Stage 1)
1. **Select Event Number** (e.g., Event 1)
2. **Enter DartConnect URL** (e.g., `https://www.dartconnect.com/...`)
3. **Click "Find Matches"** - Wait for success message
4. **Click "Scrape Match Results (Stage 1)"** - 5-10 seconds

### Step 4: Review Group Standings
After Stage 1 completes, you'll see:

#### **Group A Standings Table**
| Pos | Player | P | W | L | LF | LA | +/- |
|-----|--------|---|---|---|----|----|-----|
| 1   | Player1| 5 | 4 | 1 | 25 | 18 | +7  |
| 2   | Player2| 5 | 3 | 2 | 23 | 20 | +3  |

#### **Group B Standings Table**
| Pos | Player | P | W | L | LF | LA | +/- |
|-----|--------|---|---|---|----|----|-----|
| 1   | Player1| 5 | 5 | 0 | 27 | 15 | +12 |
| 2   | Player2| 5 | 4 | 1 | 25 | 17 | +8  |

**Legend:**
- **P** = Played
- **W** = Wins
- **L** = Losses
- **LF** = Legs For
- **LA** = Legs Against
- **+/-** = Leg Difference

### Step 5: Stage 1 Actions (Choose One)

#### Option A: Download Stage 1 Results
1. **Click "Download Stage 1 Results"**
2. Saves file: `event1_stage1_2025-12-22.json`
3. Contains: Match results, scores, winners, groups

#### Option B: Push Stage 1 to Admin
1. **Click "Push Stage 1 to Admin"**
2. Data sent directly to admin panel
3. Saved in `data/pending_review/` folder
4. No download required

### Step 6: Scrape Match Details (Stage 2)
1. **Click "Scrape Match Details (Stage 2)"** - 10-20 seconds
2. Extracts detailed stats:
   - 3-Dart Average
   - Legs played
   - 100+/120+/140+/160+/180s
   - Highest checkout
   - Doubles hit/missed

### Step 7: Stage 2 Actions (Choose One)

#### Option A: Download Stage 2 Details
1. **Click "Download Stage 2 Details"**
2. Saves file: `event1_stage2_2025-12-22.json`
3. Contains: Full match statistics

#### Option B: Push Stage 2 to Admin
1. **Click "Push Stage 2 to Admin"**
2. Complete stats sent to admin panel
3. Ready for final review

---

## 🎛️ Admin Control Panel Workflow

### Open Admin Panel
```
Double-click: 3-ADMIN-PANEL.bat
```

### Option 1: Review Pushed Data
1. Data automatically appears in **Staging Queue** tab
2. Review matches one by one
3. **Approve** or **Reject** each match
4. Approved matches publish to public display

### Option 2: Upload Downloaded Files
1. Go to **Upload Data** tab
2. **Stage 1 Upload:**
   - Click "Choose Stage 1 JSON File"
   - Select downloaded `event1_stage1_*.json`
   - Preview shows summary
   - Click "Publish to Staging"
   - Data moves to Staging Queue for review

3. **Stage 2 Upload:**
   - Click "Choose Stage 2 JSON File"
   - Select downloaded `event1_stage2_*.json`
   - Preview shows stats summary
   - Click "Publish to Production"
   - Full stats published (after implementation)

---

## 📁 File Locations

### Downloaded Files (if using Download option)
- Saved to: `Downloads/` folder
- Format: `eventN_stageX_YYYY-MM-DD.json`

### Pushed Files (if using Push option)
- Saved to: `Event-Scraper-StandAlone/data/pending_review/`
- Format: `eventN_stageX_YYYYMMDD_HHMMSS.json`

### Event Data (auto-saved during scraping)
- Location: `Event-Scraper-StandAlone/data/event_data/`
- Structure:
  ```
  event_data/
  ├── mt_joe6163l_1/
  │   ├── metadata.json
  │   ├── match_urls.txt
  │   ├── csv/
  │   │   └── matches_20251222.csv
  │   └── raw_data/
  │       └── matches_20251222.json
  ```

---

## 🔄 Recommended Workflows

### Workflow A: Quick Push (No Downloads)
1. Start Server → Open Scraper
2. Stage 1 Scrape → Review Standings
3. **Push Stage 1 to Admin**
4. Stage 2 Scrape
5. **Push Stage 2 to Admin**
6. Open Admin Panel → Review → Publish

**Best for:** Fast workflow, no file management

### Workflow B: Download & Review (Backup Files)
1. Start Server → Open Scraper
2. Stage 1 Scrape → Review Standings
3. **Download Stage 1 Results** (backup)
4. Stage 2 Scrape
5. **Download Stage 2 Details** (backup)
6. Open Admin Panel → Upload Tab
7. Upload Stage 1 → Publish to Staging
8. Review in Staging Queue → Approve
9. Upload Stage 2 → Publish to Production

**Best for:** Keep backup copies, review offline before upload

### Workflow C: Mixed (Push Stage 1, Download Stage 2)
1. Start Server → Open Scraper
2. Stage 1 Scrape → Review Standings
3. **Push Stage 1 to Admin**
4. Review in Admin Panel → Approve
5. Stage 2 Scrape
6. **Download Stage 2 Details** (backup before publish)
7. Admin Panel → Upload Stage 2 → Publish

**Best for:** Quick initial publish, careful final stats review

---

## 📊 Data Flow Diagram

```
┌─────────────────┐
│ Event Scraper   │
│                 │
│ Stage 1 → ✓ ←───┼── Group Standings Display
│           │     │
│           ├─────┼── Download JSON (Option A)
│           │     │
│           └─────┼── Push to Admin (Option B)
│                 │
│ Stage 2 → ✓     │
│           │     │
│           ├─────┼── Download JSON (Option A)
│           │     │
│           └─────┼── Push to Admin (Option B)
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ Admin Panel     │
│                 │
│ Staging Queue ◄─┼── From Push
│                 │
│ Upload Tab    ◄─┼── From Downloaded Files
│                 │
│ Review → Approve│
│           │     │
│           ▼     │
│    ┌──────────┐ │
│    │Production│ │
│    │ Tables   │ │
│    └──────────┘ │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ Public Display  │
│ (Stats Viewer)  │
└─────────────────┘
```

---

## ✅ Verification Steps

### After Stage 1:
- [ ] Standings tables show all players
- [ ] Group A has 10 players (matches 8-17)
- [ ] Group B has 10 players (matches 18-27)
- [ ] Leg differences calculated correctly
- [ ] Players sorted by leg difference

### After Download:
- [ ] JSON file saved to Downloads
- [ ] File opens in text editor
- [ ] Contains all expected matches/stats

### After Push:
- [ ] Success message appears
- [ ] Green server terminal shows "Data pushed to admin panel"
- [ ] File created in `data/pending_review/`

### In Admin Panel:
- [ ] Data appears in correct tab
- [ ] Preview shows accurate summary
- [ ] Publish button works
- [ ] Staging queue updates

---

## 🚨 Troubleshooting

### Standings Don't Appear
- Ensure Stage 1 completed successfully (check logs)
- Refresh page and try again
- Check browser console (F12) for errors

### Download Not Working
- Check browser download settings
- Ensure popup blocker disabled
- Try different browser

### Push Fails
- Verify server is running (green terminal window)
- Check server terminal for error messages
- Ensure `data/` folder has write permissions

### Admin Panel Not Showing Data
- Refresh admin panel page
- Check Supabase connection
- Verify push/upload completed successfully

---

## 📝 Notes

1. **Always review standings** before proceeding to Stage 2
2. **Download files provide backups** in case of errors
3. **Push is faster** but download gives you control
4. **Admin upload allows offline review** before publishing
5. **Server must stay running** throughout scraping process

---

## 🎓 Tips

- **Use Push for speed:** During testing/development
- **Use Download for safety:** For important events
- **Review standings carefully:** Catches scraping errors early
- **Keep server terminal visible:** Monitor progress/errors
- **Save downloaded files:** Backup before experimenting

---

**Last Updated:** December 22, 2025
**Version:** 2.0.0 with Workflow Enhancements
