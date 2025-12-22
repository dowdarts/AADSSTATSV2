# AADS Stats Engine V2 - Deployment & Collaboration Guide

## 🚀 Deployment Architecture

### **Admin Control Panel** (Localhost Only)
- **Location**: `admin/control-panel.html`
- **Access**: `http://localhost:8001`
- **Security**: NOT deployed publicly, admin access only
- **Usage**: Run locally to review and approve staging data

### **Event Scraper** (Localhost Only)
- **Location**: `../Event-Scraper-StandAlone/event_scraper.html`
- **Access**: `http://localhost:5000` (via Python API server)
- **Security**: NOT deployed publicly, local scraping only
- **Usage**: Run locally to scrape event data and send to staging

### **Public Display Frontend** (GitHub Pages)
- **Location**: `public/index.html`
- **Live URL**: https://dowdarts.github.io/AADSSTATSV2/
- **Embedding**: Can be embedded on aadsdarts.com
- **Auto-Deploy**: Automatically deploys on push to main branch

---

## 📋 Setup Instructions

### 1️⃣ GitHub Collaboration Access

To grant **dowdarts** GitHub account push access:

```bash
# Repository owner (you) needs to:
# 1. Go to: https://github.com/dowdarts/AADSSTATSV2/settings/access
# 2. Click "Add people"
# 3. Enter GitHub username: dowdarts
# 4. Select role: "Write" or "Admin"
# 5. Send invitation
```

### 2️⃣ Enable GitHub Pages

```bash
# 1. Go to: https://github.com/dowdarts/AADSSTATSV2/settings/pages
# 2. Under "Source", select "GitHub Actions"
# 3. Save
# 4. The site will auto-deploy on next push
```

### 3️⃣ Run Admin Control Panel (Localhost)

```bash
# Terminal 1: Admin Panel
cd aads-stats-v2/admin
python -m http.server 8001

# Access at: http://localhost:8001
```

### 4️⃣ Run Event Scraper (Localhost)

```bash
# Terminal 2: Scraper API Server
cd Event-Scraper-StandAlone
python api_server.py

# Access scraper UI at: http://localhost:5000
```

### 5️⃣ View Public Frontend

**Option A - Locally (for testing)**:
```bash
# Terminal 3: Public Frontend
cd aads-stats-v2/public
python -m http.server 8000

# Access at: http://localhost:8000
```

**Option B - Live (after GitHub Pages deploy)**:
- Direct: https://dowdarts.github.io/AADSSTATSV2/
- Embedded on aadsdarts.com (see embedding section below)

---

## 🌐 Embedding on aadsdarts.com

### Full-Page Iframe

```html
<!DOCTYPE html>
<html>
<head>
    <title>AADS Stats</title>
    <style>
        body { margin: 0; padding: 0; overflow: hidden; }
        iframe { 
            width: 100vw; 
            height: 100vh; 
            border: none; 
        }
    </style>
</head>
<body>
    <iframe src="https://dowdarts.github.io/AADSSTATSV2/" 
            allowfullscreen>
    </iframe>
</body>
</html>
```

### Section Embed (Leaderboard Only)

```html
<!-- Add to your aadsdarts.com page -->
<div id="aads-stats-widget" style="width: 100%; min-height: 600px;">
    <iframe 
        src="https://dowdarts.github.io/AADSSTATSV2/" 
        width="100%" 
        height="800px"
        frameborder="0"
        scrolling="auto">
    </iframe>
</div>
```

---

## 🔒 Security Configuration

### Admin Panel (Localhost Only)
- ✅ **NEVER** deploy admin panel to public hosting
- ✅ Only accessible via `localhost:8001`
- ✅ Requires Supabase admin authentication
- ✅ RLS policies enforce admin-only access to staging data

### Event Scraper (Localhost Only)
- ✅ **NEVER** deploy scraper to public hosting
- ✅ Runs on local Python server (`localhost:5000`)
- ✅ Sends data to Supabase staging (not directly to production)
- ✅ Admin must review and approve all scraped data

### Public Frontend (GitHub Pages)
- ✅ Safe to deploy publicly
- ✅ Read-only access to public data via Supabase RLS
- ✅ No write permissions, no sensitive data exposed
- ✅ Uses Supabase Anonymous Key (public API key)

---

## 📊 Data Flow Workflow

