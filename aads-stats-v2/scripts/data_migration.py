"""
AADS Stats V2 - Data Migration Script
Handles data flow: Scraper -> Staging -> Supabase
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from supabase import create_client, Client

class AADSDataMigration:
    """
    Manages data migration from scraper to Supabase staging area
    """
    
    def __init__(self, supabase_url: str, supabase_key: str):
        """Initialize Supabase client"""
        self.supabase: Client = create_client(supabase_url, supabase_key)
        
    def process_scraped_match(self, match_data: Dict) -> Dict:
        """
        Process raw scraped match data and insert into staging table
        
        Args:
            match_data: Raw match data from scraper
            
        Returns:
            Result with staging match ID or error
        """
        try:
            # Validate required fields
            required_fields = ['player_1_name', 'player_2_name', 'player_1_legs', 'player_2_legs']
            for field in required_fields:
                if field not in match_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Prepare staging data
            staging_data = {
                'event_id': match_data.get('event_id'),
                'phase': match_data.get('phase', 'round_robin'),
                'group_name': match_data.get('group_name'),
                'match_number': match_data.get('match_number'),
                'player_1_name': match_data['player_1_name'],
                'player_2_name': match_data['player_2_name'],
                'player_1_legs': int(match_data['player_1_legs']),
                'player_2_legs': int(match_data['player_2_legs']),
                'player_1_sets': match_data.get('player_1_sets', 0),
                'player_2_sets': match_data.get('player_2_sets', 0),
                'player_1_average': float(match_data.get('player_1_average', 0)),
                'player_2_average': float(match_data.get('player_2_average', 0)),
                'player_1_highest_checkout': match_data.get('player_1_highest_checkout', 0),
                'player_2_highest_checkout': match_data.get('player_2_highest_checkout', 0),
                'player_1_180s': match_data.get('player_1_180s', 0),
                'player_2_180s': match_data.get('player_2_180s', 0),
                'match_date': match_data.get('match_date', datetime.now().isoformat()),
                'board_number': match_data.get('board_number'),
                'status': 'pending',
                'source': match_data.get('source', 'scraper'),
                'raw_data': json.dumps(match_data)
            }
            
            # Insert into staging
            result = self.supabase.table('staging_matches').insert(staging_data).execute()
            
            return {
                'success': True,
                'staging_id': result.data[0]['id'],
                'message': 'Match added to staging queue'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def bulk_process_matches(self, matches: List[Dict]) -> Dict:
        """
        Process multiple matches in bulk
        
        Args:
            matches: List of match data dictionaries
            
        Returns:
            Summary of processing results
        """
        results = {
            'total': len(matches),
            'successful': 0,
            'failed': 0,
            'errors': []
        }
        
        for match in matches:
            result = self.process_scraped_match(match)
            if result['success']:
                results['successful'] += 1
            else:
                results['failed'] += 1
                results['errors'].append({
                    'match': match,
                    'error': result['error']
                })
        
        return results
    
    def get_or_create_player(self, player_name: str) -> Optional[str]:
        """
        Get existing player ID or create new player
        
        Args:
            player_name: Player's name
            
        Returns:
            Player UUID
        """
        try:
            # Try to find existing player
            result = self.supabase.table('players').select('id').eq('name', player_name).execute()
            
            if result.data:
                return result.data[0]['id']
            
            # Create new player
            new_player = self.supabase.table('players').insert({'name': player_name}).execute()
            return new_player.data[0]['id']
            
        except Exception as e:
            print(f"Error getting/creating player {player_name}: {e}")
            return None
    
    def get_or_create_event(self, event_number: int, event_name: str, event_date: str) -> Optional[str]:
        """
        Get existing event ID or create new event
        
        Args:
            event_number: Event number (1-7)
            event_name: Event name
            event_date: Event date
            
        Returns:
            Event UUID
        """
        try:
            # Try to find existing event
            result = self.supabase.table('events').select('id').eq('event_number', event_number).execute()
            
            if result.data:
                return result.data[0]['id']
            
            # Create new event
            new_event = self.supabase.table('events').insert({
                'event_number': event_number,
                'event_name': event_name,
                'event_date': event_date,
                'status': 'pending'
            }).execute()
            return new_event.data[0]['id']
            
        except Exception as e:
            print(f"Error getting/creating event: {e}")
            return None
    
    def approve_staging_match(self, staging_id: str) -> Dict:
        """
        Approve a staging match and move to production
        
        Args:
            staging_id: Staging match UUID
            
        Returns:
            Result dictionary
        """
        try:
            # Get staging match
            staging = self.supabase.table('staging_matches').select('*').eq('id', staging_id).single().execute()
            match = staging.data
            
            # Get or create player IDs
            player_1_id = self.get_or_create_player(match['player_1_name'])
            player_2_id = self.get_or_create_player(match['player_2_name'])
            
            if not player_1_id or not player_2_id:
                raise ValueError("Failed to get/create player IDs")
            
            # Determine winner
            winner_id = player_1_id if match['player_1_legs'] > match['player_2_legs'] else player_2_id
            
            # Create production match
            production_match = {
                'event_id': match['event_id'],
                'phase': match['phase'],
                'group_name': match['group_name'],
                'match_number': match['match_number'],
                'player_1_id': player_1_id,
                'player_2_id': player_2_id,
                'player_1_legs': match['player_1_legs'],
                'player_2_legs': match['player_2_legs'],
                'player_1_sets': match['player_1_sets'],
                'player_2_sets': match['player_2_sets'],
                'player_1_average': match['player_1_average'],
                'player_2_average': match['player_2_average'],
                'player_1_highest_checkout': match['player_1_highest_checkout'],
                'player_2_highest_checkout': match['player_2_highest_checkout'],
                'player_1_180s': match['player_1_180s'],
                'player_2_180s': match['player_2_180s'],
                'winner_id': winner_id,
                'match_date': match['match_date'],
                'board_number': match['board_number']
            }
            
            # Insert into matches table
            self.supabase.table('matches').insert(production_match).execute()
            
            # Update staging status
            self.supabase.table('staging_matches').update({
                'status': 'approved',
                'reviewed_at': datetime.now().isoformat()
            }).eq('id', staging_id).execute()
            
            return {
                'success': True,
                'message': 'Match approved and published'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


def main():
    """Example usage"""
    # Load from environment variables
    SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://yppxkvbmffcvdxuswsbf.supabase.co')
    SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', 'sb_publishable_U9kl9y_4_VOJyN8Mij6jnQ_A4Ilgziq')
    
    migrator = AADSDataMigration(SUPABASE_URL, SUPABASE_KEY)
    
    # Example: Process scraped match
    sample_match = {
        'event_id': 'event-uuid-here',
        'phase': 'round_robin',
        'group_name': 'A',
        'match_number': 1,
        'player_1_name': 'John Doe',
        'player_2_name': 'Jane Smith',
        'player_1_legs': 5,
        'player_2_legs': 3,
        'player_1_average': 85.5,
        'player_2_average': 78.3,
        'player_1_highest_checkout': 120,
        'player_2_highest_checkout': 100,
        'player_1_180s': 2,
        'player_2_180s': 1,
        'match_date': '2025-12-22T19:00:00'
    }
    
    result = migrator.process_scraped_match(sample_match)
    print(f"Migration result: {result}")


if __name__ == '__main__':
    main()
