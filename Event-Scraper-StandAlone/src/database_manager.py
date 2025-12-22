"""
AADS Database Manager - Handles all data operations for player stats
Maintains player statistics across 7-event AADS series
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class AADSDataManager:
    def __init__(self, db_file: str = "data/aads_master_db.json"):
        """Initialize the database manager with the JSON file path"""
        self.db_file = db_file
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.db_file) if os.path.dirname(self.db_file) else ".", exist_ok=True)
        self.data = self._load_database()
        
    def _load_database(self) -> Dict[str, Any]:
        """Load database from JSON file or create new if not exists"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Ensure all required keys exist
                    if 'players' not in data:
                        data['players'] = {}
                    if 'events' not in data:
                        data['events'] = {}
                    if 'metadata' not in data:
                        data['metadata'] = {
                            'last_updated': datetime.now().isoformat(),
                            'total_matches': 0,
                            'version': '1.0.0'
                        }
                    return data
            except (json.JSONDecodeError, FileNotFoundError):
                print(f"Warning: Could not load {self.db_file}, creating new database")
                
        # Create new database structure
        return {
            'players': {},
            'events': {},
            'metadata': {
                'last_updated': datetime.now().isoformat(),
                'total_matches': 0,
                'version': '1.0.0',
                'series_info': {
                    'qualifying_events': 6,
                    'championship_event': 1,
                    'current_event': 1
                }
            }
        }
    
    def _save_database(self) -> bool:
        """Save current data to JSON file"""
        try:
            self.data['metadata']['last_updated'] = datetime.now().isoformat()
            
            # Convert sets to lists for JSON serialization
            for player_name, player_data in self.data['players'].items():
                if isinstance(player_data.get('events_played'), set):
                    player_data['events_played'] = list(player_data['events_played'])
            
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving database: {e}")
            return False
    
    def add_match_stats(self, player_name: str, event_id: str, stats_dict: Dict[str, Any] = None, match_url: str = None, **kwargs) -> bool:
        """Add or update player stats for a specific match
        
        Args:
            player_name: Player's name
            event_id: Event identifier
            stats_dict: Dictionary of statistics (or use kwargs for individual fields)
            match_url: Optional match URL to prevent duplicates
            **kwargs: Individual stat fields (alternative to stats_dict)
            
        Returns:
            True if stats were added, False if duplicate or error
        """
        try:
            # Merge stats_dict and kwargs
            if stats_dict is None:
                stats_dict = kwargs
            else:
                stats_dict = {**stats_dict, **kwargs}
            
            # Check for duplicate match if URL provided
            if match_url:
                if 'scraped_matches' not in self.data:
                    self.data['scraped_matches'] = []
                
                # Check if this match was already scraped
                if match_url in self.data['scraped_matches']:
                    print(f"Match {match_url} already scraped for {player_name}. Skipping to prevent double-counting.")
                    return False
                
                # Mark this match as scraped
                self.data['scraped_matches'].append(match_url)
            
            # Normalize player name
            player_name = player_name.strip()
            
            # Initialize player if doesn't exist
            if player_name not in self.data['players']:
                self.data['players'][player_name] = {
                    'name': player_name,
                    'total_legs': 0,
                    'total_score': 0.0,  # Sum of all individual leg averages
                    'total_matches': 0,
                    'matches_won': 0,
                    'total_180s': 0,
                    'total_160_plus': 0,
                    'total_140_plus': 0,
                    'total_100_plus': 0,
                    'highest_finish': 0,
                    'total_double_attempts': 0,
                    'total_doubles_hit': 0,
                    'events_played': set(),  # Use set to avoid duplicates
                    'event_history': [],
                    'qualified_for_toc': False,
                    'event_wins': []
                }
            
            player = self.data['players'][player_name]
            
            # Add event to events played (will be converted to list when saving)
            if isinstance(player['events_played'], list):
                player['events_played'] = set(player['events_played'])
            player['events_played'].add(event_id)
            
            # Update stats
            legs_played = stats_dict.get('legs_played', 1)
            three_dart_avg = stats_dict.get('three_dart_average', 0.0)
            
            # Accumulate stats for weighted average calculation
            player['total_legs'] += legs_played
            player['total_score'] += (three_dart_avg * legs_played)  # Weighted by legs
            
            # Match stats
            player['total_matches'] += stats_dict.get('matches_played', 1)
            player['matches_won'] += stats_dict.get('match_won', 0)
            
            # Score counts
            player['total_180s'] += stats_dict.get('count_180s', 0)
            player['total_160_plus'] += stats_dict.get('count_160_plus', 0)
            player['total_140_plus'] += stats_dict.get('count_140_plus', 0)
            player['total_100_plus'] += stats_dict.get('count_100_plus', 0)
            
            # Checkout stats
            player['total_double_attempts'] += stats_dict.get('double_attempts', 0)
            player['total_doubles_hit'] += stats_dict.get('doubles_hit', 0)
            
            # Update highest finish
            high_finish = stats_dict.get('highest_finish', 0)
            if high_finish > player['highest_finish']:
                player['highest_finish'] = high_finish
            
            # Add to event history
            event_record = {
                'event_id': event_id,
                'date': datetime.now().isoformat(),
                'stats': stats_dict.copy()
            }
            player['event_history'].append(event_record)
            
            # Update event info
            if event_id not in self.data['events']:
                self.data['events'][event_id] = {
                    'event_id': event_id,
                    'date': datetime.now().isoformat(),
                    'players': [],
                    'winner': None,
                    'is_qualifier': True  # Assume qualifier unless set otherwise
                }
            
            if player_name not in self.data['events'][event_id]['players']:
                self.data['events'][event_id]['players'].append(player_name)
            
            # Update metadata
            self.data['metadata']['total_matches'] += 1
            
            return self._save_database()
            
        except Exception as e:
            print(f"Error adding match stats for {player_name}: {e}")
            return False
    
    def get_all_stats(self) -> Dict[str, Any]:
        """Get all player statistics"""
        return self.get_stats_api_format()
    
    def get_all_events(self) -> Dict[str, Any]:
        """Get all events"""
        return {'events': self.get_events_summary()}
    
    def get_leaderboard(self) -> List[Dict[str, Any]]:
        """Get current leaderboard with calculated averages and rankings"""
        players_list = []
        
        for player_name, player_data in self.data['players'].items():
            # Convert set to list for JSON serialization
            if isinstance(player_data['events_played'], set):
                events_played = list(player_data['events_played'])
                player_data['events_played'] = events_played
            else:
                events_played = player_data['events_played']
            
            # Calculate weighted 3DA
            total_average = 0.0
            if player_data['total_legs'] > 0:
                total_average = player_data['total_score'] / player_data['total_legs']
            
            # Calculate checkout percentage
            checkout_pct = 0.0
            if player_data.get('total_double_attempts', 0) > 0:
                checkout_pct = (player_data['total_doubles_hit'] / player_data['total_double_attempts']) * 100
            
            # Calculate match win percentage
            match_win_pct = 0.0
            if player_data.get('total_matches', 0) > 0:
                match_win_pct = (player_data['matches_won'] / player_data['total_matches']) * 100
            
            player_stats = {
                'name': player_name,
                'total_average': round(total_average, 2),
                'total_legs': player_data['total_legs'],
                'total_matches': player_data.get('total_matches', 0),
                'matches_won': player_data.get('matches_won', 0),
                'match_win_percentage': round(match_win_pct, 1),
                'total_180s': player_data['total_180s'],
                'total_160_plus': player_data.get('total_160_plus', 0),
                'total_140_plus': player_data['total_140_plus'],
                'total_100_plus': player_data['total_100_plus'],
                'highest_finish': player_data['highest_finish'],
                'total_double_attempts': player_data.get('total_double_attempts', 0),
                'total_doubles_hit': player_data.get('total_doubles_hit', 0),
                'checkout_percentage': round(checkout_pct, 1),
                'events_played': len(events_played),
                'qualified_for_toc': player_data.get('qualified_for_toc', False),
                'event_wins': len(player_data.get('event_wins', []))
            }
            
            players_list.append(player_stats)
        
        # Sort by total average (descending), then by events played
        players_list.sort(key=lambda x: (-x['total_average'], -x['events_played']))
        
        # Add rank
        for i, player in enumerate(players_list, 1):
            player['rank'] = i
        
        return players_list
    
    def get_events_summary(self) -> List[Dict[str, Any]]:
        """Get summary of all events"""
        events_list = []
        
        for event_id, event_data in self.data['events'].items():
            event_summary = {
                'event_id': event_id,
                'event_name': f"Event {event_id}",
                'date': event_data['date'],
                'players_count': len(event_data['players']),
                'winner': event_data.get('winner'),
                'is_qualifier': event_data.get('is_qualifier', True)
            }
            events_list.append(event_summary)
        
        # Sort by event_id
        events_list.sort(key=lambda x: x['event_id'])
        return events_list
    
    def get_stats_api_format(self) -> Dict[str, Any]:
        """Get data in the format expected by the stats display frontend"""
        leaderboard = self.get_leaderboard()
        events = self.get_events_summary()
        
        return {
            'players': leaderboard,
            'total_matches': self.data['metadata']['total_matches'],
            'events': events,
            'last_updated': self.data['metadata']['last_updated'],
            'series_info': self.data['metadata'].get('series_info', {})
        }
    
    def backup_database(self, backup_suffix: str = None) -> str:
        """Create a backup of the current database"""
        if backup_suffix is None:
            backup_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        backup_filename = f"{self.db_file}.backup_{backup_suffix}"
        
        try:
            with open(self.db_file, 'r', encoding='utf-8') as src:
                with open(backup_filename, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            return backup_filename
        except Exception as e:
            print(f"Error creating backup: {e}")
            return None
