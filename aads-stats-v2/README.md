# AADS Stats Engine V2 - Setup Guide

## 📋 Overview

The AADS Stats Engine V2 is a professional statistics platform for the Atlantic Amateur Darts Series. It features:

- ✅ **Staging Control Panel** (Localhost Only) - Review and approve scraped data before publishing
- 🎯 **Public Frontend** (GitHub Pages) - Live stats display at https://dowdarts.github.io/AADSSTATSV2/
- 🔒 **Secure Backend** - Supabase with Row Level Security
- 📊 **Advanced Tournament Logic** - Ranking algorithms, seeding, bracket generation
- 🔄 **Data Migration** - Seamless flow from scraper to production

## 🌐 Deployment Architecture

### **Admin Control Panel** - Localhost Only ❌
- **URL**: `http://localhost:8001`
- **Purpose**: Review and approve scraped data
- **Security**: NEVER deploy publicly

### **Event Scraper** - Localhost Only ❌
- **URL**: `http://localhost:5000`
- **Purpose**: Scrape event data and send to staging
- **Security**: NEVER deploy publicly

### **Public Display** - GitHub Pages ✅
- **URL**: https://dowdarts.github.io/AADSSTATSV2/
- **Purpose**: Public statistics display
- **Embedding**: Safe to embed on aadsdarts.com

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete deployment instructions.

## 🚀 Quick Start

### Prerequisites

