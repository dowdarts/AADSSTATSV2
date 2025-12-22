"""
AADS DartConnect Scraper - Scrapes tournament data from DartConnect
Automatically finds recap URLs and extracts player statistics
Supports both static HTML and JavaScript-rendered pages
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import json
from typing import Dict, List, Any, Optional, Tuple
from urllib.parse import urljoin, urlparse
import logging
from database_manager import AADSDataManager

# Selenium imports for JavaScript-rendered pages
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    logging.warning("Selenium not available. Install with: pip install selenium webdriver-manager")

class DartConnectScraper:
    def __init__(self, db_manager: AADSDataManager, log_level: int = logging.INFO, use_selenium: bool = True):
        """Initialize the scraper with database manager"""
        self.db = db_manager
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Setup logging
        logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)  # Explicitly set logger level
        
        # Track processed URLs to avoid duplicates
        self.processed_recaps = set()
        
        # Common DartConnect domains
        self.dartconnect_domains = [
            'dartconnect.com',
            'www.dartconnect.com',
            'tv.dartconnect.com',
            'recap.dartconnect.com'  # Recap subdomain
        ]
        
        # Selenium setup for JavaScript pages
        self.use_selenium = use_selenium and SELENIUM_AVAILABLE
        self.driver = None
        
        if self.use_selenium:
            self.logger.info("Selenium support enabled for JavaScript pages")
        else:
            self.logger.warning("Selenium not available - JavaScript pages may not work")
    
    def is_dartconnect_url(self, url: str) -> bool:
        """Check if URL is from DartConnect"""
        try:
            parsed = urlparse(url)
            return any(domain in parsed.netloc.lower() for domain in self.dartconnect_domains)
        except:
            return False
    
    def _init_selenium_driver(self):
        """Initialize Selenium WebDriver if not already done"""
        if self.driver is None and self.use_selenium:
            try:
                chrome_options = Options()
                chrome_options.add_argument('--headless')  # Run in background
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--window-size=1920,1080')
                chrome_options.add_argument(f'user-agent={self.session.headers["User-Agent"]}')
                
                self.driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()),
                    options=chrome_options
                )
                self.logger.info("Selenium WebDriver initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize Selenium: {e}")
                self.use_selenium = False
    
    def _get_page_content(self, url: str, wait_for_element: str = None) -> Optional[str]:
        """Get page content, using Selenium if needed for JavaScript pages"""
        # Try with Selenium first for known JavaScript-heavy domains
        if self.use_selenium and ('dartconnect.com' in url):
            try:
                self._init_selenium_driver()
                if self.driver:
                    self.logger.debug(f"Using Selenium to fetch: {url}")
                    self.driver.get(url)
                    
                    # Wait for content to load
                    if wait_for_element:
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, wait_for_element))
                        )
                    else:
                        time.sleep(3)  # Generic wait for JS to execute
                    
                    return self.driver.page_source
            except Exception as e:
                self.logger.warning(f"Selenium fetch failed: {e}, falling back to requests")
        
        # Fallback to regular requests with better headers to avoid 403
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            response = self.session.get(url, timeout=30, headers=headers)
            response.raise_for_status()
            return response.text
        except Exception as e:
            self.logger.error(f"Failed to fetch {url}: {e}")
            return None
    
    def __del__(self):
        """Cleanup Selenium driver on destruction"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
    
    def scrape_event_for_matches(self, event_url: str) -> dict:
        """Scrape an event page to find all match recap URLs
        
        Args:
            event_url: URL of the event page (e.g., https://tv.dartconnect.com/eventmenu/mt_joe6163l_1)
            
        Returns:
            dict: {
                'success': bool,
                'event_id': str,
                'matches': [{'url': str, 'title': str}, ...],
                'error': str (if failed),
                'progress_log': [str, ...] (detailed step-by-step log)
            }
        """
        progress_log = []
        
        def log_step(message):
            """Helper to log both to logger and progress array"""
            self.logger.info(message)
            progress_log.append(message)
        
        try:
            log_step(f"[1/8] Starting event scrape: {event_url}")
            
            # Initialize Selenium driver if not already done
            log_step("[2/8] Initializing Selenium WebDriver...")
            log_step("[2/8] Initializing Selenium WebDriver...")
            self._init_selenium_driver()
            
            if not self.driver:
                log_step("✗ ERROR: Selenium driver not available")
                return {
                    'success': False,
                    'error': 'Selenium driver not available',
                    'progress_log': progress_log
                }
            
            log_step("✓ Selenium WebDriver ready")
            
            # Extract event ID from URL
            log_step("[3/8] Extracting event ID from URL...")
            # Matches: /eventmenu/mt_joe6163l_1 or /event/mt_joe6163l_1 or /event/mt_joe6163l_1/matches
            event_id_match = re.search(r'/(?:eventmenu|event)/([^/?]+)', event_url)
            event_id = event_id_match.group(1) if event_id_match else 'unknown'
            log_step(f"✓ Event ID extracted: {event_id}")
            
            # Construct the matches page URL
            matches_url = f"https://tv.dartconnect.com/event/{event_id}/matches"
            log_step(f"[4/8] Loading matches page: {matches_url}")
            
            # Load the matches page
            self.driver.get(matches_url)
            log_step("✓ Page loaded, waiting for JavaScript...")
            time.sleep(5)  # Wait for JavaScript to load matches
            log_step("✓ JavaScript execution complete")
            
            # Get page source
            log_step("[5/8] Parsing HTML content...")
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            log_step("✓ HTML parsed successfully")
            
            # Find all links to recap pages
            matches = []
            
            # DartConnect uses Inertia.js - check for data-page attribute
            log_step("[6/8] Checking for Inertia.js framework...")
            app_div = soup.find('div', id='app')
            if app_div and app_div.get('data-page'):
                try:
                    inertia_data = json.loads(app_div['data-page'])
                    log_step(f"✓ Inertia.js detected: {inertia_data.get('component')}")
                    
                    # The matches page should have match data in props
                    # We need to make an API call to get the actual matches
                    # Use the API endpoint from the Ziggy routes
                    import requests
                    api_url = f"https://tv.dartconnect.com/api/event/{event_id}/matches"
                    log_step(f"[7/8] Calling DartConnect API: {api_url}")
                    
                    response = requests.post(api_url, headers={
                        'User-Agent': self.session.headers['User-Agent'],
                        'Accept': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    })
                    
                    # Save raw API response for later storage
                    raw_api_response = None
                    
                    if response.status_code == 200:
                        log_step(f"✓ API response received (status 200)")
                        api_data = response.json()
                        raw_api_response = api_data  # Store for return
                        log_step("✓ JSON parsed from API response")
                        
                        # DartConnect API returns: {"status": "OK", "payload": {"completed": [...], "events": [...]}}
                        # The "completed" array contains ALL matches from all events (Round Robin, Knockout, etc.)
                        log_step("[8/8] Processing match data from API...")
                        matches_data = []
                        
                        if isinstance(api_data, dict):
                            # Check for standard DartConnect API response
                            if 'payload' in api_data and isinstance(api_data['payload'], dict):
                                payload = api_data['payload']
                                # Get all completed matches (includes all events)
                                if 'completed' in payload and isinstance(payload['completed'], list):
                                    matches_data = payload['completed']
                                    log_step(f"✓ Found {len(matches_data)} completed matches in API response")
                            
                            # Fallback: try other common keys if payload not found
                            if not matches_data:
                                for key in ['matches', 'data', 'match', 'items']:
                                    if key in api_data:
                                        matches_data = api_data[key] if isinstance(api_data[key], list) else [api_data[key]]
                                        break
                        elif isinstance(api_data, list):
                            matches_data = api_data
                        
                        log_step(f"Processing {len(matches_data)} matches from API response...")
                        
                        match_counter = 1
                        for match in matches_data:
                            if isinstance(match, dict):
                                # DartConnect API match fields:
                                # "mi" = match ID, "hc" = home competitor, "ac" = away competitor, "el" = event label
                                match_id = match.get('mi') or match.get('i') or match.get('id') or match.get('match_id') or match.get('matchId')
                                if match_id:
                                    match_url = f"https://recap.dartconnect.com/matches/{match_id}"
                                    
                                    # Get player names
                                    home_name = match.get('hc') or match.get('hcf') or (match.get('home_player', {}).get('name') if isinstance(match.get('home_player'), dict) else None)
                                    away_name = match.get('ac') or match.get('acf') or (match.get('away_player', {}).get('name') if isinstance(match.get('away_player'), dict) else None)
                                    
                                    # Determine match type, phase, and group based on position
                                    # AADS Tournament Structure:
                                    # Match 1: Final
                                    # Match 2-3: Semifinals
                                    # Match 4-7: Quarterfinals
                                    # Match 8-17: Group A Round Robin (10 matches)
                                    # Match 18-27: Group B Round Robin (10 matches)
                                    
                                    if match_counter == 1:
                                        match_type = 'Knockout'
                                        phase = 'final'
                                        group_name = None
                                        phase_label = 'Final'
                                    elif match_counter <= 3:
                                        match_type = 'Knockout'
                                        phase = 'semifinal'
                                        group_name = None
                                        phase_label = 'Semifinal'
                                    elif match_counter <= 7:
                                        match_type = 'Knockout'
                                        phase = 'quarterfinal'
                                        group_name = None
                                        phase_label = 'Quarterfinal'
                                    elif match_counter <= 17:
                                        match_type = 'Round Robin'
                                        phase = 'round_robin'
                                        group_name = 'A'
                                        phase_label = 'Round Robin - Group A'
                                    elif match_counter <= 27:
                                        match_type = 'Round Robin'
                                        phase = 'round_robin'
                                        group_name = 'B'
                                        phase_label = 'Round Robin - Group B'
                                    else:
                                        # Fallback for any extra matches
                                        match_type = 'Round Robin'
                                        phase = 'round_robin'
                                        group_name = None
                                        phase_label = 'Round Robin'
                                    
                                    # Build informative title: "Event_1 Match 1 - Player A vs Player B (Final)"
                                    title_parts = [f"{event_id} Match {match_counter}"]
                                    
                                    # Add player names
                                    if home_name and away_name:
                                        title_parts.append(f"- {home_name} vs {away_name}")
                                    elif home_name or away_name:
                                        player = home_name or away_name
                                        title_parts.append(f"- {player}")
                                    
                                    # Add phase label
                                    title_parts.append(f"({phase_label})")
                                    
                                    title = ' '.join(title_parts)
                                    
                                    matches.append({
                                        'url': match_url,
                                        'title': title,
                                        'match_number': match_counter,
                                        'match_type': match_type,
                                        'phase': phase,
                                        'group_name': group_name,
                                        'home_player': home_name,
                                        'away_player': away_name
                                    })
                                    
                                    match_counter += 1
                    else:
                        self.logger.warning(f"API request failed with status {response.status_code}")
                        
                except Exception as e:
                    self.logger.error(f"Error parsing Inertia.js data: {e}")
            
            # Fallback: Look for links in HTML (old method)
            if not matches:
                self.logger.info("No matches found in API, trying HTML links...")
                for link in soup.find_all('a', href=True):
                    href = link.get('href', '')
                    
                    # Check if it's a recap URL
                    if 'recap.dartconnect.com/matches/' in href or '/matches/' in href:
                        # Construct full URL if relative
                        if href.startswith('/'):
                            match_url = 'https://recap.dartconnect.com' + href
                        elif not href.startswith('http'):
                            match_url = 'https://recap.dartconnect.com/matches/' + href
                        else:
                            match_url = href
                        
                        # Extract match title if available
                        title = link.get_text(strip=True) or f"Match {len(matches) + 1}"
                        
                        # Avoid duplicates
                        if not any(m['url'] == match_url for m in matches):
                            matches.append({
                                'url': match_url,
                                'title': title
                            })
                
                # Also look for match IDs in onclick or data attributes
                for element in soup.find_all(attrs={'data-match-id': True}):
                    match_id = element.get('data-match-id')
                    match_url = f"https://recap.dartconnect.com/matches/{match_id}"
                    title = element.get_text(strip=True) or f"Match {len(matches) + 1}"
                    
                    if not any(m['url'] == match_url for m in matches):
                        matches.append({
                            'url': match_url,
                            'title': title
                        })
            
            self.logger.info(f"Found {len(matches)} matches in event {event_id}")
            log_step(f"✓ Stage 1 Complete: Found {len(matches)} matches ({min(20, len(matches))} Round Robin, {max(0, len(matches)-20)} Knockout)")
            
            return {
                'success': True,
                'event_id': event_id,
                'matches': matches,
                'raw_response': raw_api_response if 'raw_api_response' in locals() else None,
                'progress_log': progress_log
            }
            
        except Exception as e:
            error_msg = f"Error scraping event page: {e}"
            self.logger.error(error_msg)
            progress_log.append(f"✗ ERROR: {error_msg}")
            return {
                'success': False,
                'error': str(e),
                'progress_log': progress_log
            }
    
    def _parse_recap_json_format(self, soup: BeautifulSoup, match_id: str) -> List[Dict[str, Any]]:
        """
        Parse recap.dartconnect.com JSON format embedded in data-page attribute.
        Extracts detailed match statistics including leg-by-leg analysis.
        """
        print(f"\n🔍 DEBUG: _parse_recap_json_format called for match_id={match_id}")
        try:
            import json
            
            # Find the div with id="app" that contains the data-page attribute
            app_div = soup.find('div', id='app')
            if not app_div:
                return []
            
            # Extract JSON data from data-page attribute
            data_page = app_div.get('data-page')
            if not data_page:
                return []
            
            # Parse JSON
            page_data = json.loads(data_page)
            
            # Extract match info and segments (leg-by-leg data)
            match_info = page_data.get('props', {}).get('matchInfo', {})
            segments = page_data.get('props', {}).get('segments', {})
            home_players = page_data.get('props', {}).get('homePlayers', [])
            away_players = page_data.get('props', {}).get('awayPlayers', [])
            
            if not match_info:
                return []
            
            # Extract opponent stats
            opponents = match_info.get('opponents', [])
            
            if not opponents or len(opponents) < 2:
                return []
            
            # Parse leg-by-leg data for detailed statistics
            leg_data = self._parse_leg_data(segments, opponents)
            
            players_stats = []
            
            print(f"🔍 DEBUG: Found {len(opponents)} opponents")
            print(f"🔍 DEBUG: homePlayers = {home_players}")
            print(f"🔍 DEBUG: awayPlayers = {away_players}")
            
            self.logger.info(f"===== PARSING MATCH {match_id} =====")
            self.logger.info(f"Opponents: {len(opponents)}")
            self.logger.info(f"Home players array: {home_players}")
            self.logger.info(f"Away players array: {away_players}")
            self.logger.debug(f"Processing {len(opponents)} opponents")
            self.logger.debug(f"Home players: {home_players}")
            self.logger.debug(f"Away players: {away_players}")
            
            # Process each opponent
            for idx, opponent in enumerate(opponents):
                # Try to get full name from homePlayers/awayPlayers first, fallback to opponent name
                player_name = opponent.get('name', '')
                
                # Enhance with full name if available
                if idx == 0 and home_players and len(home_players) > 0:
                    full_name = home_players[0].get('name', '')
                    if full_name:
                        player_name = full_name
                elif idx == 1 and away_players and len(away_players) > 0:
                    full_name = away_players[0].get('name', '')
                    if full_name:
                        player_name = full_name
                
                self.logger.info(f"Player {idx}: opponent.name='{opponent.get('name', '')}', final player_name='{player_name}'")
                self.logger.debug(f"Player {idx}: {player_name}")
                
                if not player_name:
                    self.logger.warning(f"Skipping opponent {idx} - no name found")
                    continue
                
                player_leg_data = leg_data.get(idx, {})
                
                # Calculate 3-dart average (DartConnect calls it PPR for 501 games)
                ppr_str = opponent.get('ppr', '0')
                try:
                    if ppr_str and ppr_str != '-':
                        ppr_average = float(ppr_str)
                    else:
                        ppr_average = 0.0
                except (ValueError, TypeError) as e:
                    self.logger.warning(f"Could not parse PPR value '{ppr_str}': {e}")
                    ppr_average = 0.0
                
                # Match-level stats
                total_legs = int(match_info.get('total_games', 0))
                legs_won = int(opponent.get('leg_wins', 0))
                legs_lost = total_legs - legs_won
                sets_won = int(opponent.get('set_wins', 0))
                
                # Calculate leg win percentage
                leg_win_percentage = (legs_won / total_legs * 100) if total_legs > 0 else 0
                
                # Extract detailed statistics from leg data
                count_180s = player_leg_data.get('count_180s', 0)
                count_160_plus = player_leg_data.get('count_160_plus', 0)
                count_140_plus = player_leg_data.get('count_140_plus', 0)
                count_100_plus = player_leg_data.get('count_100_plus', 0)
                highest_finish = player_leg_data.get('highest_finish', 0)
                double_attempts = player_leg_data.get('double_attempts', 0)
                doubles_hit = player_leg_data.get('doubles_hit', 0)
                
                # Calculate checkout percentage
                checkout_percentage = (doubles_hit / double_attempts * 100) if double_attempts > 0 else 0
                
                # Extract statistics matching the expected format
                stats = {
                    'player_name': player_name,
                    'match_id': match_id,
                    'three_dart_average': ppr_average,  # For 501: 3DA (3-dart average). For Cricket: PPR (points per round)
                    
                    # Match stats
                    'matches_played': 1,  # Each recap = 1 match
                    'match_won': 1 if (opponent.get('score', 0) > opponents[1 - idx].get('score', 0)) else 0,
                    'match_score': f"{opponent.get('score', 0)}-{opponents[1 - idx].get('score', 0)}",
                    
                    # Leg/Set stats
                    'legs_played': total_legs,
                    'legs_won': legs_won,
                    'legs_lost': legs_lost,
                    'leg_win_percentage': round(leg_win_percentage, 2),
                    'sets_played': int(match_info.get('total_sets', 1)),
                    'sets_won': sets_won,
                    'sets_lost': int(match_info.get('total_sets', 1)) - sets_won,
                    
                    # Score counts
                    'count_180s': count_180s,
                    'count_160_plus': count_160_plus,
                    'count_140_plus': count_140_plus,
                    'count_100_plus': count_100_plus,
                    
                    # Checkout stats
                    'highest_finish': highest_finish,
                    'double_attempts': double_attempts,
                    'doubles_hit': doubles_hit,
                    'checkout_percentage': round(checkout_percentage, 2),
                    
                    # Additional stats
                    'darts_thrown': self._parse_stat_value(opponent.get('darts_thrown_ppr', '0')),
                    'points_scored': self._parse_stat_value(opponent.get('points_scored_ppr', '0')),
                }
                
                self.logger.debug(f"Parsed player: {player_name} - 3DA: {stats['three_dart_average']}, " +
                                f"Legs: {legs_won}/{total_legs} ({leg_win_percentage:.1f}%), " +
                                f"180s: {count_180s}, Checkout: {checkout_percentage:.1f}%")
                
                players_stats.append(stats)
            
            self.logger.info(f"===== MATCH {match_id} COMPLETE: Extracted {len(players_stats)} players =====")
            self.logger.info(f"Extracted {len(players_stats)} players from recap JSON")
            return players_stats
            
        except Exception as e:
            self.logger.error(f"Error parsing recap JSON format: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return []
    
    def _parse_leg_data(self, segments: Dict, opponents: List) -> Dict[int, Dict]:
        """
        Parse leg-by-leg data to extract detailed statistics like 180s, checkouts, etc.
        Returns dict with player index as key and their aggregated leg stats.
        """
        player_stats = {0: {}, 1: {}}
        
        # Initialize counters for each player
        for player_idx in [0, 1]:
            player_stats[player_idx] = {
                'count_180s': 0,
                'count_160_plus': 0,
                'count_140_plus': 0,
                'count_100_plus': 0,
                'highest_finish': 0,
                'double_attempts': 0,
                'doubles_hit': 0,
            }
        
        try:
            # Segments can be organized by segment name (e.g., '' for default)
            for segment_name, segment_sets in segments.items():
                if not segment_sets:
                    continue
                    
                # Each set contains legs
                for leg_set in segment_sets:
                    if not isinstance(leg_set, list):
                        continue
                        
                    for leg in leg_set:
                        # Extract home and away player data for this leg
                        home_data = leg.get('home', {})
                        away_data = leg.get('away', {})
                        
                        # Process both players
                        for player_idx, player_data in enumerate([home_data, away_data]):
                            if not player_data:
                                continue
                            
                            # Calculate scores from this leg
                            starting_points = player_data.get('starting_points', 501)
                            ending_points = player_data.get('ending_points', 0)
                            points_scored = starting_points - ending_points
                            
                            # Check for 100+ scores (approximate based on PPR)
                            ppr = self._parse_stat_value(str(player_data.get('ppr', '0')))
                            if ppr >= 60:  # High scoring leg
                                player_stats[player_idx]['count_100_plus'] += 1
                            if ppr >= 70:
                                player_stats[player_idx]['count_140_plus'] += 1
                            if ppr >= 80:
                                player_stats[player_idx]['count_160_plus'] += 1
                            if ppr >= 100:
                                player_stats[player_idx]['count_180s'] += 1
                            
                            # Check for checkout (leg won)
                            if player_data.get('win', False):
                                double_out = player_data.get('double_out_points', 0)
                                if double_out > 0:
                                    # Successful checkout
                                    player_stats[player_idx]['doubles_hit'] += 1
                                    if double_out > player_stats[player_idx]['highest_finish']:
                                        player_stats[player_idx]['highest_finish'] = double_out
                                    
                            # Count double attempts (any leg where player got close)
                            if ending_points <= 170:  # Within checkout range
                                player_stats[player_idx]['double_attempts'] += 1
                                
        except Exception as e:
            self.logger.warning(f"Error parsing leg data: {e}")
        
        return player_stats
    
    def _parse_stat_value(self, value_str: str) -> int:
        """Parse a stat value that might have commas or dashes"""
        if not value_str or value_str == '-':
            return 0
        # Remove commas
        value_str = value_str.replace(',', '')
        try:
            return int(value_str)
        except:
            return 0
    
    def _enrich_stats_from_api(self, match_id: str, players_stats: List[Dict[str, Any]]) -> None:
        """
        Fetch additional stats from DartConnect API endpoints (other tabs)
        Enriches players_stats in-place with data from counts, games, and players tabs
        """
        try:
            import requests
            
            base_url = "https://recap.dartconnect.com"
            headers = {
                'User-Agent': self.session.headers['User-Agent'],
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-Inertia': 'true',
                'X-Inertia-Version': '1'
            }
            
            # Fetch counts tab data (COD, COO, COE, First 9 Average, etc.)
            try:
                counts_url = f"{base_url}/counts/{match_id}"
                counts_response = requests.get(counts_url, headers=headers, timeout=10)
                if counts_response.status_code == 200:
                    counts_data = counts_response.json()
                    self._merge_counts_data(players_stats, counts_data)
                    self.logger.debug(f"Fetched counts data for match {match_id}")
            except Exception as e:
                self.logger.warning(f"Could not fetch counts data: {e}")
            
            # Fetch players tab data (highest turns, high double out, highest 3DA)
            try:
                players_url = f"{base_url}/players/{match_id}"
                players_response = requests.get(players_url, headers=headers, timeout=10)
                if players_response.status_code == 200:
                    players_data = players_response.json()
                    self._merge_players_data(players_stats, players_data)
                    self.logger.debug(f"Fetched players data for match {match_id}")
            except Exception as e:
                self.logger.warning(f"Could not fetch players data: {e}")
                
        except Exception as e:
            self.logger.error(f"Error enriching stats from API: {e}")
    
    def _merge_counts_data(self, players_stats: List[Dict], counts_data: Dict) -> None:
        """Merge Match Counts tab data into players_stats"""
        try:
            # The counts API returns data in props
            props = counts_data.get('props', {})
            
            # Look for relevant count data (structure may vary)
            # This will need to be adjusted based on actual API response
            # For now, log the structure so we can see what's available
            self.logger.debug(f"Counts data structure: {list(props.keys()) if isinstance(props, dict) else 'not a dict'}")
            
            # TODO: Map specific fields once we know the structure
            # Examples of what we're looking for:
            # - first_9_average
            # - checkout_darts (COD)
            # - checkout_opportunities (COO)
            # - checkout_efficiency (COE)
            
        except Exception as e:
            self.logger.warning(f"Error merging counts data: {e}")
    
    def _merge_players_data(self, players_stats: List[Dict], players_data: Dict) -> None:
        """Merge Player Performance tab data into players_stats"""
        try:
            # The players API returns data in props
            props = players_data.get('props', {})
            
            # Log structure for debugging
            self.logger.debug(f"Players data structure: {list(props.keys()) if isinstance(props, dict) else 'not a dict'}")
            
            # TODO: Map specific fields once we know the structure
            # Examples of what we're looking for:
            # - highest_turns
            # - high_double_out
            # - highest_3da
            
        except Exception as e:
            self.logger.warning(f"Error merging players data: {e}")

    
    def find_recap_urls_from_tournament(self, tournament_url: str) -> List[str]:
        """
        Find all match recap URLs from a DartConnect tournament page
        This looks for patterns like '/dart/Recap.aspx?ID=xxxxx'
        """
        if not self.is_dartconnect_url(tournament_url):
            self.logger.warning(f"URL is not from DartConnect: {tournament_url}")
            return []
        
        recap_urls = []
        
        try:
            self.logger.info(f"Scanning tournament page: {tournament_url}")
            page_content = self._get_page_content(tournament_url, wait_for_element='a[href*="match"]')
            
            if not page_content:
                self.logger.warning(f"Could not fetch tournament page: {tournament_url}")
                return []
            
            soup = BeautifulSoup(page_content, 'html.parser')
            
            # Look for links to recap pages
            # DartConnect recaps typically have URLs like: /dart/Recap.aspx?ID=12345
            recap_links = soup.find_all('a', href=re.compile(r'/dart/Recap\.aspx\?ID=\d+', re.IGNORECASE))
            
            for link in recap_links:
                href = link.get('href', '')
                if href:
                    full_url = urljoin(tournament_url, href)
                    if full_url not in recap_urls:
                        recap_urls.append(full_url)
            
            # Also look for TV DartConnect format links
            # Look for match/game links that might be in different formats
            tv_links = soup.find_all('a', href=re.compile(r'/(match|game|result)/', re.IGNORECASE))
            for link in tv_links:
                href = link.get('href', '')
                if href and ('match' in href.lower() or 'game' in href.lower() or 'result' in href.lower()):
                    full_url = urljoin(tournament_url, href)
                    if full_url not in recap_urls:
                        recap_urls.append(full_url)
            
            # Look for any links that might contain match data
            # Check for table rows or divs that might contain match information
            match_containers = soup.find_all(['div', 'tr'], class_=re.compile(r'match|game|result', re.IGNORECASE))
            for container in match_containers:
                links = container.find_all('a', href=True)
                for link in links:
                    href = link.get('href', '')
                    if href and not href.startswith('#'):
                        full_url = urljoin(tournament_url, href)
                        if full_url not in recap_urls and self.is_dartconnect_url(full_url):
                            recap_urls.append(full_url)
            
            # Also look for any links with text suggesting they're recaps
            potential_recap_links = soup.find_all('a', string=re.compile(r'recap|summary|result|match|view', re.IGNORECASE))
            for link in potential_recap_links:
                href = link.get('href', '')
                if href and 'recap' in href.lower():
                    full_url = urljoin(tournament_url, href)
                    if full_url not in recap_urls:
                        recap_urls.append(full_url)
            
            # For debugging: let's also check what the page structure looks like
            self.logger.debug(f"Page title: {soup.title.get_text() if soup.title else 'No title'}")
            
            # Look for any links at all to understand the page structure
            all_links = soup.find_all('a', href=True)
            self.logger.debug(f"Found {len(all_links)} total links on page")
            
            # Filter and show links that might be relevant
            potential_links = []
            for link in all_links:
                href = link.get('href', '')
                text = link.get_text().strip()
                if href and not href.startswith('#') and not href.startswith('mailto:'):
                    # Check if this could be a match-related link
                    if any(keyword in href.lower() or keyword in text.lower() 
                           for keyword in ['match', 'game', 'result', 'recap', 'view', 'detail']):
                        full_url = urljoin(tournament_url, href)
                        if self.is_dartconnect_url(full_url):
                            potential_links.append((full_url, text[:50]))
            
            self.logger.info(f"Found {len(potential_links)} potential match links:")
            for url, text in potential_links[:10]:  # Show first 10
                self.logger.info(f"  - {text}: {url}")
                if url not in recap_urls:
                    recap_urls.append(url)
            
            self.logger.info(f"Found {len(recap_urls)} recap URLs")
            return recap_urls
            
        except Exception as e:
            self.logger.error(f"Error scanning tournament page {tournament_url}: {e}")
            return []
    
    def extract_player_stats_from_recap(self, recap_url: str) -> List[Dict[str, Any]]:
        """
        Extract player statistics from a DartConnect recap page
        Returns list of player stats dictionaries
        """
        print(f"\n🚀 ENTRY: extract_player_stats_from_recap called with URL: {recap_url}")
        
        # Note: Removed processed_recaps check to allow re-scraping during development/debugging
        # if recap_url in self.processed_recaps:
        #     self.logger.debug(f"Already processed: {recap_url}")
        #     return []
        
        try:
            self.logger.info(f"Scraping recap: {recap_url}")
            page_content = self._get_page_content(recap_url, wait_for_element='#app')
            
            if not page_content:
                self.logger.warning(f"Could not fetch recap page: {recap_url}")
                return []
            
            soup = BeautifulSoup(page_content, 'html.parser')
            
            # Extract event/match ID from URL for tracking
            match_id = self._extract_match_id_from_url(recap_url)
            
            players_stats = []
            
            # Check if this is recap.dartconnect.com with JSON data
            if 'recap.dartconnect.com' in recap_url:
                players_stats = self._parse_recap_json_format(soup, match_id)
                
                # Fetch additional stats from other tabs via API (non-blocking)
                if players_stats and match_id:
                    try:
                        self._enrich_stats_from_api(match_id, players_stats)
                    except Exception as e:
                        self.logger.warning(f"Could not enrich stats from API: {e}")
            
            # Fallback to table parsing for other formats
            if not players_stats:
                # Look for statistics tables (DartConnect typically uses tables)
                stats_tables = soup.find_all('table')
                
                for table in stats_tables:
                    # Look for headers that indicate this is a stats table
                    headers = table.find_all(['th', 'td'])
                    header_text = ' '.join([h.get_text().strip().lower() for h in headers[:10]])
                    
                    # Check if this looks like a statistics table
                    if any(keyword in header_text for keyword in ['average', 'dart', '180', '140', 'finish', 'player']):
                        table_stats = self._parse_stats_table(table, match_id)
                        players_stats.extend(table_stats)
            
            # If still no tables found, try alternative parsing methods
            if not players_stats:
                players_stats = self._parse_alternative_format(soup, match_id)
            
            if players_stats:
                self.processed_recaps.add(recap_url)
                self.logger.info(f"Extracted stats for {len(players_stats)} players from {recap_url}")
            else:
                self.logger.warning(f"No player stats found in {recap_url}")
            
            return players_stats
            
        except Exception as e:
            self.logger.error(f"Error extracting stats from {recap_url}: {e}")
            return []
    
    def _extract_match_id_from_url(self, url: str) -> str:
        """Extract match/event ID from DartConnect URL"""
        # Look for ID parameter in URL
        match = re.search(r'ID=(\d+)', url, re.IGNORECASE)
        if match:
            return f"DC_{match.group(1)}"
        
        # Fallback: use last part of URL
        parsed = urlparse(url)
        return f"Match_{hash(url) % 100000}"
    
    def _parse_stats_table(self, table, match_id: str) -> List[Dict[str, Any]]:
        """Parse a statistics table to extract player data"""
        players_stats = []
        
        try:
            rows = table.find_all('tr')
            if len(rows) < 2:
                return []
            
            # Try to identify columns by header text
            header_row = rows[0]
            headers = [th.get_text().strip().lower() for th in header_row.find_all(['th', 'td'])]
            
            # Map common column names to our standard fields
            column_mapping = {
                'name': ['name', 'player', 'player name'],
                'average': ['average', 'avg', '3-dart avg', '3da', 'dart average'],
                '180s': ['180s', '180', 'maximum'],
                '140+': ['140+', '140', 'tons plus', 'ton+'],
                '100+': ['100+', '100', 'tons', 'ton'],
                'high_finish': ['high finish', 'highest finish', 'hf', 'high out'],
                'legs': ['legs', 'legs played', 'played']
            }
            
            # Find column indices
            col_indices = {}
            for field, possible_names in column_mapping.items():
                for i, header in enumerate(headers):
                    if any(name in header for name in possible_names):
                        col_indices[field] = i
                        break
            
            # Process data rows
            for row in rows[1:]:
                cells = row.find_all(['td', 'th'])
                if len(cells) < 2:
                    continue
                
                player_stats = self._extract_player_stats_from_row(cells, col_indices, match_id)
                if player_stats:
                    players_stats.append(player_stats)
        
        except Exception as e:
            self.logger.error(f"Error parsing stats table: {e}")
        
        return players_stats
    
    def _extract_player_stats_from_row(self, cells, col_indices: Dict[str, int], match_id: str) -> Optional[Dict[str, Any]]:
        """Extract player stats from a table row"""
        try:
            # Get player name
            if 'name' not in col_indices:
                # Try first column as name
                player_name = cells[0].get_text().strip()
            else:
                player_name = cells[col_indices['name']].get_text().strip()
            
            if not player_name or len(player_name) < 2:
                return None
            
            # Extract numeric stats with defaults
            stats = {
                'match_id': match_id,
                'player_name': player_name,
                'three_dart_average': self._safe_float_extract(cells, col_indices.get('average', 1)),
                'legs_played': self._safe_int_extract(cells, col_indices.get('legs', -1), default=1),
                'count_180s': self._safe_int_extract(cells, col_indices.get('180s', -1)),
                'count_140_plus': self._safe_int_extract(cells, col_indices.get('140+', -1)),
                'count_100_plus': self._safe_int_extract(cells, col_indices.get('100+', -1)),
                'highest_finish': self._safe_int_extract(cells, col_indices.get('high_finish', -1))
            }
            
            # Validate that we got at least a player name and average
            if stats['three_dart_average'] > 0:
                return stats
            
        except Exception as e:
            self.logger.debug(f"Error extracting player stats from row: {e}")
        
        return None
    
    def _safe_float_extract(self, cells, index: int, default: float = 0.0) -> float:
        """Safely extract float value from table cell"""
        if index < 0 or index >= len(cells):
            return default
        
        try:
            text = cells[index].get_text().strip()
            # Remove non-numeric characters except decimal point
            numeric_text = re.sub(r'[^\d.]', '', text)
            return float(numeric_text) if numeric_text else default
        except:
            return default
    
    def _safe_int_extract(self, cells, index: int, default: int = 0) -> int:
        """Safely extract integer value from table cell"""
        if index < 0 or index >= len(cells):
            return default
        
        try:
            text = cells[index].get_text().strip()
            # Remove non-numeric characters
            numeric_text = re.sub(r'[^\d]', '', text)
            return int(numeric_text) if numeric_text else default
        except:
            return default
    
    def _parse_alternative_format(self, soup, match_id: str) -> List[Dict[str, Any]]:
        """Alternative parsing method for non-table formats"""
        players_stats = []
        
        try:
            # Look for div-based layouts or other formats
            # This is a fallback for sites that don't use tables
            
            # Look for patterns like "Player Name: 78.45 avg"
            text_content = soup.get_text()
            
            # Regular expressions to find player statistics
            player_patterns = [
                r'([A-Za-z\s]+):\s*(\d+\.?\d*)\s*avg',
                r'([A-Za-z\s]+)\s+(\d+\.?\d*)\s+average',
            ]
            
            for pattern in player_patterns:
                matches = re.findall(pattern, text_content, re.IGNORECASE)
                for match in matches:
                    player_name = match[0].strip()
                    average = float(match[1])
                    
                    if len(player_name) > 2 and average > 0:
                        stats = {
                            'match_id': match_id,
                            'player_name': player_name,
                            'three_dart_average': average,
                            'legs_played': 1,  # Default when not specified
                            'count_180s': 0,
                            'count_140_plus': 0,
                            'count_100_plus': 0,
                            'highest_finish': 0
                        }
                        players_stats.append(stats)
        
        except Exception as e:
            self.logger.debug(f"Error in alternative parsing: {e}")
        
        return players_stats
    
    def extract_players_from_api_data(self, event_id: str) -> List[Dict[str, Any]]:
        """Extract player stats from existing API data instead of scraping broken recap URLs
        
        Args:
            event_id: Event identifier like 'mt_joe6163l_1'
            
        Returns:
            List[Dict]: List of player stats dictionaries
        """
        import json
        import os
        
        self.logger.info(f"🎯 Extracting players from API data for event {event_id}")
        
        # Look for API data file
        event_dir = f"event_data/{event_id}/raw_data"
        api_files = []
        
        if os.path.exists(event_dir):
            for file in os.listdir(event_dir):
                if file.startswith("api_response_") and file.endswith(".json"):
                    api_files.append(os.path.join(event_dir, file))
        
        if not api_files:
            self.logger.error(f"No API data found for event {event_id} in {event_dir}")
            return []
            
        # Use the most recent API file
        api_file = sorted(api_files)[-1]
        self.logger.info(f"Using API data file: {api_file}")
        
        try:
            with open(api_file, 'r') as f:
                api_data = json.load(f)
            
            players_stats = []
            completed_matches = api_data.get('payload', {}).get('completed', [])
            
            self.logger.info(f"Found {len(completed_matches)} completed matches in API data")
            
            for match in completed_matches:
                # Extract home player
                home_player = {
                    'player_name': match.get('hcf', 'Unknown'),  # Full name
                    'three_dart_average': match.get('hp5', 0),  # 5-dart average
                    'legs_played': 1,  # Default to 1 for now
                    'legs_won': 1 if match.get('hs', 0) > match.get('as', 0) else 0,
                    'legs_lost': 1 if match.get('hs', 0) < match.get('as', 0) else 0,
                    'matches_played': 1,
                    'match_won': match.get('hs', 0) > match.get('as', 0),
                    'count_180s': match.get('h180', 0),
                    'count_140_plus': match.get('h140', 0),
                    'count_100_plus': match.get('h100', 0),
                    'highest_finish': match.get('hhf', 0),
                    'checkout_percentage': 0,  # Calculate if needed
                    'match_id': match.get('mi', ''),
                    'event_id': event_id
                }
                players_stats.append(home_player)
                
                # Extract away player  
                away_player = {
                    'player_name': match.get('acf', 'Unknown'),  # Full name
                    'three_dart_average': match.get('ap5', 0),  # 5-dart average
                    'legs_played': 1,
                    'legs_won': 1 if match.get('as', 0) > match.get('hs', 0) else 0,
                    'legs_lost': 1 if match.get('as', 0) < match.get('hs', 0) else 0,
                    'matches_played': 1,
                    'match_won': match.get('as', 0) > match.get('hs', 0),
                    'count_180s': match.get('a180', 0),
                    'count_140_plus': match.get('a140', 0),
                    'count_100_plus': match.get('a100', 0),
                    'highest_finish': match.get('ahf', 0),
                    'checkout_percentage': 0,
                    'match_id': match.get('mi', ''),
                    'event_id': event_id
                }
                players_stats.append(away_player)
            
            self.logger.info(f"✅ Extracted {len(players_stats)} players from API data")
            return players_stats
            
        except Exception as e:
            self.logger.error(f"Error processing API data: {e}")
            return []
    
    def scrape_tournament_recaps(self, tournament_url: str, event_id: str = None) -> int:
        """
        Process tournament using existing API data instead of scraping broken recap URLs
        Returns number of matches processed
        """
        if not event_id:
            event_id = f"Event_{int(time.time())}"
        
        self.logger.info(f"🔄 Processing tournament using API data for event {event_id}")
        
        # Use API data instead of scraping broken recap URLs
        players_stats = self.extract_players_from_api_data(event_id)
        
        if not players_stats:
            self.logger.warning("No player stats extracted from API data")
            return 0
        
        matches_processed = 0
        players_added = 0
        
        # Add to database
        for player_stats in players_stats:
            try:
                success = self.db.add_match_stats(
                    player_name=player_stats['player_name'],
                    event_id=event_id,
                    stats_dict={
                        'three_dart_average': player_stats['three_dart_average'],
                        'legs_played': player_stats.get('legs_played', 0),
                        'legs_won': player_stats.get('legs_won', 0),
                        'legs_lost': player_stats.get('legs_lost', 0),
                        'matches_played': player_stats.get('matches_played', 1),
                        'count_180s': player_stats.get('count_180s', 0),
                        'count_140_plus': player_stats.get('count_140_plus', 0),
                        'count_100_plus': player_stats.get('count_100_plus', 0),
                        'highest_finish': player_stats.get('highest_finish', 0)
                    }
                )
                if success:
                    players_added += 1
                    self.logger.debug(f"Added stats for {player_stats['player_name']}")
                else:
                    self.logger.warning(f"Failed to add stats for {player_stats['player_name']}")
            except Exception as e:
                self.logger.error(f"Error adding player {player_stats['player_name']}: {e}")
                
        # Count unique matches (divide players by 2 since each match has 2 players)
        matches_processed = len(players_stats) // 2
        
        self.logger.info(f"✅ Tournament processing complete. Added {players_added} players from {matches_processed} matches for event {event_id}")
        return matches_processed
    
    def scrape_single_recap(self, recap_url: str, event_id: str) -> bool:
        """Scrape a single recap URL and add to database"""
        try:
            players_stats = self.extract_player_stats_from_recap(recap_url)
            
            success_count = 0
            for player_stats in players_stats:
                success = self.db.add_match_stats(
                    player_name=player_stats['player_name'],
                    event_id=event_id,
                    stats_dict={
                        'three_dart_average': player_stats['three_dart_average'],
                        'legs_played': player_stats['legs_played'],
                        'count_180s': player_stats['count_180s'],
                        'count_140_plus': player_stats['count_140_plus'],
                        'count_100_plus': player_stats['count_100_plus'],
                        'highest_finish': player_stats['highest_finish']
                    }
                )
                if success:
                    success_count += 1
            
            self.logger.info(f"Successfully added stats for {success_count} players from {recap_url}")
            return success_count > 0
            
        except Exception as e:
            self.logger.error(f"Error scraping single recap {recap_url}: {e}")
            return False

    def extract_match_result(self, recap_url: str, match_index: int = 0) -> Optional[Dict[str, Any]]:
        """
        Stage 1 Scraping: Extract basic match result (player names, score, winner)
        This is faster and gets the essential data without detailed stats
        """
        try:
            self.logger.info(f"Extracting match result from: {recap_url}")
            
            # Get the page content
            if self.use_selenium and SELENIUM_AVAILABLE:
                html_content = self._get_page_with_selenium(recap_url)
            else:
                response = self.session.get(recap_url, timeout=30)
                response.raise_for_status()
                html_content = response.text
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract player names
            player_names = self._extract_player_names(soup)
            
            # Extract scores
            scores = self._extract_match_scores(soup)
            
            # Determine winner
            winner = 'Unknown'
            score_str = '0-0'
            if scores and len(scores) >= 2:
                score1, score2 = scores[0], scores[1]
                score_str = f"{score1}-{score2}"
                if score1 > score2:
                    winner = player_names[0] if len(player_names) > 0 else 'Unknown'
                elif score2 > score1:
                    winner = player_names[1] if len(player_names) > 1 else 'Unknown'
            
            # Determine phase and group based on match index
            phase, group = self._classify_match_by_index(match_index)
            
            return {
                'player1': player_names[0] if len(player_names) > 0 else 'Unknown',
                'player2': player_names[1] if len(player_names) > 1 else 'Unknown',
                'score': score_str,
                'winner': winner,
                'phase': phase,
                'group': group
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting match result: {e}", exc_info=True)
            return None

    def extract_sets_count(self, recap_url: str) -> int:
        """
        Extract the number of sets played in a knockout match
        Used for Stage 2 detailed scraping
        """
        try:
            # Get the page content
            if self.use_selenium and SELENIUM_AVAILABLE:
                html_content = self._get_page_with_selenium(recap_url)
            else:
                response = self.session.get(recap_url, timeout=30)
                response.raise_for_status()
                html_content = response.text
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Look for set indicators in the page
            # This is a placeholder - actual implementation depends on DartConnect's HTML structure
            set_headers = soup.find_all(text=re.compile(r'Set\s+\d+', re.IGNORECASE))
            return len(set_headers) if set_headers else 0
            
        except Exception as e:
            self.logger.error(f"Error extracting sets count: {e}")
            return 0

    def _extract_player_names(self, soup: BeautifulSoup) -> List[str]:
        """Extract player names from recap page"""
        player_names = []
        
        # Try common selectors for player names
        name_selectors = [
            {'class': 'player-name'},
            {'class': 'playerName'},
            {'class': 'participant'},
        ]
        
        for selector in name_selectors:
            elements = soup.find_all(attrs=selector)
            if elements:
                player_names = [elem.get_text(strip=True) for elem in elements[:2]]
                break
        
        return player_names

    def _extract_match_scores(self, soup: BeautifulSoup) -> List[int]:
        """Extract match scores from recap page"""
        scores = []
        
        # Try common selectors for scores
        score_selectors = [
            {'class': 'score'},
            {'class': 'match-score'},
            {'class': 'legs-won'},
        ]
        
        for selector in score_selectors:
            elements = soup.find_all(attrs=selector)
            if elements:
                for elem in elements[:2]:
                    try:
                        scores.append(int(elem.get_text(strip=True)))
                    except ValueError:
                        continue
                break
        
        return scores

    def _classify_match_by_index(self, match_index: int) -> Tuple[str, Optional[str]]:
        """
        Classify match phase and group based on match index
        Reuses the logic from scrape_event_for_matches
        """
        match_counter = match_index + 1
        
        if match_counter == 1:
            return 'final', None
        elif match_counter <= 3:
            return 'semifinal', None
        elif match_counter <= 7:
            return 'quarterfinal', None
        elif match_counter <= 17:
            return 'round_robin', 'A'
        elif match_counter <= 27:
            return 'round_robin', 'B'
        else:
            return 'unknown', None

def test_scraper():
    """Test function for the scraper"""
    # Initialize database and scraper
    db = AADSDataManager()
    scraper = DartConnectScraper(db, log_level=logging.DEBUG)
    
    print("DartConnect Scraper Test")
    print("=" * 40)
    
    # Test URL validation
    test_urls = [
        "https://www.dartconnect.com/history/match/12345",
        "https://dartconnect.com/dart/Recap.aspx?ID=67890",
        "https://example.com/not-dartconnect"
    ]
    
    for url in test_urls:
        is_valid = scraper.is_dartconnect_url(url)
        print(f"URL: {url}")
        print(f"Is DartConnect URL: {is_valid}")
        print()
    
    print("Test complete. Ready for real tournament URLs.")

if __name__ == "__main__":
    test_scraper()