```
┌─────────────────────────────────────────────────────────┐
│                   LOCALHOST ONLY                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Event Scraper (localhost:5000)                        │
│       │                                                 │
│       │ (sends to staging)                             │
│       ▼                                                 │
│  Supabase staging_matches table                        │
│       │                                                 │
│       │                                                 │
│  Admin Control Panel (localhost:8001)                  │
│       │                                                 │
│       │ (review & approve)                             │
│       ▼                                                 │
│  Supabase matches table (production)                   │
│       │                                                 │
└───────┼─────────────────────────────────────────────────┘
        │
        │ (automatic triggers update)
        ▼
┌─────────────────────────────────────────────────────────┐
│                   PUBLICLY ACCESSIBLE                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Public Frontend (GitHub Pages)                        │
│  https://dowdarts.github.io/AADSSTATSV2/               │
│       │                                                 │
│       │ (reads from)                                   │
│       ▼                                                 │
│  Supabase public tables:                               │
│    - series_leaderboard                                │
│    - event_standings                                   │
│    - matches                                           │
│    - players                                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🔄 Development Workflow

### Making Changes

```bash
# 1. Make your edits locally
# 2. Test locally
cd aads-stats-v2/public
python -m http.server 8000

# 3. Commit and push
git add .
git commit -m "Description of changes"
git push origin main

# 4. GitHub Actions auto-deploys to Pages
# 5. Check: https://dowdarts.github.io/AADSSTATSV2/
```

### Updating Admin Panel or Scraper

```bash
# Admin panel and scraper are NOT auto-deployed
# They remain localhost-only for security

# Just commit to track changes:
git add admin/control-panel.html
git commit -m "Updated admin panel"
git push origin main

# Run locally as needed:
cd admin
python -m http.server 8001
```

---

## 🎯 Post-Deployment Checklist

- [ ] GitHub Pages enabled (Settings → Pages → GitHub Actions)
- [ ] `.github/workflows/deploy-pages.yml` workflow file committed
- [ ] Public frontend accessible at GitHub Pages URL
- [ ] Admin panel runs locally on `localhost:8001`
- [ ] Event scraper runs locally on `localhost:5000`
- [ ] Supabase credentials configured in `.env` (NOT committed)
- [ ] `dowdarts` GitHub user granted repository access
- [ ] Test embedding on aadsdarts.com
- [ ] Verify staging workflow: Scraper → Staging → Admin Approval → Public Display

---

## 📞 Support & Collaboration

### Repository Owners
- Primary: Your GitHub account
- Collaborator: `dowdarts` (write access)

### GitHub Repository
- URL: https://github.com/dowdarts/AADSSTATSV2
- Public Frontend Live: https://dowdarts.github.io/AADSSTATSV2/

### Making Pull Requests
```bash
# For collaborators:
git checkout -b feature/your-feature-name
# Make changes
git commit -m "Description"
git push origin feature/your-feature-name
# Create PR on GitHub
```

---

## 🛡️ Important Security Notes

1. **NEVER commit `.env` file** - It's in `.gitignore`
2. **NEVER deploy admin panel publicly** - Localhost only
3. **NEVER deploy scraper publicly** - Localhost only
4. **ONLY deploy public frontend** - Read-only, safe for embedding
5. **Supabase Anonymous Key** - Safe to use in public frontend (RLS protects data)
6. **Supabase Service Key** - Keep secret, never commit, never expose

---

## 📄 Files & Directories

### Public (Safe to Deploy)
- `public/index.html` - Public display frontend ✅ GitHub Pages

### Private (Localhost Only)
- `admin/control-panel.html` - Admin panel ❌ Never deploy
- `../Event-Scraper-StandAlone/` - Scraper ❌ Never deploy
- `.env` - Credentials ❌ Never commit

### Configuration
- `.github/workflows/deploy-pages.yml` - Auto-deploy config
- `.gitignore` - Protects sensitive files
- `package.json` - Project metadata

---

## 🎉 Quick Start Summary

```bash
# 1. Clone repo (collaborators)
git clone https://github.com/dowdarts/AADSSTATSV2.git

# 2. Set up environment
cd aads-stats-v2
cp .env.example .env
# Edit .env with your Supabase credentials

# 3. Run admin panel (localhost)
cd admin
python -m http.server 8001

# 4. Run scraper (localhost)
cd ../../Event-Scraper-StandAlone
python api_server.py

# 5. View public frontend
# Live: https://dowdarts.github.io/AADSSTATSV2/
# Or locally: cd ../aads-stats-v2/public && python -m http.server 8000
```

Your AADS Stats Engine V2 is now deployed and ready! 🎯