1. **Supabase Account** - [Sign up at supabase.com](https://supabase.com)
2. **Python 3.8+** - For data migration scripts
3. **Modern Web Browser** - For admin panel and public frontend

### Step 1: Set Up Supabase

#### 1.1 Create a New Supabase Project

1. Go to [supabase.com](https://supabase.com) and create a new project
2. Note your project URL and API keys (Settings → API)

#### 1.2 Run Database Migrations

In your Supabase SQL Editor, run these migrations in order:

1. **Schema Creation**
   ```sql
   -- Copy and paste contents from:
   supabase/migrations/001_create_schema.sql
   ```

2. **Row Level Security**
   ```sql
   -- Copy and paste contents from:
   supabase/migrations/002_rls_policies.sql
   ```

#### 1.3 Create Your First Admin User

```sql
INSERT INTO admin_users (email, role, is_active)
VALUES ('your-email@example.com', 'super_admin', true);
```

Replace `your-email@example.com` with the email you'll use to sign in.

### Step 2: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your Supabase credentials:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_ANON_KEY=your_anon_key_here
   SUPABASE_SERVICE_KEY=your_service_key_here
   ```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Frontend

#### 4.1 Update Admin Panel

Edit `admin/control-panel.html` line 354-355:

```javascript
const SUPABASE_URL = 'https://your-project.supabase.co';
const SUPABASE_ANON_KEY = 'your_anon_key_here';
```

#### 4.2 Update Public Frontend

Edit `public/index.html` line 528-529:

```javascript
const SUPABASE_URL = 'https://your-project.supabase.co';
const SUPABASE_ANON_KEY = 'your_anon_key_here';
```

### Step 5: Launch the Platform

#### Option A: Simple HTTP Server (Development)

```bash
# Serve public frontend
cd public
python -m http.server 8000

# In another terminal, serve admin panel
cd admin
python -m http.server 8001
```

Access:
- **Public Frontend**: http://localhost:8000
- **Admin Panel**: http://localhost:8001

#### Option B: Production Deployment

Deploy to Vercel, Netlify, or any static hosting:

1. Upload `public/` folder to your hosting
2. Upload `admin/` folder to a password-protected subdomain
3. Set up Supabase authentication for admin access

## 📊 Database Schema

### Core Tables

#### `players`
Stores all player information and aggregated stats.

#### `events`
Tracks each of the 7 events (Events 1-6 + Tournament of Champions).

#### `matches` (Production)
Published match data visible to the public.

#### `staging_matches` (Admin Only)
Pending matches awaiting review and approval.

#### `event_standings`
Round Robin standings for each event/group.

#### `series_leaderboard`
Overall series rankings across all events.

#### `brand_sponsors`
Organization and sponsor information.

#### `admin_users`
Admin user accounts for control panel access.

## 🎯 Tournament Rules Implementation

### Events 1-6 (Regular Events)

**Format**: 10 players, 2 groups (A & B)

**Round Robin Phase**:
- Each group plays internally (all vs all)
- Ranking criteria (in order):
  1. Wins
  2. Leg Difference
  3. Head-to-Head (manual resolution)
  4. 3-Dart Average

**Knockout Phase**:
- Top 4 from each group advance
- Crossover seeding:
  - QF1: A1 vs B4
  - QF2: B2 vs A3
  - QF3: B1 vs A4
  - QF4: A2 vs B3
- Semifinals: QF1 winner vs QF2 winner, QF3 winner vs QF4 winner
- Final: SF winners

### Event 7 (Tournament of Champions)

**Format**: 6 players (winners of Events 1-6)

**Round Robin**:
- Single group, all players face each other
- Same ranking criteria as regular events

**Knockout**:
- Top 4 advance to semifinals
- SF1: 1st vs 4th
- SF2: 2nd vs 3rd
- Final: SF winners

## 🔄 Data Flow Workflow

### 1. Scraper Captures Data

Your existing scraper (`Event-Scraper-StandAlone`) captures match data.

### 2. Data Goes to Staging

Use the migration script to send data to staging:

```python
from scripts.data_migration import AADSDataMigration

migrator = AADSDataMigration(SUPABASE_URL, SUPABASE_KEY)

match_data = {
    'event_id': 'uuid-of-event',
    'phase': 'round_robin',
    'group_name': 'A',
    'player_1_name': 'John Doe',
    'player_2_name': 'Jane Smith',
    'player_1_legs': 5,
    'player_2_legs': 3,
    'player_1_average': 85.5,
    'player_2_average': 78.3,
    # ... other fields
}

result = migrator.process_scraped_match(match_data)
```

### 3. Admin Reviews in Control Panel

1. Admin logs into control panel
2. Views staging queue with pending matches
3. **Inline editing**: Click any field to edit directly
4. **Approve**: Data moves to production `matches` table
5. **Reject**: Data marked as rejected with optional notes

### 4. Automatic Calculations

When match is approved, triggers automatically:
- Update `event_standings` (RR stats)
- Update `series_leaderboard` (overall stats)
- Calculate rankings based on AADS rules

### 5. Public Display

Data appears instantly on:
- Series leaderboard
- Event standings
- Player profiles
- Knockout brackets

## 🛡️ Security & Access Control

### Row Level Security (RLS)

**Public Access**:
- ✅ Read `players`, `events`, `matches`, `event_standings`, `series_leaderboard`
- ✅ View active sponsors
- ❌ No write access

**Admin Access** (Authenticated):
- ✅ Full CRUD on all tables
- ✅ Access to `staging_matches`
- ✅ Approve/reject workflow

### Authentication Setup

1. Enable Supabase Auth (Email/Password or OAuth)
2. Users must have email in `admin_users` table
3. `is_admin()` function checks authentication

## 📱 Admin Control Panel Features

### Dashboard Overview
- Pending reviews count
- Approved today count
- Total matches
- Active players

### Staging Queue
- View all pending matches
- **Inline editing**: Click field to edit
- Approve/reject buttons
- Filter by status

### Published Matches
- View all live matches
- Edit if needed
- Filter by event/phase

### Player Management
- View all players
- Add new players
- View detailed stats

### Event Management
- Create new events
- Update event status
- Set event winners

## 🎨 Frontend Customization

### Branding

Edit `public/index.html` to update sponsors (lines 103-143):

```html
<div class="sponsor-logo">
    <a href="https://your-sponsor.com" target="_blank">
        Your Sponsor Name
    </a>
</div>
```

### Styling

Colors are defined in CSS variables (`:root`):

```css
--primary-color: #1a472a;      /* Dark green */
--secondary-color: #2d7a4f;    /* Medium green */
--accent-color: #ffd700;       /* Gold */
```

## 🧪 Testing Tournament Logic

Run the tournament logic test suite:

```bash
python scripts/tournament_logic.py
```

This demonstrates:
- Round Robin ranking
- Knockout seeding
- Tournament of Champions bracket generation

## 📊 API Functions

### Get Player Stats

```javascript
const { data } = await supabase.rpc('get_player_stats', {
    p_player_id: 'player-uuid',
    p_filter: 'series' // 'all', 'event_1', 'knockouts', 'series'
});
```

### Get Knockout Bracket

```javascript
const { data } = await supabase.rpc('get_knockout_bracket', {
    p_event_id: 'event-uuid'
});
```

## 🔧 Troubleshooting

### Issue: Admin can't access staging queue

**Solution**: 
1. Ensure user email is in `admin_users` table
2. Check RLS policies are enabled
3. Verify user is authenticated

### Issue: Rankings not updating

**Solution**:
1. Check database triggers are created
2. Verify `event_standings` and `series_leaderboard` tables exist
3. Review trigger execution logs in Supabase

### Issue: Frontend not loading data

**Solution**:
1. Check browser console for errors
2. Verify Supabase URL and API key are correct
3. Ensure RLS policies allow public read access

## 📞 Support

For issues or questions:
1. Check database logs in Supabase Dashboard
2. Review browser console for JavaScript errors
3. Verify all migrations ran successfully

## 🎯 Next Steps

1. ✅ Set up Supabase project
2. ✅ Run migrations
3. ✅ Configure frontend with API keys
4. ✅ Create first admin user
5. ✅ Test data migration script
6. ✅ Import or create first event
7. ✅ Test staging workflow
8. ✅ Customize branding
9. ✅ Deploy to production

## 📄 License

MIT License - Feel free to customize and extend for your tournament!
