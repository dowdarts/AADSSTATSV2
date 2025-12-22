# AADS Stats V2 - Integration Guide

## 🔗 Integrating with Your Existing Scraper

This guide shows how to connect your existing Event Scraper (`Event-Scraper-StandAlone`) with the new AADS Stats V2 platform.

## Architecture Overview

```
┌─────────────────────┐
│  Event Scraper      │
│  (Existing)         │
└──────────┬──────────┘
           │ Scraped Data
           ▼
┌─────────────────────┐
│  Data Migration     │
│  Script (New)       │
└──────────┬──────────┘
           │ Validated Data
           ▼
┌─────────────────────┐
│  Supabase Staging   │
│  (Pending Review)   │
└──────────┬──────────┘
           │ Admin Approval
           ▼
┌─────────────────────┐
│  Supabase Production│
│  (Public Data)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Frontend Display   │
│  (Public Access)    │
└─────────────────────┘
```

## Step 1: Update Your Scraper Output

Modify your scraper to output data in the expected format:

### Required Fields

```python
match_data = {
    # Event Information
    'event_id': 'uuid',           # From events table
    'event_number': 1,             # 1-7
    
    # Match Details
    'phase': 'round_robin',        # 'round_robin', 'quarterfinal', 'semifinal', 'final'
    'group_name': 'A',             # 'A', 'B', or None for knockouts
    'match_number': 1,             # Sequential match number
    
    # Player Information
    'player_1_name': 'John Doe',
    'player_2_name': 'Jane Smith',
    
    # Scores
    'player_1_legs': 5,
    'player_2_legs': 3,
    'player_1_sets': 1,            # Optional
    'player_2_sets': 0,            # Optional
    
    # Statistics
    'player_1_average': 85.5,      # 3-Dart Average
    'player_2_average': 78.3,
    'player_1_highest_checkout': 120,
    'player_2_highest_checkout': 100,
    'player_1_180s': 2,
    'player_2_180s': 1,
    
    # Metadata
    'match_date': '2025-12-22T19:00:00',
    'board_number': 1,
    'source': 'scraper'
}
```

## Step 2: Modify Your Scraper Script

Add integration to your existing `scraper.py`:

```python
import sys
import os

# Add path to AADS Stats V2
sys.path.append('../aads-stats-v2')

from scripts.data_migration import AADSDataMigration
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../aads-stats-v2/.env')

class EventScraper:
    def __init__(self):
        # Your existing scraper initialization
        self.migrator = AADSDataMigration(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        
    def scrape_match(self, match_element):
        # Your existing scraping logic
        match_data = {
            # Extract data from match_element
            'player_1_name': self.extract_player_1_name(match_element),
            'player_2_name': self.extract_player_2_name(match_element),
            # ... etc
        }
        
        # Send to staging
        result = self.migrator.process_scraped_match(match_data)
        
        if result['success']:
            print(f"✅ Match sent to staging: {result['staging_id']}")
        else:
            print(f"❌ Error: {result['error']}")
```

## Step 3: Batch Processing

For bulk imports, use the batch processor:

```python
def scrape_event(event_url):
    """Scrape entire event and batch process"""
    matches = []
    
    # Scrape all matches
    for match_element in match_elements:
        match_data = extract_match_data(match_element)
        matches.append(match_data)
    
    # Batch process
    results = migrator.bulk_process_matches(matches)
    
    print(f"Processed: {results['successful']}/{results['total']}")
    print(f"Failed: {results['failed']}")
    
    if results['errors']:
        for error in results['errors']:
            print(f"Error: {error}")
```

## Step 4: Create Event Before Scraping

Before scraping matches, ensure the event exists:

```python
def create_or_get_event(event_number, event_name, event_date):
    """Create event if it doesn't exist"""
    event_id = migrator.get_or_create_event(
        event_number=event_number,
        event_name=event_name,
        event_date=event_date
    )
    return event_id

# Example usage
event_id = create_or_get_event(
    event_number=1,
    event_name="AADS Event 1 - Season 2025",
    event_date="2025-01-15"
)
```

## Step 5: Automated Scraping Workflow

### Complete Integration Example

```python
"""
Enhanced Event Scraper with AADS Stats V2 Integration
"""

import sys
sys.path.append('../aads-stats-v2')

from scripts.data_migration import AADSDataMigration
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv('../aads-stats-v2/.env')

class AADSEventScraper:
    def __init__(self):
        self.migrator = AADSDataMigration(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
    
    def scrape_full_event(self, event_url, event_number, event_name):
        """
        Scrape entire event and send to staging
        """
        print(f"🎯 Scraping Event {event_number}: {event_name}")
        
        # Step 1: Create/Get Event
        event_date = datetime.now().date().isoformat()
        event_id = self.migrator.get_or_create_event(
            event_number=event_number,
            event_name=event_name,
            event_date=event_date
        )
        
        if not event_id:
            print("❌ Failed to create/get event")
            return
        
        print(f"✅ Event ID: {event_id}")
        
        # Step 2: Scrape Round Robin Matches
        print("\n📊 Scraping Round Robin...")
        rr_matches = self.scrape_round_robin(event_url, event_id)
        
        # Step 3: Scrape Knockout Matches (if available)
        print("\n🏆 Scraping Knockouts...")
        ko_matches = self.scrape_knockouts(event_url, event_id)
        
        # Step 4: Batch Process All Matches
        all_matches = rr_matches + ko_matches
        results = self.migrator.bulk_process_matches(all_matches)
        
        # Step 5: Report Results
        print(f"\n✅ Successfully processed: {results['successful']}")
        print(f"❌ Failed: {results['failed']}")
        
        if results['errors']:
            print("\n⚠️  Errors:")
            for error in results['errors']:
                print(f"  - {error}")
        
        return results
    
    def scrape_round_robin(self, event_url, event_id):
        """Your existing RR scraping logic"""
        matches = []
        
        # Group A
        for match in self.scrape_group_matches(event_url, 'A'):
            match['event_id'] = event_id
            match['phase'] = 'round_robin'
            match['group_name'] = 'A'
            matches.append(match)
        
        # Group B
        for match in self.scrape_group_matches(event_url, 'B'):
            match['event_id'] = event_id
            match['phase'] = 'round_robin'
            match['group_name'] = 'B'
            matches.append(match)
        
        return matches
    
    def scrape_knockouts(self, event_url, event_id):
        """Your existing knockout scraping logic"""
        matches = []
        
        for phase in ['quarterfinal', 'semifinal', 'final']:
            phase_matches = self.scrape_phase_matches(event_url, phase)
            for match in phase_matches:
                match['event_id'] = event_id
                match['phase'] = phase
                match['group_name'] = None
                matches.append(match)
        
        return matches
    
    def scrape_group_matches(self, event_url, group_name):
        """Implement your group scraping logic"""
        # Your existing code here
        pass
    
    def scrape_phase_matches(self, event_url, phase):
        """Implement your phase scraping logic"""
        # Your existing code here
        pass


# Usage
if __name__ == '__main__':
    scraper = AADSEventScraper()
    
    # Scrape an event
    scraper.scrape_full_event(
        event_url='https://example.com/event/1',
        event_number=1,
        event_name='AADS Event 1 - January 2025'
    )
```

