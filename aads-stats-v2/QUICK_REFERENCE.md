# AADS Stats V2 - Quick Reference

## 🚀 Essential Commands

### Start Development Servers
```bash
# Public Frontend (Port 8000)
cd public && python -m http.server 8000

# Admin Panel (Port 8001)  
cd admin && python -m http.server 8001
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Test Scripts
```bash
# Test tournament logic
python scripts/tournament_logic.py

# Test data migration
python scripts/data_migration.py
```

## 🔑 Configuration Files

### Environment Variables (.env)
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=eyJhbGc...
SUPABASE_SERVICE_KEY=eyJhbGc...
```

### Frontend Configuration
Update in both `admin/control-panel.html` and `public/index.html`:
```javascript
const SUPABASE_URL = 'YOUR_URL';
const SUPABASE_ANON_KEY = 'YOUR_KEY';
```

## 📊 Database Quick Reference

### Create Admin User
```sql
INSERT INTO admin_users (email, role, is_active)
VALUES ('admin@example.com', 'super_admin', true);
```

### Create Event
```sql
INSERT INTO events (event_number, event_name, event_date, status)
VALUES (1, 'AADS Event 1 - Jan 2025', '2025-01-15', 'pending');
```

### Create Player
```sql
INSERT INTO players (name, email)
VALUES ('John Doe', 'john@example.com');
```

### View Pending Staging
```sql
SELECT * FROM staging_matches WHERE status = 'pending';
```

### Get Leaderboard
```sql
SELECT 
    p.name,
    sl.overall_rank,
    sl.overall_3da,
    sl.total_wins
FROM series_leaderboard sl
JOIN players p ON sl.player_id = p.id
ORDER BY overall_rank;
```

## 🎯 Common API Calls

### Get All Players
```javascript
const { data } = await supabase
  .from('players')
  .select('*')
  .order('name');
```

### Get Event Standings
```javascript
const { data } = await supabase
  .from('event_standings')
  .select('*, players(name)')
  .eq('event_id', eventId)
  .order('rank');
```

### Get Player Stats
```javascript
const { data } = await supabase.rpc('get_player_stats', {
  p_player_id: playerId,
  p_filter: 'series'  // 'all', 'event_1', 'knockouts', 'series'
});
```

### Search Players
```javascript
const { data } = await supabase
  .from('players')
  .select('*')
  .ilike('name', `%${searchTerm}%`);
```

## 🔄 Data Migration Script

### Process Single Match
```python
from scripts.data_migration import AADSDataMigration

migrator = AADSDataMigration(SUPABASE_URL, SUPABASE_KEY)

match = {
    'event_id': 'event-uuid',
    'phase': 'round_robin',
    'group_name': 'A',
    'player_1_name': 'John Doe',
    'player_2_name': 'Jane Smith',
    'player_1_legs': 5,
    'player_2_legs': 3,
    'player_1_average': 85.5,
    'player_2_average': 78.3
}

result = migrator.process_scraped_match(match)
```

### Bulk Process
```python
matches = [match1, match2, match3]
results = migrator.bulk_process_matches(matches)
print(f"Success: {results['successful']}/{results['total']}")
```

## 🏆 Tournament Logic

### Rank Round Robin Group
```python
from scripts.tournament_logic import TournamentLogic, Player

players = [
    Player("p1", "Alice", wins=4, legs_won=20, legs_lost=8, average_3da=85.5),
    Player("p2", "Bob", wins=3, legs_won=18, legs_lost=10, average_3da=82.3),
    # ... more players
]

ranked = TournamentLogic.rank_round_robin_group(players)
top_4 = TournamentLogic.get_top_n(ranked, 4)
```

### Generate Knockout Bracket
```python
qf_matches = TournamentLogic.generate_knockout_seeding(group_a_top4, group_b_top4)
# Returns: [(A1, B4), (B2, A3), (B1, A4), (A2, B3)]
```

## 🎨 CSS Variables

```css
:root {
    --primary-color: #1a472a;      /* Dark green */
    --secondary-color: #2d7a4f;    /* Medium green */
    --accent-color: #ffd700;       /* Gold */
    --danger-color: #dc3545;       /* Red */
    --success-color: #28a745;      /* Green */
    --warning-color: #ffc107;      /* Yellow */
}
```

## 🔐 Access Levels

| Feature | Public | Admin |
|---------|--------|-------|
| View Players | ✅ | ✅ |
| View Matches | ✅ | ✅ |
| View Leaderboard | ✅ | ✅ |
| View Staging Queue | ❌ | ✅ |
| Edit Data | ❌ | ✅ |
| Approve/Reject | ❌ | ✅ |
| Create Events | ❌ | ✅ |

## 📱 URLs

### Development
- Public: `http://localhost:8000`
- Admin: `http://localhost:8001`

### Production
- Public: `https://your-domain.com`
- Admin: `https://admin.your-domain.com`

## 🐛 Troubleshooting

### Can't access staging queue
1. Check you're in `admin_users` table
2. Verify email matches authenticated user
3. Check RLS policies enabled

### Rankings not updating
1. Verify triggers exist in database
2. Check `event_standings` and `series_leaderboard` tables
3. Review Supabase logs

### Frontend not loading
1. Check browser console for errors
2. Verify Supabase URL/key correct
3. Check CORS settings in Supabase

## 📋 File Locations

| File | Purpose |
|------|---------|
| `supabase/migrations/001_create_schema.sql` | Database schema |
| `supabase/migrations/002_rls_policies.sql` | Security policies |
| `admin/control-panel.html` | Admin dashboard |
| `public/index.html` | Public frontend |
| `scripts/data_migration.py` | Data pipeline |
| `scripts/tournament_logic.py` | Ranking algorithms |
| `.env` | Environment config |
| `requirements.txt` | Python dependencies |

## 🎯 Common Tasks

### Add New Event
1. Go to Admin Panel → Events tab
2. Click "Create Event"
3. Fill in details
4. Save

### Review Staged Data
1. Go to Admin Panel → Staging Queue
2. Review each match
3. Click fields to edit
4. Click "Approve" to publish

### Search Player Stats
1. Go to Public Frontend → Player Search
2. Type player name
3. Select filter (Series/Event 1/Knockouts)
4. View player card

### View Event Standings
1. Go to Public Frontend → Event Standings
2. Select event from dropdown
3. View Group A and B standings

## 📞 Quick Help

| Issue | Solution |
|-------|----------|
| No data showing | Check Supabase connection |
| Can't edit | Verify admin authentication |
| Wrong rankings | Check match data accuracy |
| Missing players | Create in admin panel |
| Broken brackets | Ensure knockout matches exist |

## 🔗 Documentation Links

- [Full Setup Guide](README.md)
- [Integration Guide](INTEGRATION_GUIDE.md)
- [API Documentation](API_DOCUMENTATION.md)
- [Project Summary](PROJECT_SUMMARY.md)

## 💡 Tips

- Use inline editing in staging queue for quick fixes
- Filter player stats by Event/Series/Knockouts
- Check dashboard for pending review count
- Export data via Supabase SQL editor
- Monitor real-time updates with subscriptions

---

**Quick Start**: Setup Supabase → Run migrations → Update API keys → Launch! 🚀
