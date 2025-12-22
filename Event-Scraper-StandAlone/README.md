# Event Scraper Application

A standalone event scraper application for extracting dart match data from DartConnect events. This tool automates the process of finding and scraping match statistics, making it easy to collect comprehensive tournament data.

## Features

- 🔍 **Automatic Match Discovery**: Finds all matches from a DartConnect event URL
- ⚡ **Batch Scraping**: Scrapes multiple matches with rate limiting
- 💾 **Multiple Export Formats**: Saves data in JSON, CSV, and plain text
- 📊 **Real-time Progress**: Live progress tracking with detailed logs
- 🔄 **Duplicate Prevention**: Automatically detects and skips duplicate matches
- 📤 **Import/Export**: Download and upload scraping data for offline processing

## Requirements

- Python 3.8 or higher
- Chrome browser (for Selenium automation)
- Internet connection

## Installation

### Quick Start

1. **Clone or download this directory**
   ```bash
   cd event-scraper-app
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server**
   ```bash
   python api_server.py
   ```

4. **Open the web interface**
   - Open your browser to: `http://localhost:5000`
   - Or open `event_scraper.html` directly

### Detailed Setup

#### Windows

```powershell
# Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python api_server.py
```

#### Linux/Mac

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python api_server.py
```

## Usage

### Web Interface (Recommended)

1. **Start the API server**:
   ```bash
   python api_server.py
   ```

2. **Open your browser** to `http://localhost:5000`

3. **Stage 1: Find Matches**
   - Enter a DartConnect event URL (e.g., `https://tv.dartconnect.com/eventmenu/mt_joe6163l_1`)
   - Click "Find Matches"
   - Wait for the scraper to discover all match URLs
   - Download Stage 1 data if needed

4. **Stage 2: Scrape Statistics**
   - Click "Scrape All Stats" to extract player statistics from all matches
   - Monitor progress in real-time
   - Download Stage 2 data when complete

### Python API Usage

```python
from src.database_manager import AADSDataManager
from src.scraper import DartConnectScraper
from src.event_data_manager import EventDataManager

# Initialize managers
db_manager = AADSDataManager()
event_manager = EventDataManager()
scraper = DartConnectScraper(db_manager)

# Scrape an event for matches
result = scraper.scrape_event_for_matches("https://tv.dartconnect.com/eventmenu/mt_joe6163l_1")

if result['success']:
    event_id = result['event_id']
    matches = result['matches']
    
    # Save matches
    event_manager.save_event_matches(event_id, matches, result.get('raw_response'))
    
    # Scrape individual matches
    for match in matches:
        players_stats = scraper.extract_player_stats_from_recap(match['url'])
        for player in players_stats:
            db_manager.add_match_stats(
                player_name=player['player_name'],
                event_id=event_id,
                match_url=match['url'],
                stats_dict=player
            )
```

## API Endpoints

### POST /api/scrape_event
Scrape an event page to find all match URLs.

**Request:**
```json
{
  "event_url": "https://tv.dartconnect.com/eventmenu/mt_joe6163l_1"
}
```

**Response:**
```json
{
  "success": true,
  "event_id": "mt_joe6163l_1",
  "matches": [...],
  "saved_to": "data/event_data/mt_joe6163l_1",
  "progress_log": [...]
}
```

### POST /api/scrape_recap
Scrape a single match recap URL.

**Request:**
```json
{
  "recap_url": "https://recap.dartconnect.com/matches/688e0078f4fc02e124e712ee",
  "event_id": "mt_joe6163l_1"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Added stats for 2 players",
  "players_added": 2,
  "players": [...]
}
```

### POST /api/upload_stage2
Upload Stage 2 data (scraped stats) to database.

**Request:**
```json
{
  "event_id": "mt_joe6163l_1",
  "stats": [...]
}
```

### GET /api/events
Get list of all scraped events.

### GET /api/stats
Get all player statistics from database.

### GET /admin/health
Health check endpoint.

## Directory Structure

