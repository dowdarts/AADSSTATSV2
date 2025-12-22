# 🎯 AADS Stats Engine & Control Panel V2

## Project Summary

A complete professional statistics platform for the Atlantic Amateur Darts Series (AADS) featuring a staging workflow, admin control panel, and public-facing frontend with Supabase backend.

## 📁 Project Structure

```
aads-stats-v2/
│
├── supabase/
│   └── migrations/
│       ├── 001_create_schema.sql         # Complete database schema
│       └── 002_rls_policies.sql          # Row Level Security policies
│
├── admin/
│   └── control-panel.html                # Admin dashboard for data review
│
├── public/
│   └── index.html                        # Public-facing stats display
│
├── scripts/
│   ├── data_migration.py                 # Scraper → Supabase integration
│   └── tournament_logic.py               # Ranking & seeding algorithms
│
├── .env.example                          # Environment variables template
├── requirements.txt                      # Python dependencies
├── package.json                          # Project metadata
│
├── README.md                             # Setup & deployment guide
├── INTEGRATION_GUIDE.md                  # Scraper integration guide
└── API_DOCUMENTATION.md                  # Complete API reference
```

## ✨ Key Features

### 1. **Staging Workflow** 
- ✅ Scraped data enters "Pending" state
- ✅ Admin reviews in Control Panel
- ✅ Inline editing of any field
- ✅ Approve/Reject workflow
- ✅ Data validation before production

### 2. **Admin Control Panel**
- 📊 Dashboard with stats overview
- 📋 Staging queue management
- ✏️ Inline field editing
- ✅ One-click approval
- 👥 Player management
- 🏆 Event management
- 📈 Real-time statistics

### 3. **Public Frontend**
- 🏅 Series leaderboard with rankings
- 📊 Event standings (Group A & B)
- 🔍 Player search with filters
- 📇 Dynamic player cards
- 🎯 Knockout bracket visualization
- 🎨 Professional AADS branding
- 📱 Responsive design

### 4. **Tournament Logic**
- 🥇 Round Robin ranking (Wins → Leg Diff → H2H → 3DA)
- 🔀 Crossover knockout seeding
- 🏆 Tournament of Champions format
- 📊 Automatic standings calculation
- 🎲 Match generation utilities

### 5. **Database Architecture**
- 🗄️ PostgreSQL with Supabase
- 🔒 Row Level Security (RLS)
- ⚡ Automatic triggers for calculations
- 📈 Materialized series stats
- 🔐 Admin/public access control

## 🎮 Tournament Rules Implementation

### Events 1-6 (Regular Format)
- **10 players** → 2 groups (A & B)
- **Round Robin**: All vs all within group
- **Ranking**: Wins → Leg Diff → H2H → 3DA
- **Knockouts**: Top 4 advance with crossover seeding
  - A1 vs B4, B2 vs A3, B1 vs A4, A2 vs B3

### Event 7 (Tournament of Champions)
- **6 players** (Event 1-6 winners only)
- **Single group**: Round Robin
- **Top 4 advance** to semifinals (1v4, 2v3)
- **Final**: SF winners

## 🔄 Data Flow

```
┌─────────────────────┐
│  Your Scraper       │  Captures match data from website
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Migration Script   │  Validates & sends to staging
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Staging Queue      │  Admin reviews in Control Panel
│  (Pending State)    │  - View all matches
└──────────┬──────────┘  - Edit any field inline
           │              - Approve or reject
           ▼
┌─────────────────────┐
│  Production DB      │  Approved data goes live
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Public Frontend    │  Displays stats to users
└─────────────────────┘
```

## 🚀 Quick Start

