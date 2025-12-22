-- AADS Stats Engine V2 - Supabase Schema
-- Atlantic Amateur Darts Series Database Schema

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- PLAYERS TABLE
-- ============================================
CREATE TABLE players (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255),
    phone VARCHAR(50),
    profile_image_url TEXT,
    
    -- Aggregated Series Stats
    series_total_wins INTEGER DEFAULT 0,
    series_total_matches INTEGER DEFAULT 0,
    series_total_legs_won INTEGER DEFAULT 0,
    series_total_legs_lost INTEGER DEFAULT 0,
    series_average_3da DECIMAL(5,2) DEFAULT 0.00,
    series_highest_checkout INTEGER DEFAULT 0,
    series_180s INTEGER DEFAULT 0,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- ============================================
-- EVENTS TABLE
-- ============================================
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_number INTEGER NOT NULL CHECK (event_number BETWEEN 1 AND 7),
    event_name VARCHAR(255) NOT NULL,
    event_date DATE NOT NULL,
    venue VARCHAR(255),
    
    -- Event Status
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed', 'cancelled')),
    
    -- Event Winner
    winner_id UUID REFERENCES players(id) ON DELETE SET NULL,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(event_number)
);

-- ============================================
-- MATCHES TABLE (Production - Public Data)
-- ============================================
CREATE TABLE matches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    
    -- Match Details
    phase VARCHAR(50) NOT NULL CHECK (phase IN ('round_robin', 'quarterfinal', 'semifinal', 'final')),
    group_name VARCHAR(10) CHECK (group_name IN ('A', 'B', NULL)), -- NULL for knockout stages
    match_number INTEGER,
    
    -- Players
    player_1_id UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    player_2_id UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    
    -- Scores
    player_1_legs INTEGER DEFAULT 0,
    player_2_legs INTEGER DEFAULT 0,
    player_1_sets INTEGER DEFAULT 0,
    player_2_sets INTEGER DEFAULT 0,
    
    -- Statistics
    player_1_average DECIMAL(5,2),
    player_2_average DECIMAL(5,2),
    player_1_highest_checkout INTEGER,
    player_2_highest_checkout INTEGER,
    player_1_180s INTEGER DEFAULT 0,
    player_2_180s INTEGER DEFAULT 0,
    
    -- Winner
    winner_id UUID REFERENCES players(id) ON DELETE SET NULL,
    
    -- Match Details
    match_date TIMESTAMP WITH TIME ZONE,
    board_number INTEGER,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CHECK (player_1_id != player_2_id)
);

-- ============================================
-- STAGING_MATCHES TABLE (Admin Review Queue)
-- ============================================
CREATE TABLE staging_matches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_id UUID REFERENCES events(id) ON DELETE CASCADE,
    
    -- Match Details
    phase VARCHAR(50) NOT NULL CHECK (phase IN ('round_robin', 'quarterfinal', 'semifinal', 'final')),
    group_name VARCHAR(10) CHECK (group_name IN ('A', 'B', NULL)),
    match_number INTEGER,
    
    -- Players (can be names if not yet linked to player IDs)
    player_1_id UUID REFERENCES players(id) ON DELETE SET NULL,
    player_2_id UUID REFERENCES players(id) ON DELETE SET NULL,
    player_1_name VARCHAR(255),
    player_2_name VARCHAR(255),
    
    -- Scores
    player_1_legs INTEGER DEFAULT 0,
    player_2_legs INTEGER DEFAULT 0,
    player_1_sets INTEGER DEFAULT 0,
    player_2_sets INTEGER DEFAULT 0,
    
    -- Statistics
    player_1_average DECIMAL(5,2),
    player_2_average DECIMAL(5,2),
    player_1_highest_checkout INTEGER,
    player_2_highest_checkout INTEGER,
    player_1_180s INTEGER DEFAULT 0,
    player_2_180s INTEGER DEFAULT 0,
    
    -- Winner
    winner_id UUID REFERENCES players(id) ON DELETE SET NULL,
    
    -- Match Details
    match_date TIMESTAMP WITH TIME ZONE,
    board_number INTEGER,
    
    -- Staging Status
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'reviewed', 'approved', 'rejected')),
    review_notes TEXT,
    reviewed_by VARCHAR(255),
    reviewed_at TIMESTAMP WITH TIME ZONE,
    
    -- Source Information
    source VARCHAR(100), -- e.g., 'scraper', 'manual_entry'
    raw_data JSONB, -- Store original scraped data
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- EVENT_STANDINGS TABLE
-- ============================================
CREATE TABLE event_standings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    player_id UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    group_name VARCHAR(10) CHECK (group_name IN ('A', 'B', NULL)),
    
    -- Round Robin Stats
    matches_played INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    legs_won INTEGER DEFAULT 0,
    legs_lost INTEGER DEFAULT 0,
    leg_difference INTEGER DEFAULT 0,
    
    -- 3-Dart Average
    average_3da DECIMAL(5,2) DEFAULT 0.00,
    
    -- Rankings
    rank INTEGER,
    qualified_for_knockout BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(event_id, player_id, group_name)
);

