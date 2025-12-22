# Integration Guide

## Using Event Scraper in Your Project

The Event Scraper can be integrated into your applications in several ways:

## Method 1: Python Module

### Import and Use Directly

```python
import sys
sys.path.append('path/to/event-scraper-app')

from src.database_manager import AADSDataManager
from src.scraper import DartConnectScraper
from src.event_data_manager import EventDataManager

# Initialize
db = AADSDataManager(db_file="your_data/database.json")
event_mgr = EventDataManager(base_dir="your_data/events")
scraper = DartConnectScraper(db)

# Scrape an event
result = scraper.scrape_event_for_matches(event_url)
if result['success']:
    event_id = result['event_id']
    matches = result['matches']
    
    # Save matches
    event_mgr.save_event_matches(event_id, matches)
    
    # Scrape stats
    for match in matches:
        stats = scraper.extract_player_stats_from_recap(match['url'])
        for player in stats:
            db.add_match_stats(
                player_name=player['player_name'],
                event_id=event_id,
                match_url=match['url'],
                stats_dict=player
            )
```

## Method 2: REST API (Microservice)

### Start the Server

```bash
python api_server.py
```

### Call from Any Language

#### JavaScript/Node.js

```javascript
async function scrapeEvent(eventUrl) {
  const response = await fetch('http://localhost:5000/api/scrape_event', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ event_url: eventUrl })
  });
  
  const data = await response.json();
  return data;
}

async function scrapeMatch(recapUrl, eventId) {
  const response = await fetch('http://localhost:5000/api/scrape_recap', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      recap_url: recapUrl,
      event_id: eventId
    })
  });
  
  const data = await response.json();
  return data;
}

// Usage
const eventResult = await scrapeEvent('https://tv.dartconnect.com/eventmenu/mt_joe6163l_1');
console.log(`Found ${eventResult.matches.length} matches`);

for (const match of eventResult.matches) {
  const stats = await scrapeMatch(match.url, eventResult.event_id);
  console.log(`Scraped ${stats.players_added} players from ${match.title}`);
}
```

#### Python

```python
import requests

def scrape_event(event_url):
    response = requests.post(
        'http://localhost:5000/api/scrape_event',
        json={'event_url': event_url}
    )
    return response.json()

def scrape_match(recap_url, event_id):
    response = requests.post(
        'http://localhost:5000/api/scrape_recap',
        json={
            'recap_url': recap_url,
            'event_id': event_id
        }
    )
    return response.json()

# Usage
result = scrape_event('https://tv.dartconnect.com/eventmenu/mt_joe6163l_1')
print(f"Found {len(result['matches'])} matches")

for match in result['matches']:
    stats = scrape_match(match['url'], result['event_id'])
    print(f"Scraped {stats['players_added']} players")
```

#### cURL

```bash
# Scrape event
curl -X POST http://localhost:5000/api/scrape_event \
  -H "Content-Type: application/json" \
  -d '{"event_url": "https://tv.dartconnect.com/eventmenu/mt_joe6163l_1"}'

# Scrape match
curl -X POST http://localhost:5000/api/scrape_recap \
  -H "Content-Type: application/json" \
  -d '{"recap_url": "https://recap.dartconnect.com/matches/xxx", "event_id": "mt_joe6163l_1"}'

# Get all stats
curl http://localhost:5000/api/stats

# Get all events
curl http://localhost:5000/api/events
```

## Method 3: Data Export

### Export Formats

The scraper automatically saves data in multiple formats:

```
data/event_data/{event_id}/
├── metadata.json          # Event metadata
├── match_urls.txt        # Plain text list
├── raw_data/
│   ├── matches_*.json    # Match list
│   └── api_response_*.json  # Raw API data
├── csv/
│   └── matches_*.csv     # CSV format
└── stats/
    └── {match_id}.json   # Individual match stats
```

### Read Exported Data

```python
import json
import csv

# Read JSON
with open('data/event_data/mt_joe6163l_1/raw_data/matches_20251220.json') as f:
    data = json.load(f)
    matches = data['matches']

# Read CSV
with open('data/event_data/mt_joe6163l_1/csv/matches_20251220.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['url'], row['title'])

# Read database
with open('data/aads_master_db.json') as f:
    database = json.load(f)
    players = database['players']
    events = database['events']
```

## Method 4: Docker Container

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Copy application
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create data directories
RUN mkdir -p data/event_data

EXPOSE 5000

CMD ["python", "api_server.py"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  event-scraper:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
    environment:
      - FLASK_ENV=production
      - USE_SELENIUM=True
```

### Usage

```bash
# Build
docker build -t event-scraper .

# Run
docker run -p 5000:5000 -v $(pwd)/data:/app/data event-scraper

# Or with docker-compose
docker-compose up
```

## Best Practices

### Rate Limiting

```python
import time

for match in matches:
    stats = scraper.extract_player_stats_from_recap(match['url'])
    # Wait 200ms between requests to avoid rate limiting
    time.sleep(0.2)
```

### Error Handling

```python
try:
    result = scraper.scrape_event_for_matches(event_url)
    if result['success']:
        # Process matches
        pass
    else:
        print(f"Error: {result['error']}")
except Exception as e:
    print(f"Exception: {e}")
```

### Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Scraper will use your logging configuration
scraper = DartConnectScraper(db, log_level=logging.INFO)
```

## Example Projects

### 1. Tournament Stats Dashboard

```python
# Scrape tournament data
result = scraper.scrape_event_for_matches(event_url)

# Get all player stats
stats = db.get_all_stats()

# Display in web dashboard
@app.route('/dashboard')
def dashboard():
    players = stats['players']
    return render_template('dashboard.html', players=players)
```

### 2. Automated Daily Scraper

```python
import schedule

def scrape_daily_events():
    events = get_todays_events()  # Your function
    for event_url in events:
        result = scraper.scrape_event_for_matches(event_url)
        # Process matches...

schedule.every().day.at("01:00").do(scrape_daily_events)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### 3. Analytics Pipeline

```python
# Extract
result = scraper.scrape_event_for_matches(event_url)

# Transform
for match in result['matches']:
    stats = scraper.extract_player_stats_from_recap(match['url'])
    # Calculate additional metrics
    for player in stats:
        player['efficiency'] = calculate_efficiency(player)

# Load
save_to_data_warehouse(stats)
```

## Support

For integration questions:
- Check the API documentation
- Review example code
- Open an issue on GitHub