### 1. Setup Supabase
1. Create project at [supabase.com](https://supabase.com)
2. Run migrations from `supabase/migrations/`
3. Create admin user in `admin_users` table

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

### 3. Update Frontend
Edit `admin/control-panel.html` and `public/index.html`:
```javascript
const SUPABASE_URL = 'your-url-here';
const SUPABASE_ANON_KEY = 'your-key-here';
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Launch
```bash
# Public frontend
cd public && python -m http.server 8000

# Admin panel
cd admin && python -m http.server 8001
```

## 📊 Database Schema

### Core Tables
- **players** - Player profiles and series stats
- **events** - Event information (1-7)
- **matches** - Production match data (public)
- **staging_matches** - Pending review queue (admin-only)
- **event_standings** - Round Robin standings
- **series_leaderboard** - Overall series rankings
- **brand_sponsors** - Sponsor information
- **admin_users** - Admin access control

### Custom Functions
- `get_player_stats(player_id, filter)` - Filtered player statistics
- `get_knockout_bracket(event_id)` - Bracket visualization data
- `is_admin()` - Check admin permissions

## 🔐 Security Features

### Row Level Security (RLS)
- ✅ Public read access to production data
- ❌ Public cannot write anything
- ✅ Admins have full CRUD access
- 🔒 Staging queue is admin-only
- 🛡️ Email-based admin verification

### Authentication
- Supabase Auth integration ready
- Email/password or OAuth support
- Admin role verification
- Session management

## 🎨 Customization

### Branding
Edit sponsor logos in `public/index.html`:
```html
<div class="sponsor-logo">
    <a href="https://your-sponsor.com">Your Sponsor</a>
</div>
```

### Styling
CSS variables in both HTML files:
```css
--primary-color: #1a472a;      /* Dark green */
--secondary-color: #2d7a4f;    /* Medium green */
--accent-color: #ffd700;       /* Gold */
```

## 📚 Documentation

- **[README.md](README.md)** - Complete setup guide
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - Connect your scraper
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - API reference

## 🧪 Testing

### Test Tournament Logic
```bash
python scripts/tournament_logic.py
```

### Test Data Migration
```bash
python scripts/data_migration.py
```

## 🌟 Features Highlights

### Admin Control Panel
- Real-time dashboard statistics
- Tabbed interface (Staging/Matches/Players/Events)
- Inline field editing (click to edit)
- Bulk approval workflow
- Search and filter capabilities
- Responsive design

### Public Frontend
- Professional AADS styling
- Series leaderboard with gold/silver/bronze ranks
- Event-specific standings
- Player search with multiple filter options
- Knockout bracket visualization
- Sponsor integration
- Mobile-responsive

## 🔧 Technology Stack

- **Backend**: Supabase (PostgreSQL)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Data Migration**: Python 3.8+
- **Database Functions**: PL/pgSQL
- **Authentication**: Supabase Auth
- **Hosting**: Static hosting (Vercel/Netlify/etc)

## 📈 Automatic Calculations

When a match is approved, the system automatically:
- ✅ Creates player records if needed
- ✅ Updates event standings
- ✅ Recalculates group rankings
- ✅ Updates series leaderboard
- ✅ Calculates leg differences
- ✅ Aggregates 3-dart averages
- ✅ Tracks 180s and checkouts

## 🎯 Use Cases

### For Admins
1. Scraper runs after event
2. Check staging queue for new data
3. Review and edit any errors
4. Approve to publish
5. Monitor stats dashboard

### For Players
1. Visit public frontend
2. Search for their name
3. View stats (Event/Series/Knockouts)
4. Check leaderboard ranking
5. Review match history

### For Spectators
1. View series leaderboard
2. Check event standings
3. See knockout brackets
4. Browse player profiles
5. Track tournament progress

## 🚧 Future Enhancements

Potential additions:
- [ ] Email notifications for new staging data
- [ ] Export to PDF/CSV
- [ ] Player comparison tool
- [ ] Historical trends graphs
- [ ] Mobile app (PWA)
- [ ] Live match scoring
- [ ] Photo uploads
- [ ] Social media integration

## 📞 Support

For issues:
1. Check [README.md](README.md) troubleshooting section
2. Review Supabase logs
3. Check browser console
4. Verify RLS policies

## 📄 License

MIT License - Customize and extend as needed!

## 🎉 Deployment Checklist

- [ ] Create Supabase project
- [ ] Run database migrations
- [ ] Create admin user(s)
- [ ] Update frontend API keys
- [ ] Test staging workflow
- [ ] Customize branding
- [ ] Deploy public frontend
- [ ] Deploy admin panel (password-protected)
- [ ] Set up authentication
- [ ] Integrate with scraper
- [ ] Test end-to-end workflow
- [ ] Go live! 🚀

---

**Built for the Atlantic Amateur Darts Series** 🎯
Professional stats tracking made simple.