## Step 6: Schedule Automated Scraping

### Option A: Windows Task Scheduler

Create `run_scraper.bat`:

```batch
@echo off
cd C:\path\to\Event-Scraper-StandAlone
python scraper.py
```

Schedule in Task Scheduler to run after each event.

### Option B: Python Scheduler

```python
import schedule
import time

def scrape_job():
    scraper = AADSEventScraper()
    scraper.scrape_full_event(
        event_url=os.getenv('EVENT_URL'),
        event_number=1,
        event_name='AADS Event 1'
    )

# Run every Saturday at 8 PM
schedule.every().saturday.at("20:00").do(scrape_job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Step 7: Error Handling

Add robust error handling:

```python
def safe_scrape(self, event_url, event_number, event_name):
    """Scrape with error recovery"""
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            return self.scrape_full_event(event_url, event_number, event_name)
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print("🔄 Retrying in 30 seconds...")
                time.sleep(30)
            else:
                print("❌ All retries exhausted")
                # Send notification email
                self.send_error_notification(str(e))
                raise
```

## Step 8: Data Validation

Add validation before sending to staging:

```python
def validate_match_data(match_data):
    """Validate match data before staging"""
    required = ['player_1_name', 'player_2_name', 'player_1_legs', 'player_2_legs']
    
    for field in required:
        if field not in match_data or match_data[field] is None:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate scores
    if match_data['player_1_legs'] < 0 or match_data['player_2_legs'] < 0:
        raise ValueError("Invalid leg scores")
    
    # Validate averages
    if match_data.get('player_1_average', 0) > 200:
        raise ValueError("Unrealistic average detected")
    
    return True
```

## API Reference

### AADSDataMigration Class

#### `process_scraped_match(match_data: Dict) -> Dict`
Process single match and send to staging.

**Returns:**
```python
{
    'success': True,
    'staging_id': 'uuid',
    'message': 'Match added to staging queue'
}
```

#### `bulk_process_matches(matches: List[Dict]) -> Dict`
Process multiple matches in bulk.

**Returns:**
```python
{
    'total': 10,
    'successful': 9,
    'failed': 1,
    'errors': [...]
}
```

#### `get_or_create_player(player_name: str) -> str`
Get player UUID or create if doesn't exist.

#### `get_or_create_event(event_number, event_name, event_date) -> str`
Get event UUID or create if doesn't exist.

## Testing Your Integration

### Test Script

```python
def test_integration():
    """Test scraper integration"""
    migrator = AADSDataMigration(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )
    
    # Test data
    test_match = {
        'event_id': 'test-event-id',
        'phase': 'round_robin',
        'group_name': 'A',
        'player_1_name': 'Test Player 1',
        'player_2_name': 'Test Player 2',
        'player_1_legs': 5,
        'player_2_legs': 3,
        'player_1_average': 85.0,
        'player_2_average': 80.0,
    }
    
    result = migrator.process_scraped_match(test_match)
    assert result['success'], f"Test failed: {result.get('error')}"
    print("✅ Integration test passed!")

if __name__ == '__main__':
    test_integration()
```

## Troubleshooting

### Issue: Player names not matching

**Solution**: Implement name normalization:

```python
def normalize_player_name(name):
    """Normalize player names for consistency"""
    return name.strip().title()

match_data['player_1_name'] = normalize_player_name(raw_name)
```

### Issue: Duplicate matches in staging

**Solution**: Check for duplicates before inserting:

```python
def check_duplicate(self, match_data):
    """Check if match already exists in staging"""
    result = self.supabase.table('staging_matches')\
        .select('id')\
        .eq('event_id', match_data['event_id'])\
        .eq('player_1_name', match_data['player_1_name'])\
        .eq('player_2_name', match_data['player_2_name'])\
        .execute()
    
    return len(result.data) > 0
```

## Next Steps

1. ✅ Update your scraper output format
2. ✅ Test integration with sample data
3. ✅ Run full event scrape
4. ✅ Review data in admin control panel
5. ✅ Approve/reject staging matches
6. ✅ Verify public frontend display
7. ✅ Set up automated scheduling

## Support

For integration assistance, check:
- [Main README](README.md)
- Database schema in `supabase/migrations/`
- Example scripts in `scripts/`
