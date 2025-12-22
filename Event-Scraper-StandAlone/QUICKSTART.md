# Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies (2 minutes)

```bash
# Windows
python -m pip install -r requirements.txt

# Linux/Mac
python3 -m pip install -r requirements.txt
```

### 2. Start the Server (1 minute)

```bash
# Windows
start_server.bat

# Linux/Mac
chmod +x start_server.sh
./start_server.sh

# Or directly
python api_server.py
```

### 3. Open Web Interface (1 minute)

Open your browser to: **http://localhost:5000**

### 4. Scrape Your First Event (1 minute)

1. Paste a DartConnect event URL
2. Click "Find Matches"
3. Click "Scrape All Stats"
4. Done! Download your data

## Common Event URLs

DartConnect event URLs look like:
```
https://tv.dartconnect.com/eventmenu/mt_joe6163l_1
https://tv.dartconnect.com/event/mt_joe6163l_1
https://tv.dartconnect.com/event/mt_joe6163l_1/matches
```

## Troubleshooting

### Server won't start
- Make sure Python 3.8+ is installed
- Install dependencies: `pip install -r requirements.txt`
- Check if port 5000 is available

### Chrome driver errors
- Selenium will auto-download Chrome driver
- Make sure Chrome browser is installed
- Or set `USE_SELENIUM=False` in config

### Can't find matches
- Check the event URL is correct
- Make sure the event has completed matches
- Check your internet connection

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) for API details
- See [INTEGRATION_GUIDE.md](docs/INTEGRATION_GUIDE.md) for using in your projects
