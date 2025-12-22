# 🎯 AADS Stats V2 - Quick Reference Card

## 📍 Important URLs

| Component | URL | Access |
|-----------|-----|--------|
| **GitHub Repository** | https://github.com/dowdarts/AADSSTATSV2 | Public |
| **Public Stats (Live)** | https://dowdarts.github.io/AADSSTATSV2/ | Public |
| **Admin Control Panel** | http://localhost:8001 | Localhost Only |
| **Event Scraper** | http://localhost:5000 | Localhost Only |
| **Supabase Dashboard** | https://supabase.com/dashboard/project/yppxkvbmffcvdxuswsbf | Your Account |

---

## ⚡ Quick Commands

### Start Admin Control Panel
```powershell
cd "c:\Users\cgcda\OneDrive\Desktop\MDStudios-StandAlone-APPs\NewAADSSSCRAPPER\aads-stats-v2\admin"
python -m http.server 8001
```
**Then open**: http://localhost:8001

### Start Event Scraper
```powershell
cd "c:\Users\cgcda\OneDrive\Desktop\MDStudios-StandAlone-APPs\NewAADSSSCRAPPER\Event-Scraper-StandAlone"
python api_server.py
```
**Then open**: http://localhost:5000

### Test Public Frontend Locally
```powershell
cd "c:\Users\cgcda\OneDrive\Desktop\MDStudios-StandAlone-APPs\NewAADSSSCRAPPER\aads-stats-v2\public"
python -m http.server 8000
```
**Then open**: http://localhost:8000

### Push Changes to GitHub
```powershell
cd "c:\Users\cgcda\OneDrive\Desktop\MDStudios-StandAlone-APPs\NewAADSSSCRAPPER\aads-stats-v2"
git add .
git commit -m "Your change description"
git push origin main
```
**Auto-deploys to**: https://dowdarts.github.io/AADSSTATSV2/

---

## 🔑 Immediate Actions Required

### 1. Enable GitHub Pages (2 min)
1. Go to: https://github.com/dowdarts/AADSSTATSV2/settings/pages
2. Under "Source", select **"GitHub Actions"**
3. Click Save
4. Wait for deployment at: https://github.com/dowdarts/AADSSTATSV2/actions

### 2. Add Collaborator (1 min)
1. Go to: https://github.com/dowdarts/AADSSTATSV2/settings/access
2. Click "Add people"
3. Enter: **dowdarts**
4. Select role: **Write**
5. Send invitation

---

## 📊 Typical Workflow

```
1. Run Scraper (localhost:5000)
   ↓
2. Scrape event data
   ↓
3. Data goes to Supabase staging_matches table
   ↓
4. Open Admin Panel (localhost:8001)
   ↓
5. Review staged data
   ↓
6. Click fields to edit if needed
   ↓
7. Click "Approve" button
   ↓
8. Data moves to production matches table
   ↓
9. Triggers auto-update standings & leaderboard
   ↓
10. Public site updates instantly
    https://dowdarts.github.io/AADSSTATSV2/
```

---

## 🌐 Embed Code for aadsdarts.com

**Quick Embed (Full Page)**:
```html
<iframe src="https://dowdarts.github.io/AADSSTATSV2/" 
        width="100%" height="800px" frameborder="0"></iframe>
```

**Responsive Embed**:
```html
<div style="position: relative; padding-bottom: 56.25%; height: 0;">
    <iframe src="https://dowdarts.github.io/AADSSTATSV2/" 
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
            frameborder="0"></iframe>
</div>
```

---

## 🔒 Security Checklist

- [x] `.env` file in `.gitignore` (credentials protected)
- [x] Admin panel localhost-only (never deployed)
- [x] Event scraper localhost-only (never deployed)
- [x] Public frontend on GitHub Pages (safe, read-only)
- [x] Supabase RLS policies active (admin vs public access)

---

## 📞 Admin Credentials

**Supabase Admin User**:
- Email: `admin@aadsstats.com`
- Created: ✅ (in admin_users table)
- Role: super_admin

**Change admin email**:
```sql
-- Run in Supabase SQL Editor
UPDATE admin_users 
SET email = 'your-actual-email@example.com' 
WHERE email = 'admin@aadsstats.com';
```

---

## 📁 File Structure

```
aads-stats-v2/
├── admin/
│   └── control-panel.html          ← Localhost only ❌
├── public/
│   └── index.html                  ← GitHub Pages ✅
├── scripts/
│   ├── data_migration.py           ← Migration utilities
│   └── tournament_logic.py         ← Ranking algorithms
├── supabase/migrations/
│   ├── 001_create_schema.sql       ← Database schema
│   └── 002_rls_policies.sql        ← Security policies
├── .env.example                     ← Template (copy to .env)
├── .gitignore                       ← Protects .env
├── GITHUB_SETUP_INSTRUCTIONS.md    ← This guide
└── DEPLOYMENT_GUIDE.md             ← Full deployment docs

Event-Scraper-StandAlone/
├── event_scraper.html              ← Localhost only ❌
├── api_server.py                   ← Python server
└── src/scraper.py                  ← Scraping logic
```

---

## 🎯 Success Indicators

✅ **GitHub Pages Live**: https://dowdarts.github.io/AADSSTATSV2/

✅ **Admin Panel Running**: http://localhost:8001

✅ **Scraper Running**: http://localhost:5000

✅ **Collaborator Added**: `dowdarts` has push access

✅ **Stats Embedded**: Working on aadsdarts.com

---

## 📖 Full Documentation

- **[GITHUB_SETUP_INSTRUCTIONS.md](GITHUB_SETUP_INSTRUCTIONS.md)** - Setup steps
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Deployment architecture
- **[README.md](README.md)** - Complete setup guide
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - API reference

---

**Repository**: https://github.com/dowdarts/AADSSTATSV2

**Live Stats**: https://dowdarts.github.io/AADSSTATSV2/

**Admin**: http://localhost:8001

**Scraper**: http://localhost:5000
