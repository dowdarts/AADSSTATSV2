# 🚀 AADS Stats V2 - Setup Checklist

## ✅ Your Configuration

- **Supabase Project**: dowdarts's Project
- **Project ID**: yppxkvbmffcvdxuswsbf
- **Supabase URL**: https://yppxkvbmffcvdxuswsbf.supabase.co
- **GitHub Repo**: https://github.com/dowdarts/AADSSTATSV2.git

## 📋 Next Steps

### Step 1: Run Database Migrations ⏱️ 5 minutes

1. Go to your Supabase Dashboard:
   - Visit: https://supabase.com/dashboard/project/yppxkvbmffcvdxuswsbf

2. Navigate to **SQL Editor** (left sidebar)

3. Create a new query and run **Migration 1**:
   - Copy entire contents from: `supabase/migrations/001_create_schema.sql`
   - Paste into SQL Editor
   - Click "Run" or press Ctrl+Enter
   - ✅ Should see "Success. No rows returned"

4. Create another new query and run **Migration 2**:
   - Copy entire contents from: `supabase/migrations/002_rls_policies.sql`
   - Paste into SQL Editor
   - Click "Run"
   - ✅ Should see "Success. No rows returned"

### Step 2: Create Your Admin User ⏱️ 1 minute

In Supabase SQL Editor, run:

```sql
INSERT INTO admin_users (email, role, is_active)
VALUES ('your-email@example.com', 'super_admin', true);
```

**Replace** `your-email@example.com` with your actual email.

### Step 3: Create Your First Event ⏱️ 1 minute

```sql
INSERT INTO events (event_number, event_name, event_date, venue, status)
VALUES (1, 'AADS Event 1 - January 2025', '2025-01-15', 'Your Venue Name', 'pending');
```

### Step 4: Get Your Service Key (Optional - for Python scripts)

1. Go to: https://supabase.com/dashboard/project/yppxkvbmffcvdxuswsbf/settings/api
2. Copy your **service_role key** (under "Project API keys")
3. Update `.env` file:
   ```
   SUPABASE_SERVICE_KEY=your_service_role_key_here
   ```

### Step 5: Install Python Dependencies ⏱️ 2 minutes

```powershell
cd "c:\Users\cgcda\OneDrive\Desktop\MDStudios-StandAlone-APPs\NewAADSSSCRAPPER\aads-stats-v2"
pip install -r requirements.txt
```

### Step 6: Launch the Platform! ⏱️ 1 minute

**Terminal 1 - Public Frontend:**
```powershell
cd "c:\Users\cgcda\OneDrive\Desktop\MDStudios-StandAlone-APPs\NewAADSSSCRAPPER\aads-stats-v2\public"
python -m http.server 8000
```

**Terminal 2 - Admin Control Panel:**
```powershell
cd "c:\Users\cgcda\OneDrive\Desktop\MDStudios-StandAlone-APPs\NewAADSSSCRAPPER\aads-stats-v2\admin"
python -m http.server 8001
```

### Step 7: Access Your Platforms

- **Public Frontend**: http://localhost:8000
- **Admin Control Panel**: http://localhost:8001

---

## ✨ Configuration Already Complete!

✅ Supabase URL configured in admin panel  
✅ Supabase URL configured in public frontend  
✅ API keys configured in both files  
✅ .env file created with your credentials  
✅ Data migration script configured  

---

## 🧪 Test the Integration

### Quick Test with Python:

```powershell
cd "c:\Users\cgcda\OneDrive\Desktop\MDStudios-StandAlone-APPs\NewAADSSSCRAPPER\aads-stats-v2"
python scripts/data_migration.py
```

This will test the connection to your Supabase project.

---

## 📊 Verify Database Setup

Go to Supabase Table Editor:
- Visit: https://supabase.com/dashboard/project/yppxkvbmffcvdxuswsbf/editor

You should see these tables:
- ✅ players
- ✅ events
- ✅ matches
- ✅ staging_matches
- ✅ event_standings
- ✅ series_leaderboard
- ✅ brand_sponsors
- ✅ admin_users

---

## 🔗 Connect Your Existing Scraper

1. Open your existing scraper: `Event-Scraper-StandAlone/scraper.py`

2. Add at the top:
```python
import sys
sys.path.append('../aads-stats-v2')

from scripts.data_migration import AADSDataMigration
from dotenv import load_dotenv
import os

load_dotenv('../aads-stats-v2/.env')

# Initialize migrator
migrator = AADSDataMigration(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_ANON_KEY')
)
```

3. After scraping each match:
```python
result = migrator.process_scraped_match(match_data)
if result['success']:
    print(f"✅ Match sent to staging: {result['staging_id']}")
```

See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for complete details.

---

## 🎯 What You Can Do Right Now

1. ✅ **Run migrations** (Step 1)
2. ✅ **Create admin user** (Step 2)
3. ✅ **Launch the platform** (Step 6)
4. ✅ **Visit the admin panel** at http://localhost:8001
5. ✅ **Visit the public frontend** at http://localhost:8000

---

## 📞 Quick Links

- **Supabase Dashboard**: https://supabase.com/dashboard/project/yppxkvbmffcvdxuswsbf
- **SQL Editor**: https://supabase.com/dashboard/project/yppxkvbmffcvdxuswsbf/sql
- **Table Editor**: https://supabase.com/dashboard/project/yppxkvbmffcvdxuswsbf/editor
- **API Settings**: https://supabase.com/dashboard/project/yppxkvbmffcvdxuswsbf/settings/api
- **GitHub Repo**: https://github.com/dowdarts/AADSSTATSV2.git

---

## 🎉 Ready to Go!

Everything is configured with your actual Supabase credentials. Just run the migrations and launch! 🚀
