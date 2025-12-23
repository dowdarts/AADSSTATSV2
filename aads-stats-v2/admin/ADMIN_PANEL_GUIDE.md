# Admin Control Panel User Guide

## Overview
The AADS Admin Control Panel is a redesigned administrative interface that mirrors the public display app's appearance while adding powerful editing and management capabilities.

## Key Features

### 1. **Identical Visual Design**
- Matches the public display app exactly (dark theme, orange accents, same fonts and spacing)
- Seamless transition between admin and public views
- Professional broadcast-quality appearance

### 2. **Edit Mode Toggle**
- Click "Enable Edit Mode" button in header to activate inline editing
- When enabled, all editable fields show a ✏️ icon on hover
- Click any editable field to make changes in-place
- Changes save automatically to Supabase on blur or Enter key

### 3. **Seven Main Tabs**

#### 📊 Dashboard
- **Overview Stats**: Total Players, Total Matches, Total Events, Pending Reviews
- **Recent Activity**: Timeline of latest changes and uploads
- **Quick Status**: At-a-glance system health

#### 📤 Upload Data
- **Stage 1 Upload**: Upload JSON file with basic match results and group standings
  - Automatic preview of uploaded data
  - Shows event URL, match count, timestamp
  - Publish directly to Staging Queue
  
- **Stage 2 Upload**: Upload JSON file with detailed statistics
  - Player averages, 180s, checkouts, leg-by-leg data
  - Preview before publishing
  - Publish to Staging Queue for review

#### ⏳ Staging Queue
- **Review Pending Matches**: All uploaded matches await approval here
- **Inline Editing**: Edit any field before publishing
- **Batch Actions**:
  - ✓ Approve individual matches → moves to production
  - ✗ Reject individual matches → removes from queue
  - "Publish All to Production" → approve all at once
  - "Clear All" → remove all pending matches
- **Status Badges**: Visual indicators for pending/approved/published states

#### 🏆 Standings
- **Live Tournament Rankings**: Same view as public display
- **Editable Fields** (with Edit Mode on):
  - Player names
  - Points
  - Wins/Losses
  - 3DA averages
- **Actions**: Refresh, Export
- **Auto-sorts**: By points (highest first)

#### 👥 Players
- **Complete Player Database**: All registered players
- **Editable Stats**: Name, Points, Wins, Losses, 3DA
- **Actions**:
  - ➕ Add Player: Create new player profile
  - Delete: Remove player from database
  - 🔄 Refresh: Reload latest data

#### 🎯 Matches
- **All Published Matches**: Production match database
- **Editable Fields**: Player names, scores, winners
- **Match Details**: Phase (Final/Semifinals/etc.), Group (A/B)
- **Actions**: Add Match, Delete Match, Refresh

#### 📅 Events
- **Event Management**: Tournament and event listings
- **Editable**: Event name, date
- **Status Tracking**: Active/Completed/Upcoming
- **Actions**: Add Event, Delete Event, Refresh

## Workflow Guide

### Standard Upload → Review → Publish Workflow

1. **Scrape Event Data**
   - Use Event Scraper to scrape Stage 1 (basic results)
   - Scraper can "Download JSON" or "Push to Admin"

2. **Upload to Admin** (if downloaded)
   - Open Admin Panel → Upload Data tab
   - Click "Choose Stage 1 File"
   - Preview data in preview container
   - Click "Publish to Staging ✓"

3. **Review in Staging Queue**
   - Navigate to Staging Queue tab
   - Review all pending matches
   - Enable Edit Mode to correct any errors
   - Click ✓ to approve individual matches
   - OR click "Publish All to Production" for batch approval

4. **Verify in Production**
   - Check Standings, Players, or Matches tabs
   - Data now appears in production database
   - Changes immediately visible in public display app

5. **Optional: Manual Editing**
   - Enable Edit Mode (button in header)
   - Click any editable field in any tab
   - Make changes
   - Press Enter or click away to save
   - Changes push to Supabase instantly

### Direct Editing Workflow (No Upload Required)

1. **Enable Edit Mode**
   - Click "✏️ Enable Edit Mode" button in header
   - Button turns green: "✅ Edit Mode ON"
   - All editable fields now show ✏️ icon on hover

2. **Edit Any Field**
   - Click on player name, score, stat, etc.
   - Field converts to input box
   - Type new value
   - Press Enter or click away to save

3. **Verify Changes**
   - Field updates immediately in table
   - Changes save to Supabase database
   - Refresh public display app to see updates

## Field-by-Field Editing Reference

### Staging Queue
| Field | Editable | Notes |
|-------|----------|-------|
| ID | No | Auto-generated |
| Player 1 | Yes | Player name |
| Player 2 | Yes | Player name |
| Score | Yes | Format: "3-2", "3-1", etc. |
| Winner | Yes | Winning player name |
| Phase | No | Determined by match index |
| Group | No | A or B for round robin |
| Status | No | Visual indicator only |

