# Installation Checklist

Use this checklist to verify your event-scraper-app is properly set up.

## ☑️ Pre-Installation

- [ ] Python 3.8 or higher installed
  - Check: `python --version` or `python3 --version`
- [ ] pip package manager available
  - Check: `pip --version`
- [ ] Chrome browser installed (for Selenium)
- [ ] Internet connection active

## ☑️ Installation Steps

- [ ] Navigate to event-scraper-app directory
  ```bash
  cd event-scraper-app
  ```

- [ ] (Optional but recommended) Create virtual environment
  ```bash
  # Windows
  python -m venv venv
  venv\Scripts\activate
  
  # Linux/Mac
  python3 -m venv venv
  source venv/bin/activate
  ```

- [ ] Install Python dependencies
  ```bash
  pip install -r requirements.txt
  ```
  
- [ ] Verify installation
  ```bash
  python -c "import flask; import selenium; print('All dependencies installed!')"
  ```

## ☑️ First Run

- [ ] Start the API server
  ```bash
  # Option 1: Direct
  python api_server.py
  
  # Option 2: Startup script (Windows)
  start_server.bat
  
  # Option 3: Startup script (Linux/Mac)
  chmod +x start_server.sh
  ./start_server.sh
  ```

- [ ] Verify server is running
  - Look for: "Running on http://0.0.0.0:5000"
  - Server starts without errors

- [ ] Test web interface
  - [ ] Open browser to: http://localhost:5000
  - [ ] Event scraper page loads successfully
  - [ ] No red error alerts

- [ ] Test API endpoint
  ```bash
  curl http://localhost:5000/admin/health
  # Should return: {"status":"ok",...}
  ```

## ☑️ Test Scraping

- [ ] Test Stage 1: Find Matches
  - [ ] Enter a test event URL
  - [ ] Click "Find Matches"
  - [ ] Matches are discovered successfully
  - [ ] Download Stage 1 button appears

- [ ] Test Stage 2: Scrape Stats
  - [ ] Click "Scrape All Stats"
  - [ ] Progress bar updates
  - [ ] Matches turn green with "✓ X players"
  - [ ] Download Stage 2 button appears

- [ ] Verify Data Saved
  - [ ] Check `data/` directory exists
  - [ ] Check `data/aads_master_db.json` created
  - [ ] Check `data/event_data/{event_id}/` folder created
  - [ ] JSON, CSV, and TXT files present

## ☑️ Troubleshooting

If any step fails, check:

### Python not found
- [ ] Install Python from python.org
- [ ] Add Python to PATH
- [ ] Try `python3` instead of `python`

### pip install fails
- [ ] Run as administrator (Windows) or with sudo (Linux)
- [ ] Update pip: `pip install --upgrade pip`
- [ ] Try: `pip install -r requirements.txt --user`

### Chrome driver error
- [ ] Install Chrome browser
- [ ] Run: `pip install --upgrade webdriver-manager`
- [ ] Check internet connection (downloads driver automatically)

### Port 5000 in use
- [ ] Edit `api_server.py`, change port to 5001
- [ ] Or stop other service using port 5000

### Server won't start
- [ ] Check all dependencies installed
- [ ] Look for error messages in console
- [ ] Verify data directory permissions

### Can't find matches
- [ ] Check event URL is correct format
- [ ] Verify event has completed matches
- [ ] Check internet connection
- [ ] Try different event URL

## ☑️ Configuration (Optional)

- [ ] Copy `.env.example` to `.env`
  ```bash
  cp config/.env.example .env
  ```

- [ ] Edit `.env` for custom settings
  - Port number
  - Selenium settings
  - Delay timing
  - Log level

- [ ] Review `config/config.json` for advanced options

## ☑️ Integration Test (Optional)

- [ ] Test Python module import
  ```python
  from src.scraper import DartConnectScraper
  from src.database_manager import AADSDataManager
  print("Import successful!")
  ```

- [ ] Test REST API call
  ```bash
  curl -X POST http://localhost:5000/api/scrape_event \
    -H "Content-Type: application/json" \
    -d '{"event_url":"https://tv.dartconnect.com/eventmenu/mt_joe6163l_1"}'
  ```

- [ ] Test data export
  ```bash
  # Check JSON database
  cat data/aads_master_db.json
  
  # Check CSV export
  ls data/event_data/*/csv/*.csv
  ```

## ✅ Complete!

Once all checkboxes are checked, your event-scraper-app is fully functional!

## 📚 Next Steps

- [ ] Read README.md for detailed documentation
- [ ] Review QUICKSTART.md for quick reference
- [ ] Check INTEGRATION_GUIDE.md for using in other projects
- [ ] Review PROJECT_SUMMARY.md for complete feature list

## 🆘 Still Having Issues?

1. Check logs in terminal output
2. Review docs/ folder for help
3. Try test event URL: `https://tv.dartconnect.com/eventmenu/mt_joe6163l_1`
4. Restart server and try again

---

**Happy Scraping! 🎯**
