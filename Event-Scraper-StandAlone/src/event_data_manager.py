"""
Event Data Manager - Manages saving and loading event scraping data
Organizes data into folders with multiple formats (JSON, CSV, TXT)
"""

import os
import json
import csv
from datetime import datetime
from typing import Dict, List, Any
import logging

class EventDataManager:
    def __init__(self, base_dir: str = "event_data"):
        """Initialize the event data manager
        
        Args:
            base_dir: Base directory for storing event data
        """
        self.base_dir = base_dir
        self.logger = logging.getLogger(__name__)
        
        # Create base directory if it doesn't exist
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
            self.logger.info(f"Created event data directory: {self.base_dir}")
    
    def event_exists(self, event_id: str) -> bool:
        """Check if an event has already been saved
        
        Args:
            event_id: Event identifier
            
        Returns:
            True if event data exists
        """
        event_dir = os.path.join(self.base_dir, event_id)
        metadata_file = os.path.join(event_dir, "metadata.json")
        return os.path.exists(metadata_file)
    
    def get_existing_matches(self, event_id: str) -> List[Dict]:
        """Get list of existing matches for an event
        
        Args:
            event_id: Event identifier
            
        Returns:
            List of match dictionaries
        """
        event_dir = os.path.join(self.base_dir, event_id)
        raw_dir = os.path.join(event_dir, "raw_data")
        
        if not os.path.exists(raw_dir):
            return []
        
        # Find most recent matches JSON file
        matches_files = [f for f in os.listdir(raw_dir) if f.startswith('matches_') and f.endswith('.json')]
        if not matches_files:
            return []
        
        latest_file = sorted(matches_files)[-1]
        file_path = os.path.join(raw_dir, latest_file)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('matches', [])
        except Exception as e:
            self.logger.error(f"Error loading existing matches: {e}")
            return []
    
    def save_event_matches(self, event_id: str, matches: List[Dict], raw_api_response: Dict = None, event_number: int = None) -> str:
        """Save event matches in multiple formats
        
        Args:
            event_id: Event identifier (e.g., 'mt_joe6163l_1' or 'Event_1')
            matches: List of match dictionaries with 'url' and 'title'
            raw_api_response: Optional raw API response to save
            event_number: Optional event number (1-7)
            
        Returns:
            Path to the event directory
        """
        # Check if event already exists
        existing_matches = self.get_existing_matches(event_id)
        existing_urls = {m['url'] for m in existing_matches}
        
        # Filter out duplicates
        new_matches = [m for m in matches if m['url'] not in existing_urls]
        
        if existing_matches and not new_matches:
            self.logger.info(f"Event {event_id} already has all {len(existing_matches)} matches saved. Skipping duplicate save.")
            return os.path.join(self.base_dir, event_id)
        
        if existing_matches and new_matches:
            self.logger.info(f"Event {event_id}: Found {len(existing_matches)} existing matches, adding {len(new_matches)} new matches")
            # Merge: existing + new
            all_matches = existing_matches + new_matches
        else:
            all_matches = matches
        
        # Create event directory structure
        event_dir = os.path.join(self.base_dir, event_id)
        raw_dir = os.path.join(event_dir, "raw_data")
        csv_dir = os.path.join(event_dir, "csv")
        
        for dir_path in [event_dir, raw_dir, csv_dir]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. Save raw API response (if provided)
        if raw_api_response:
            raw_file = os.path.join(raw_dir, f"api_response_{timestamp}.json")
            with open(raw_file, 'w', encoding='utf-8') as f:
                json.dump(raw_api_response, f, indent=2)
            self.logger.info(f"Saved raw API response: {raw_file}")
        
        # 2. Save matches as JSON
        matches_json_file = os.path.join(raw_dir, f"matches_{timestamp}.json")
        with open(matches_json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'event_id': event_id,
                'timestamp': timestamp,
                'match_count': len(all_matches),
                'new_matches': len(new_matches) if existing_matches else len(all_matches),
                'matches': all_matches
            }, f, indent=2)
        self.logger.info(f"Saved matches JSON: {matches_json_file}")
        
        # 3. Save matches as CSV
        csv_file = os.path.join(csv_dir, f"matches_{timestamp}.csv")
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['match_number', 'match_type', 'phase', 'group_name', 'url', 'title', 'status', 'scraped_at'])
            writer.writeheader()
            for idx, match in enumerate(all_matches, 1):
                # Use match data from scraper if available, otherwise fallback to old logic
                match_type = match.get('match_type', 'Round Robin' if idx <= 20 else 'Knockout')
                phase = match.get('phase', 'round_robin' if idx <= 20 else 'quarterfinal')
                group_name = match.get('group_name', '')
                
                writer.writerow({
                    'match_number': match.get('match_number', idx),
                    'match_type': match_type,
                    'phase': phase,
                    'group_name': group_name if group_name else '',
                    'url': match['url'],
                    'title': match['title'],
                    'status': 'pending',
                    'scraped_at': ''
                })
        self.logger.info(f"Saved matches CSV: {csv_file}")
        
        # 4. Save match URLs as plain text list
        urls_file = os.path.join(event_dir, "match_urls.txt")
        with open(urls_file, 'w', encoding='utf-8') as f:
            f.write(f"Event: {event_id}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Matches: {len(all_matches)}\n")
            f.write(f"Round Robin: {min(20, len(all_matches))}\n")
            f.write(f"Knockout: {max(0, len(all_matches) - 20)}\n")
            f.write("-" * 80 + "\n\n")
            for i, match in enumerate(all_matches, 1):
                match_type = 'Round Robin' if i <= 20 else 'Knockout'
                f.write(f"{i}. [{match_type}] {match['title']}\n")
                f.write(f"   {match['url']}\n\n")
        self.logger.info(f"Saved match URLs: {urls_file}")
        
        # 5. Save metadata
        metadata_file = os.path.join(event_dir, "metadata.json")
        metadata = {
            'event_id': event_id,
            'created_at': timestamp,
            'match_count': len(all_matches),
            'round_robin_count': min(20, len(all_matches)),
            'knockout_count': max(0, len(all_matches) - 20),
            'last_updated': timestamp,
            'status': 'matches_found',
            'files': {
                'raw_api_response': os.path.basename(raw_file) if raw_api_response else None,
                'matches_json': os.path.basename(matches_json_file),
                'matches_csv': os.path.basename(csv_file),
                'match_urls': 'match_urls.txt'
            }
        }
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        self.logger.info(f"Saved metadata: {metadata_file}")
        
        return event_dir
    
    def load_pending_matches(self, event_id: str) -> List[Dict]:
        """Load pending matches from an event
        
        Args:
            event_id: Event identifier
            
        Returns:
            List of pending matches
        """
        event_dir = os.path.join(self.base_dir, event_id)
        csv_dir = os.path.join(event_dir, "csv")
        
        if not os.path.exists(csv_dir):
            return []
        
        # Find the most recent CSV file
        csv_files = [f for f in os.listdir(csv_dir) if f.startswith('matches_') and f.endswith('.csv')]
        if not csv_files:
            return []
        
        latest_csv = sorted(csv_files)[-1]
        csv_path = os.path.join(csv_dir, latest_csv)
        
        pending_matches = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['status'] == 'pending':
                    pending_matches.append({
                        'url': row['url'],
                        'title': row['title']
                    })
        
        return pending_matches
    
    def update_match_status(self, event_id: str, match_url: str, status: str, stats_data: Dict = None):
        """Update the status of a specific match
        
        Args:
            event_id: Event identifier
            match_url: URL of the match
            status: New status (e.g., 'completed', 'error')
            stats_data: Optional stats data from scraping
        """
        event_dir = os.path.join(self.base_dir, event_id)
        csv_dir = os.path.join(event_dir, "csv")
        
        if not os.path.exists(csv_dir):
            return
        
        # Find the most recent CSV file
        csv_files = [f for f in os.listdir(csv_dir) if f.startswith('matches_') and f.endswith('.csv')]
        if not csv_files:
            return
        
        latest_csv = sorted(csv_files)[-1]
        csv_path = os.path.join(csv_dir, latest_csv)
        
        # Read all rows
        rows = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                if row['url'] == match_url:
                    row['status'] = status
                    row['scraped_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                rows.append(row)
        
        # Write back
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        # Save stats data if provided
        if stats_data:
            stats_dir = os.path.join(event_dir, "stats")
            if not os.path.exists(stats_dir):
                os.makedirs(stats_dir)
            
            # Extract match ID from URL
            match_id = match_url.split('/')[-1]
            stats_file = os.path.join(stats_dir, f"{match_id}.json")
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats_data, f, indent=2)
    
    def get_event_summary(self, event_id: str) -> Dict:
        """Get summary of an event's scraping status
        
        Args:
            event_id: Event identifier
            
        Returns:
            Summary dictionary
        """
        event_dir = os.path.join(self.base_dir, event_id)
        metadata_file = os.path.join(event_dir, "metadata.json")
        
        if not os.path.exists(metadata_file):
            return {'error': 'Event not found'}
        
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # Count completed matches
        csv_dir = os.path.join(event_dir, "csv")
        completed = 0
        pending = 0
        
        if os.path.exists(csv_dir):
            csv_files = [f for f in os.listdir(csv_dir) if f.startswith('matches_') and f.endswith('.csv')]
            if csv_files:
                latest_csv = sorted(csv_files)[-1]
                csv_path = os.path.join(csv_dir, latest_csv)
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row['status'] == 'completed':
                            completed += 1
                        elif row['status'] == 'pending':
                            pending += 1
        
        return {
            'event_id': event_id,
            'total_matches': metadata['match_count'],
            'completed': completed,
            'pending': pending,
            'created_at': metadata['created_at'],
            'last_updated': metadata['last_updated'],
            'status': metadata['status']
        }
    
    def list_events(self) -> List[Dict]:
        """List all saved events
        
        Returns:
            List of event summaries
        """
        events = []
        
        if not os.path.exists(self.base_dir):
            return events
        
        for event_id in os.listdir(self.base_dir):
            event_path = os.path.join(self.base_dir, event_id)
            if os.path.isdir(event_path):
                summary = self.get_event_summary(event_id)
                if 'error' not in summary:
                    events.append(summary)
        
        return sorted(events, key=lambda x: x['created_at'], reverse=True)