-- ============================================
-- SERIES_LEADERBOARD (View/Materialized)
-- ============================================
CREATE TABLE series_leaderboard (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    player_id UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    
    -- Series Performance
    total_events_played INTEGER DEFAULT 0,
    total_wins INTEGER DEFAULT 0,
    total_matches_played INTEGER DEFAULT 0,
    total_match_wins INTEGER DEFAULT 0,
    total_match_losses INTEGER DEFAULT 0,
    
    -- Leg Stats
    total_legs_won INTEGER DEFAULT 0,
    total_legs_lost INTEGER DEFAULT 0,
    leg_difference INTEGER DEFAULT 0,
    
    -- 3-Dart Average
    overall_3da DECIMAL(5,2) DEFAULT 0.00,
    rr_only_3da DECIMAL(5,2) DEFAULT 0.00,
    ko_only_3da DECIMAL(5,2) DEFAULT 0.00,
    
    -- Additional Stats
    highest_checkout INTEGER DEFAULT 0,
    total_180s INTEGER DEFAULT 0,
    
    -- Rankings
    overall_rank INTEGER,
    
    -- Metadata
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(player_id)
);

-- ============================================
-- BRAND_SPONSORS TABLE
-- ============================================
CREATE TABLE brand_sponsors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    logo_url TEXT,
    website_url TEXT,
    sponsor_type VARCHAR(50) CHECK (sponsor_type IN ('organization', 'title_sponsor', 'partner', 'venue')),
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- ADMIN_USERS TABLE
-- ============================================
CREATE TABLE admin_users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL UNIQUE,
    role VARCHAR(50) DEFAULT 'admin' CHECK (role IN ('super_admin', 'admin', 'moderator')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- ============================================
-- INDEXES
-- ============================================
CREATE INDEX idx_matches_event_id ON matches(event_id);
CREATE INDEX idx_matches_player_1 ON matches(player_1_id);
CREATE INDEX idx_matches_player_2 ON matches(player_2_id);
CREATE INDEX idx_matches_phase ON matches(phase);
CREATE INDEX idx_staging_matches_status ON staging_matches(status);
CREATE INDEX idx_event_standings_event ON event_standings(event_id);
CREATE INDEX idx_event_standings_player ON event_standings(player_id);
CREATE INDEX idx_series_leaderboard_rank ON series_leaderboard(overall_rank);

-- ============================================
-- FUNCTIONS & TRIGGERS
-- ============================================

-- Update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to all tables
CREATE TRIGGER update_players_updated_at BEFORE UPDATE ON players
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_events_updated_at BEFORE UPDATE ON events
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_matches_updated_at BEFORE UPDATE ON matches
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_staging_matches_updated_at BEFORE UPDATE ON staging_matches
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_event_standings_updated_at BEFORE UPDATE ON event_standings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- FUNCTION: Calculate Leg Difference
-- ============================================
CREATE OR REPLACE FUNCTION calculate_leg_difference(p_event_id UUID, p_player_id UUID, p_group_name VARCHAR)
RETURNS INTEGER AS $$
DECLARE
    v_legs_won INTEGER;
    v_legs_lost INTEGER;
BEGIN
    SELECT 
        COALESCE(SUM(CASE 
            WHEN player_1_id = p_player_id THEN player_1_legs
            WHEN player_2_id = p_player_id THEN player_2_legs
            ELSE 0
        END), 0),
        COALESCE(SUM(CASE 
            WHEN player_1_id = p_player_id THEN player_2_legs
            WHEN player_2_id = p_player_id THEN player_1_legs
            ELSE 0
        END), 0)
    INTO v_legs_won, v_legs_lost
    FROM matches
    WHERE event_id = p_event_id
        AND phase = 'round_robin'
        AND group_name = p_group_name
        AND (player_1_id = p_player_id OR player_2_id = p_player_id);
    
    RETURN v_legs_won - v_legs_lost;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- FUNCTION: Update Event Standings
-- ============================================
CREATE OR REPLACE FUNCTION update_event_standings()
RETURNS TRIGGER AS $$
BEGIN
    -- Update standings for both players in the match
    IF NEW.phase = 'round_robin' THEN
        -- Update player 1
        INSERT INTO event_standings (event_id, player_id, group_name, matches_played, wins, losses, legs_won, legs_lost, leg_difference)
        VALUES (
            NEW.event_id,
            NEW.player_1_id,
            NEW.group_name,
            1,
            CASE WHEN NEW.winner_id = NEW.player_1_id THEN 1 ELSE 0 END,
            CASE WHEN NEW.winner_id = NEW.player_2_id THEN 1 ELSE 0 END,
            NEW.player_1_legs,
            NEW.player_2_legs,
            NEW.player_1_legs - NEW.player_2_legs
        )
        ON CONFLICT (event_id, player_id, group_name)
        DO UPDATE SET
            matches_played = event_standings.matches_played + 1,
            wins = event_standings.wins + CASE WHEN NEW.winner_id = NEW.player_1_id THEN 1 ELSE 0 END,
            losses = event_standings.losses + CASE WHEN NEW.winner_id = NEW.player_2_id THEN 1 ELSE 0 END,
            legs_won = event_standings.legs_won + NEW.player_1_legs,
            legs_lost = event_standings.legs_lost + NEW.player_2_legs,
            leg_difference = calculate_leg_difference(NEW.event_id, NEW.player_1_id, NEW.group_name),
            updated_at = NOW();
        
        -- Update player 2
        INSERT INTO event_standings (event_id, player_id, group_name, matches_played, wins, losses, legs_won, legs_lost, leg_difference)
        VALUES (
            NEW.event_id,
            NEW.player_2_id,
            NEW.group_name,
            1,
            CASE WHEN NEW.winner_id = NEW.player_2_id THEN 1 ELSE 0 END,
            CASE WHEN NEW.winner_id = NEW.player_1_id THEN 1 ELSE 0 END,
            NEW.player_2_legs,
            NEW.player_1_legs,
            NEW.player_2_legs - NEW.player_1_legs
        )
        ON CONFLICT (event_id, player_id, group_name)
        DO UPDATE SET
            matches_played = event_standings.matches_played + 1,
            wins = event_standings.wins + CASE WHEN NEW.winner_id = NEW.player_2_id THEN 1 ELSE 0 END,
            losses = event_standings.losses + CASE WHEN NEW.winner_id = NEW.player_1_id THEN 1 ELSE 0 END,
            legs_won = event_standings.legs_won + NEW.player_2_legs,
            legs_lost = event_standings.legs_lost + NEW.player_1_legs,
            leg_difference = calculate_leg_difference(NEW.event_id, NEW.player_2_id, NEW.group_name),
            updated_at = NOW();
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_event_standings
AFTER INSERT OR UPDATE ON matches
FOR EACH ROW EXECUTE FUNCTION update_event_standings();

-- ============================================
-- FUNCTION: Update Series Stats
-- ============================================
CREATE OR REPLACE FUNCTION update_series_leaderboard()
RETURNS TRIGGER AS $$
BEGIN
    -- Update series leaderboard for both players
    INSERT INTO series_leaderboard (player_id, total_matches_played, total_match_wins, total_match_losses, total_legs_won, total_legs_lost)
    VALUES (
        NEW.player_1_id,
        1,
        CASE WHEN NEW.winner_id = NEW.player_1_id THEN 1 ELSE 0 END,
        CASE WHEN NEW.winner_id = NEW.player_2_id THEN 1 ELSE 0 END,
        NEW.player_1_legs,
        NEW.player_2_legs
    )
    ON CONFLICT (player_id)
    DO UPDATE SET
        total_matches_played = series_leaderboard.total_matches_played + 1,
        total_match_wins = series_leaderboard.total_match_wins + CASE WHEN NEW.winner_id = NEW.player_1_id THEN 1 ELSE 0 END,
        total_match_losses = series_leaderboard.total_match_losses + CASE WHEN NEW.winner_id = NEW.player_2_id THEN 1 ELSE 0 END,
        total_legs_won = series_leaderboard.total_legs_won + NEW.player_1_legs,
        total_legs_lost = series_leaderboard.total_legs_lost + NEW.player_2_legs,
        leg_difference = (series_leaderboard.total_legs_won + NEW.player_1_legs) - (series_leaderboard.total_legs_lost + NEW.player_2_legs),
        updated_at = NOW();
    
    INSERT INTO series_leaderboard (player_id, total_matches_played, total_match_wins, total_match_losses, total_legs_won, total_legs_lost)
    VALUES (
        NEW.player_2_id,
        1,
        CASE WHEN NEW.winner_id = NEW.player_2_id THEN 1 ELSE 0 END,
        CASE WHEN NEW.winner_id = NEW.player_1_id THEN 1 ELSE 0 END,
        NEW.player_2_legs,
        NEW.player_1_legs
    )
    ON CONFLICT (player_id)
    DO UPDATE SET
        total_matches_played = series_leaderboard.total_matches_played + 1,
        total_match_wins = series_leaderboard.total_match_wins + CASE WHEN NEW.winner_id = NEW.player_2_id THEN 1 ELSE 0 END,
        total_match_losses = series_leaderboard.total_match_losses + CASE WHEN NEW.winner_id = NEW.player_1_id THEN 1 ELSE 0 END,
        total_legs_won = series_leaderboard.total_legs_won + NEW.player_2_legs,
        total_legs_lost = series_leaderboard.total_legs_lost + NEW.player_1_legs,
        leg_difference = (series_leaderboard.total_legs_won + NEW.player_2_legs) - (series_leaderboard.total_legs_lost + NEW.player_1_legs),
        updated_at = NOW();
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_series_leaderboard
AFTER INSERT OR UPDATE ON matches
FOR EACH ROW EXECUTE FUNCTION update_series_leaderboard();