```
event-scraper-app/
├── api_server.py           # Flask API server
├── event_scraper.html      # Web interface
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── src/                   # Source code
│   ├── database_manager.py      # Database operations
│   ├── scraper.py              # Core scraping logic
│   └── event_data_manager.py   # Event data management
├── data/                  # Data storage (created automatically)
│   ├── aads_master_db.json    # Main database
│   └── event_data/            # Event-specific data
│       └── {event_id}/        # Per-event folders
│           ├── metadata.json
│           ├── match_urls.txt
│           ├── raw_data/      # Raw API responses
│           ├── csv/           # CSV exports
│           └── stats/         # Individual match stats
├── config/                # Configuration files
└── docs/                  # Additional documentation
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Server Configuration
FLASK_ENV=development
FLASK_DEBUG=True
API_PORT=5000

# Data Directories
DATA_DIR=data
EVENT_DATA_DIR=data/event_data

# Scraper Configuration
USE_SELENIUM=True
SCRAPER_DELAY_MS=200
LOG_LEVEL=INFO
```

### Config File

Create `config/config.json`:

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": true
  },
  "scraper": {
    "use_selenium": true,
    "delay_between_requests_ms": 200,
    "max_retries": 3,
    "timeout_seconds": 30
  },
  "data": {
    "base_dir": "data",
    "event_data_dir": "data/event_data",
    "backup_enabled": true
  }
}
```

## Data Formats

### Stage 1: Match Discovery

Saved as JSON with structure:
```json
{
  "version": "1.0",
  "stage": 1,
  "event_id": "mt_joe6163l_1",
  "timestamp": "2025-12-20T03:03:41",
  "matches": [
    {
      "url": "https://recap.dartconnect.com/matches/...",
      "title": "Match 1 - Player A vs Player B",
      "match_number": 1,
      "match_type": "Round Robin"
    }
  ]
}
```

### Stage 2: Player Statistics

Saved as JSON with structure:
```json
{
  "version": "1.0",
  "stage": 2,
  "event_id": "mt_joe6163l_1",
  "stats": [
    {
      "match_url": "...",
      "players": [
        {
          "player_name": "John Doe",
          "three_dart_average": 78.45,
          "legs_played": 5,
          "count_180s": 2,
          "count_140_plus": 8,
          "highest_finish": 120
        }
      ]
    }
  ]
}
```

## Troubleshooting

### Chrome Driver Issues

If you get Chrome driver errors:

```bash
# Manually install webdriver-manager
pip install --upgrade webdriver-manager

# Or disable Selenium in config
USE_SELENIUM=False
```

### Port Already in Use

Change the port in `api_server.py`:

```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Changed to 5001
```

### Permission Errors

Make sure the data directory is writable:

```bash
chmod -R 755 data/
```

## Integration with Other Projects

This scraper can be easily integrated into other projects:

### As a Python Module

```python
# Add to your project
import sys
sys.path.append('path/to/event-scraper-app')

from src.scraper import DartConnectScraper
from src.database_manager import AADSDataManager

# Use in your code
db = AADSDataManager(db_file="your_database.json")
scraper = DartConnectScraper(db)
```

### As a Microservice

Run the API server and call it from any application:

```javascript
// From JavaScript/Node.js
const response = await fetch('http://localhost:5000/api/scrape_event', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ event_url: eventUrl })
});
```

```python
# From Python
import requests

response = requests.post('http://localhost:5000/api/scrape_event', json={
    'event_url': event_url
})
```

### Data Export

Export data for use in other applications:

```bash
# Data is automatically saved in multiple formats:
# - JSON: data/event_data/{event_id}/raw_data/matches_*.json
# - CSV: data/event_data/{event_id}/csv/matches_*.csv
# - Text: data/event_data/{event_id}/match_urls.txt
```

## Performance Tips

- **Batch Processing**: Use "Scrape All" for best performance
- **Rate Limiting**: Default 200ms delay prevents rate limiting
- **Caching**: Duplicate matches are automatically skipped
- **Selenium**: Required for JavaScript-rendered pages

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Code Style

```bash
# Format code
black src/

# Lint code
flake8 src/
```

## License

This is a standalone application designed for data collection from public DartConnect events. Please respect DartConnect's terms of service and rate limits.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Check logs in the console output
4. Open an issue on GitHub

## Changelog

### Version 1.0.0 (2025-12-20)
- Initial standalone release
- Event discovery via DartConnect API
- Batch match scraping
- Multiple export formats
- Web interface
- Stage 1/2 data persistence
- Import/export functionality
