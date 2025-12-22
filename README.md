# AADS Stats V2 - Complete Platform

**Atlantic Amateur Darts Series Official Statistics Platform**

A comprehensive full-stack tournament management system with event scraping, admin review workflow, and public statistics display.

---

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [System Overview](#system-overview)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Deployment](#deployment)
- [Architecture](#architecture)
- [Support](#support)

---

## 🚀 Quick Start

### Prerequisites
- **Supabase Account**: [https://supabase.com](https://supabase.com) (free tier works)
- **Python 3.8+**: For event scraper
- **Modern Web Browser**: Chrome, Firefox, Safari, or Edge

### 5-Minute Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/dowdarts/AADSSTATSV2.git
   cd AADSSTATSV2
   ```

2. **Setup Supabase Database**
   - Create new project at [supabase.com](https://supabase.com)
   - Go to SQL Editor
   - Run migrations in order:
     - `supabase/migrations/001_create_schema.sql`
     - `supabase/migrations/002_rls_policies.sql`
     - `supabase/migrations/003_add_event_tracking.sql`

3. **Configure Environment**
   ```bash
   cd aads-stats-v2
   cp .env.example .env
   # Edit .env with your Supabase credentials
   ```

4. **Install Event Scraper**
   ```bash
   cd ../Event-Scraper-StandAlone
   pip install -r requirements.txt
   ```

5. **Start Scraper Server**
   ```bash
   python api_server.py
   ```

6. **Access Applications**
   - **Event Scraper**: http://localhost:5000
   - **Admin Panel**: http://localhost:8001/admin/control-panel.html
   - **Public Display**: Open `public/index.html` in browser

---

## 🏗️ System Overview

### Three-Tier Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    EVENT SCRAPER (localhost:5000)            │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │   Step 1:    │→ │   Step 2:    │→ │    Step 3:      │   │
│  │ Select Event │  │ Match Results│  │ Match Details   │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
│           ↓                 ↓                    ↓           │
│  ┌───────────────────────────────────────────────────────┐  │
│  │           Step 4: Review Stats Table                  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
        ┌─────────────────────────────┐
        │   SUPABASE (Cloud Database) │
        │   staging_matches table     │
        └─────────────┬───────────────┘
                      ↓
┌─────────────────────────────────────────────────────────────┐
│           ADMIN CONTROL PANEL (localhost:8001)              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  • Review scraped data                               │   │
│  │  • Inline edit any field (click to edit)             │   │
│  │  • Approve → Production | Reject → Delete            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
        ┌─────────────────────────────┐
        │   SUPABASE (Cloud Database) │
        │   matches table (production)│
        └─────────────┬───────────────┘
                      ↓
┌─────────────────────────────────────────────────────────────┐
│           PUBLIC DISPLAY (GitHub Pages)                     │
│  • Series Leaderboard    • Event Standings                  │
│  • Knockout Brackets     • Player Search                    │
│  • Statistics Dashboard  • Event History                    │
└─────────────────────────────────────────────────────────────┘
```

### Key Features

✅ **Event-Based Scraping** (Events 1-6)
✅ **Two-Stage Workflow** (Match Results → Match Details)
✅ **Admin Review Queue** with inline editing
✅ **Automatic Calculations** (standings, leaderboards, brackets)
✅ **Real-time Updates** via Supabase
✅ **Mobile Responsive** design
✅ **GitHub Pages** deployment

---

## 📦 Installation

### Event Scraper Setup

```bash
cd Event-Scraper-StandAlone

# Install Python dependencies
pip install -r requirements.txt

# Start Flask API server
python api_server.py
```

**Required Packages:**
- Flask 3.0+
- Flask-CORS 4.0+
- BeautifulSoup4 4.12+
- Selenium 4.15+
- Requests 2.31+
- webdriver-manager

### Frontend Setup

No build process required! Pure HTML/CSS/JavaScript.

```bash
cd aads-stats-v2

# Configure Supabase credentials
cp .env.example .env
nano .env  # Edit with your credentials
```

### Database Setup

1. **Create Supabase Project**
   - Visit [supabase.com](https://supabase.com)
   - Click "New Project"
   - Note your Project URL and Anon Key

2. **Run Migrations**
   ```sql
   -- In Supabase SQL Editor, run in order:
   -- 1. supabase/migrations/001_create_schema.sql
   -- 2. supabase/migrations/002_rls_policies.sql
   -- 3. supabase/migrations/003_add_event_tracking.sql
   ```

3. **Create Admin User**
   ```sql
   INSERT INTO admin_users (email, role, is_active)
   VALUES ('admin@aadsstats.com', 'super_admin', true);
   ```

---

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# Supabase Configuration
SUPABASE_URL=https://yppxkvbmffcvdxuswsbf.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here

# Project Configuration
PROJECT_NAME=AADS Stats V2
ADMIN_EMAIL=admin@aadsstats.com
```

### Update Frontend Files

**Admin Panel** (`admin/control-panel.html`):
```javascript
const SUPABASE_URL = 'YOUR_SUPABASE_URL';
const SUPABASE_ANON_KEY = 'YOUR_ANON_KEY';
```

**Public Display** (`public/index.html`):
```javascript
const SUPABASE_URL = 'YOUR_SUPABASE_URL';
const SUPABASE_ANON_KEY = 'YOUR_ANON_KEY';
```

---

## 🎯 Usage

### Complete Workflow: From Scraping to Public Display

#### Step 1: Scrape Event Data

1. Open Event Scraper: http://localhost:5000
2. Select event number (1-6) from dropdown
3. Enter DartConnect event URL
4. Click "Find Matches" → 27 matches found
5. Click "Scrape Match Results (Stage 1)" → Basic scores captured
6. Click "Scrape Match Details (Stage 2)" → Detailed stats captured
7. Review stats in comprehensive table
8. Click "Send to Admin Control Panel"

**Event Structure (27 matches):**
- 1 Final
- 2 Semifinals
- 4 Quarterfinals
- 10 Group A Round Robin
- 10 Group B Round Robin

#### Step 2: Admin Review & Approval

1. Open Admin Panel: http://localhost:8001/admin/control-panel.html
2. Login with admin credentials
3. View staging matches (event-specific)
4. **Inline Edit**: Click any cell to edit
   - Player names
   - Scores (legs/sets)
   - Averages
   - 180s counts
   - Highest checkouts
5. Click "Approve" → Moves to production
6. Click "Reject" → Deletes from staging

#### Step 3: View Public Stats

1. Open Public Display: `public/index.html`
2. Navigate sections:
   - **Standings**: Series leaderboard with rankings
   - **Events**: Event-specific standings (Group A/B)
   - **Champions**: Past event winners
   - **Statistics**: Top averages, 180s, checkouts
   - **Players**: Search and filter

---

## 🚀 Deployment

### GitHub Pages (Public Display Only)

```bash
# Enable GitHub Pages in repository settings:
# Settings → Pages → Source: GitHub Actions

# Push to trigger auto-deploy
git push origin main

# Public URL:
# https://dowdarts.github.io/AADSSTATSV2/
```

### Local Deployment (Admin + Scraper)

**Admin Panel** and **Event Scraper** must run localhost only for security.

```bash
# Start Event Scraper
cd Event-Scraper-StandAlone
python api_server.py  # http://localhost:5000

# Start Admin Panel (use any local server)
cd aads-stats-v2/admin
python -m http.server 8001  # http://localhost:8001
```

### Production Considerations

- ✅ Public display → GitHub Pages (free, fast)
- ❌ Admin panel → NEVER deploy publicly
- ❌ Event scraper → NEVER deploy publicly
- ✅ Supabase → Handles all backend/database
- ✅ Row Level Security → Protects staging data

---

## 🏛️ Architecture

### Database Schema

**8 Core Tables:**
1. `players` - Player registry
2. `events` - Tournament events
3. `matches` - Production match data
4. `staging_matches` - Admin review queue
5. `event_standings` - Group standings (view)
6. `series_leaderboard` - Overall rankings
7. `brand_sponsors` - Sponsor management
8. `admin_users` - Admin authentication

**Key Columns (staging_matches/matches):**
- `event_number` (1-7)
- `phase` (round_robin, quarterfinal, semifinal, final)
- `group_name` (A, B, or NULL)
- `player_1/2_100_plus` through `player_1/2_180s`
- `player_1/2_doubles_hit/attempted`
- `is_knockout` (TRUE = set play, FALSE = best of 5 legs)
- `scrape_stage` (match_results, match_details, complete)

### API Endpoints (Event Scraper)

```
POST /api/scrape_event
  → Find all match URLs from event page

POST /api/scrape_match_result
  → Stage 1: Extract player names, scores, winner

POST /api/scrape_match_details
  → Stage 2: Extract 3DA, legs, 180s, checkouts, doubles

POST /api/send_to_admin
  → Send complete data to Supabase staging table

GET /admin/health
  → Health check endpoint
```

### File Structure

```
AADSSTATSV2/
├── Event-Scraper-StandAlone/
│   ├── api_server.py          # Flask API server
│   ├── event_scraper.html     # Scraper UI (4-step workflow)
│   ├── requirements.txt       # Python dependencies
│   ├── src/
│   │   ├── scraper.py         # DartConnect scraping logic
│   │   ├── event_data_manager.py  # Data persistence
│   │   └── database_manager.py    # Database operations
│   └── data/                  # JSON/CSV backups
│
├── aads-stats-v2/
│   ├── admin/
│   │   └── control-panel.html # Admin dashboard
│   ├── public/
│   │   └── index.html         # Public stats display
│   ├── supabase/
│   │   └── migrations/        # Database migrations
│   ├── scripts/
│   │   ├── data_migration.py  # Data utilities
│   │   └── tournament_logic.py # Ranking algorithms
│   ├── .env                   # Environment config
│   └── package.json           # Project metadata
│
├── display-app/               # Legacy standalone display
├── README.md                  # This file
└── .gitignore                 # Git exclusions
```

---

## 🔧 Troubleshooting

### Event Scraper Issues

**Problem**: Server won't start
```bash
# Solution: Check Python version
python --version  # Must be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

**Problem**: Selenium errors
```bash
# Solution: Update Chrome/ChromeDriver
pip install webdriver-manager --upgrade
```

### Supabase Connection Issues

**Problem**: "Failed to fetch" errors
- Check SUPABASE_URL and SUPABASE_ANON_KEY
- Verify RLS policies are created
- Check browser console for CORS errors

**Problem**: Data not appearing
```sql
-- Check if tables exist
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public';

-- Check staging data
SELECT COUNT(*) FROM staging_matches;
```

### Admin Panel Issues

**Problem**: Can't edit fields
- Ensure you're logged in as admin
- Check `admin_users` table has your email
- Verify `is_admin()` function exists

---

## 📚 Additional Resources

### Documentation Files

- **USER_GUIDE.md** - Step-by-step usage instructions
- **EVENT_BASED_SCRAPING_GUIDE.md** - Detailed scraping workflow
- **supabase/migrations/** - Database schema documentation

### External Links

- **Supabase Docs**: https://supabase.com/docs
- **DartConnect**: https://www.dartconnect.com
- **GitHub Pages**: https://pages.github.com
- **AADS Website**: https://aadsdarts.com

---

## 🤝 Support

### Issues & Questions

- **GitHub Issues**: https://github.com/dowdarts/AADSSTATSV2/issues
- **Email**: admin@aadsstats.com

### Contributing

Pull requests welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is proprietary software for the Atlantic Amateur Darts Series.

---

## 🙏 Acknowledgments

- **AADS Organization** - Tournament management
- **DartConnect** - Match data source
- **Supabase** - Backend infrastructure
- **GitHub Pages** - Free hosting

---

**Version**: 2.0.0  
**Last Updated**: December 22, 2025  
**Maintainer**: AADS Development Team