### Standings
| Field | Editable | Notes |
|-------|----------|-------|
| Rank | No | Auto-calculated from points |
| Player | Yes | Player name |
| Points | Yes | Tournament points |
| Wins | Yes | Match wins |
| Losses | Yes | Match losses |
| 3DA | Yes | Three-dart average |

### Players
| Field | Editable | Notes |
|-------|----------|-------|
| ID | No | Auto-generated |
| Name | Yes | Full player name |
| Points | Yes | Tournament points |
| Wins | Yes | Total wins |
| Losses | Yes | Total losses |
| 3DA | Yes | Average (e.g., "65.43") |

### Matches
| Field | Editable | Notes |
|-------|----------|-------|
| ID | No | Auto-generated |
| Player 1 | Yes | First player name |
| Player 2 | Yes | Second player name |
| Score | Yes | Match score (e.g., "3-2") |
| Winner | Yes | Winning player |
| Phase | No | Bracket phase |
| Group | No | Round robin group |

### Events
| Field | Editable | Notes |
|-------|----------|-------|
| ID | No | Auto-generated |
| Name | Yes | Event title |
| Date | Yes | Event date |
| Status | No | Display only |

## Technical Details

### Database Tables
- **staging_matches**: Temporary holding for uploaded/scraped data awaiting approval
- **matches**: Production match results (published)
- **players**: Player profiles and statistics
- **events**: Tournament and event metadata

### Data Flow
```
Scraper → JSON Download → Admin Upload → Staging Queue → Approve → Production → Display App
                    OR
Scraper → Push API → Staging Queue → Approve → Production → Display App
                    OR
Admin Panel Edit Mode → Direct Edit → Production → Display App
```

### Styling Variables
```css
--primary-orange: #FF6B00   /* Main accent color */
--dark-bg: #0a0a0a          /* Background */
--card-bg: #1a1a1a          /* Card backgrounds */
--text-primary: #ffffff     /* Main text */
--text-secondary: #b0b0b0   /* Subdued text */
--success-green: #00ff88    /* Success indicators */
--danger-red: #ff4444       /* Delete/reject */
--warning-yellow: #ffd700   /* Pending status */
--accent-blue: #4a9eff      /* Published status */
```

## Troubleshooting

### Issue: Changes not saving
**Solution**: 
- Ensure Edit Mode is enabled (button should be green)
- Check browser console for errors
- Verify Supabase connection is active

### Issue: Old data displaying after refresh
**Solution**:
- Hard refresh browser: `Ctrl + F5` (Windows) or `Cmd + Shift + R` (Mac)
- Clear browser cache
- Use `3-ADMIN-PANEL-NOCACHE.bat` to open with cache disabled

### Issue: Can't see uploaded data in staging
**Solution**:
- Check preview container shows data before clicking "Publish to Staging"
- Refresh Staging Queue tab
- Check browser console for upload errors

### Issue: Display app not showing new data
**Solution**:
- Verify data was approved and published from Staging Queue
- Check that matches appear in Matches tab
- Refresh display app (auto-refreshes every 30 seconds)
- Verify Supabase connection in display app

### Issue: Duplicate players or matches
**Solution**:
- Enable Edit Mode
- Go to Players or Matches tab
- Delete duplicate entries using Delete button
- Consider data validation before uploading

## Best Practices

1. **Always Review in Staging First**
   - Don't publish directly to production without review
   - Use Staging Queue to catch errors before they go live

2. **Use Edit Mode Sparingly on Production Data**
   - Prefer editing in Staging Queue before approval
   - Document manual edits for audit trail

3. **Regular Backups**
   - Export data periodically
   - Keep JSON backups of scraped data

4. **Consistent Naming**
   - Use full player names consistently
   - Maintain same score format (e.g., "3-2" not "3 - 2")

5. **Test Changes in Display App**
   - After publishing, verify display app shows correctly
   - Check formatting, rankings, and calculations

6. **Clear Cache When Needed**
   - Use no-cache batch file for admin panel
   - Hard refresh display app after major changes

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Save edit | `Enter` |
| Cancel edit | `Escape` |
| Hard refresh | `Ctrl + F5` |
| Open DevTools | `F12` |
| Clear cache | `Ctrl + Shift + Delete` |

## Security Notes

- Admin panel requires authentication (logout button in header)
- Supabase RLS (Row Level Security) controls data access
- Edit Mode is client-side toggle for UX (server validates all writes)
- Never share Supabase credentials
- Use admin account only on trusted devices

## Future Enhancements

Planned features:
- Audit log of all edits
- Bulk import/export CSV
- Undo/redo for edits
- Real-time collaboration (multiple admins)
- Advanced filtering and search
- Custom player stats calculations
- Tournament bracket visualization

---

For technical support or feature requests, contact the development team.
