# Event Scraper App

**Standalone event scraper for DartConnect tournaments**

## 📦 What's Inside

A complete, portable application for scraping dart match data from DartConnect events.

## ⚡ Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Run server: `python api_server.py`
3. Open browser: `http://localhost:5000`
4. Paste event URL and scrape!

## 🎯 Features

- ✅ Automatic match discovery
- ✅ Batch scraping with progress tracking
- ✅ Multiple export formats (JSON, CSV, TXT)
- ✅ Web interface included
- ✅ REST API for integrations
- ✅ Duplicate prevention
- ✅ Rate limiting
- ✅ Error recovery

## 📁 Structure

```
event-scraper-app/
├── api_server.py          # Flask API server
├── event_scraper.html     # Web interface
├── requirements.txt       # Dependencies
├── start_server.bat       # Windows startup
├── start_server.sh        # Linux/Mac startup
├── src/                   # Source code
│   ├── scraper.py
│   ├── database_manager.py
│   └── event_data_manager.py
├── data/                  # Auto-created data storage
├── config/                # Configuration examples
└── docs/                  # Documentation
```

## 📖 Documentation

- [README.md](README.md) - Full documentation
- [QUICKSTART.md](QUICKSTART.md) - 5-minute setup guide
- [docs/INTEGRATION_GUIDE.md](docs/INTEGRATION_GUIDE.md) - Integration examples

## 🔧 Requirements

- Python 3.8+
- Chrome browser (for Selenium)
- Internet connection

## 💾 Data Output

All scraped data is saved in multiple formats:
- **JSON**: Structured data with full details
- **CSV**: Spreadsheet-compatible format  
- **TXT**: Plain text match lists
- **Database**: SQLite-like JSON database

## 🚀 Use Cases

- Collect tournament statistics
- Build analytics dashboards
- Track player performance
- Export data for other tools
- Automate data collection
- Research and analysis

## 🔌 Integration

Can be used as:
- **Python module** - Import directly
- **REST API** - Microservice
- **CLI tool** - Command line
- **Docker container** - Containerized deployment

## 📝 License

Standalone application for educational and research purposes.

## 🤝 Contributing

This is a standalone, portable application. Feel free to modify and adapt for your needs.

---

**Ready to start?** See [QUICKSTART.md](QUICKSTART.md) for a 5-minute setup guide!
