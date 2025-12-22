#!/usr/bin/env python3
"""
Event Scraper API Server - Standalone Flask server for the event scraper
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import sys
import json
import logging
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database_manager import AADSDataManager
from scraper import DartConnectScraper
from event_data_manager import EventDataManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='.')
CORS(app)

# Initialize managers
db_manager = AADSDataManager(db_file="data/aads_master_db.json")
event_manager = EventDataManager(base_dir="data/event_data")
scraper = DartConnectScraper(db_manager, log_level=logging.INFO)

# ==================== STATIC FILES ====================

@app.route('/')
def serve_index():
    """Serve the event scraper page"""
    return send_from_directory('.', 'event_scraper.html')

@app.route('/event_scraper.html')
def serve_scraper():
    """Serve the event scraper page"""
    return send_from_directory('.', 'event_scraper.html')

# ==================== API ENDPOINTS ====================

@app.route('/api/scrape_event', methods=['POST'])
def scrape_event():
    """Scrape an event page to find all match URLs"""
    try:
        data = request.json
        event_url = data.get('event_url')
        
        if not event_url:
            return jsonify({'success': False, 'error': 'event_url is required'}), 400
        
        logger.info(f"Scraping event: {event_url}")
        
        # Scrape the event for matches
        result = scraper.scrape_event_for_matches(event_url)
        
        if result['success']:
            event_id = result['event_id']
            matches = result['matches']
            raw_response = result.get('raw_response')
            
            # Save matches using event data manager
            saved_to = event_manager.save_event_matches(
                event_id=event_id,
                matches=matches,
                raw_api_response=raw_response
            )
            
            # Get event summary
            summary = event_manager.get_event_summary(event_id)
            
            # Check if event already existed
            is_duplicate = event_manager.event_exists(event_id)
            
            return jsonify({
                'success': True,
                'event_id': event_id,
                'matches': matches,
                'saved_to': saved_to,
                'is_duplicate_event': is_duplicate,
                'data_summary': summary,
                'progress_log': result.get('progress_log', [])
            })
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Error scraping event: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/scrape_recap', methods=['POST'])
def scrape_recap():
    """Scrape a single recap URL"""
    try:
        data = request.json
        recap_url = data.get('recap_url')
        event_id = data.get('event_id')
        
        if not recap_url or not event_id:
            return jsonify({'success': False, 'error': 'recap_url and event_id are required'}), 400
        
        logger.info(f"Scraping recap: {recap_url}")
        
        # Extract stats from recap
        players_stats = scraper.extract_player_stats_from_recap(recap_url)
        
        if not players_stats:
            return jsonify({
                'success': False,
                'error': 'No player stats found in recap'
            }), 400
        
        # Add stats to database
        players_added = 0
        for player_stats in players_stats:
            success = db_manager.add_match_stats(
                player_name=player_stats['player_name'],
                event_id=event_id,
                match_url=recap_url,
                stats_dict={
                    'three_dart_average': player_stats['three_dart_average'],
                    'legs_played': player_stats.get('legs_played', 1),
                    'matches_played': player_stats.get('matches_played', 1),
                    'match_won': player_stats.get('match_won', 0),
                    'count_180s': player_stats.get('count_180s', 0),
                    'count_140_plus': player_stats.get('count_140_plus', 0),
                    'count_100_plus': player_stats.get('count_100_plus', 0),
                    'highest_finish': player_stats.get('highest_finish', 0),
                    'double_attempts': player_stats.get('double_attempts', 0),
                    'doubles_hit': player_stats.get('doubles_hit', 0)
                }
            )
            if success:
                players_added += 1
        
        # Update event data manager with match status
        event_manager.update_match_status(event_id, recap_url, 'completed', players_stats)
        
        message = f"Added stats for {players_added} players"
        logger.info(message)
        
        return jsonify({
            'success': True,
            'message': message,
            'players_added': players_added,
            'players': players_stats
        })
        
    except Exception as e:
        logger.error(f"Error scraping recap: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/upload_stage2', methods=['POST'])
def upload_stage2():
    """Upload Stage 2 data (scraped stats) to database"""
    try:
        data = request.json
        
        if not data or 'stats' not in data:
            return jsonify({'success': False, 'error': 'Invalid data format'}), 400
        
        event_id = data.get('event_id', f'Uploaded_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        stats = data.get('stats', [])
        
        logger.info(f"Uploading Stage 2 data: {len(stats)} matches for event {event_id}")
        
        matches_processed = 0
        players_added = 0
        
        for match_data in stats:
            match_url = match_data.get('match_url', '')
            players = match_data.get('players', [])
            
            for player_stats in players:
                success = db_manager.add_match_stats(
                    player_name=player_stats.get('player_name', 'Unknown'),
                    event_id=event_id,
                    match_url=match_url,
                    stats_dict={
                        'three_dart_average': player_stats.get('three_dart_average', 0),
                        'legs_played': player_stats.get('legs_played', 1),
                        'matches_played': player_stats.get('matches_played', 1),
                        'match_won': player_stats.get('match_won', 0),
                        'count_180s': player_stats.get('count_180s', 0),
                        'count_140_plus': player_stats.get('count_140_plus', 0),
                        'count_100_plus': player_stats.get('count_100_plus', 0),
                        'highest_finish': player_stats.get('highest_finish', 0),
                        'double_attempts': player_stats.get('double_attempts', 0),
                        'doubles_hit': player_stats.get('doubles_hit', 0)
                    }
                )
                if success:
                    players_added += 1
            
            if players:
                matches_processed += 1
        
        message = f"Uploaded {matches_processed} matches with {players_added} players"
        logger.info(message)
        
        return jsonify({
            'success': True,
            'message': message,
            'matches_processed': matches_processed,
            'players_added': players_added
        })
        
    except Exception as e:
        logger.error(f"Error uploading Stage 2 data: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/events', methods=['GET'])
def get_events():
    """Get list of all events"""
    try:
        events = event_manager.list_events()
        return jsonify({'success': True, 'events': events})
    except Exception as e:
        logger.error(f"Error getting events: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get all player statistics"""
    try:
        stats = db_manager.get_all_stats()
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/admin/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


if __name__ == '__main__':
    logger.info("=" * 50)
    logger.info("Event Scraper API Server Starting")
    logger.info("=" * 50)
    logger.info(f"Data directory: {os.path.abspath('data')}")
    logger.info(f"Event data directory: {os.path.abspath('data/event_data')}")
    logger.info("Server will be available at: http://localhost:5000")
    logger.info("=" * 50)
    
    # Ensure data directories exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('data/event_data', exist_ok=True)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
