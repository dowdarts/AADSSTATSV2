-- Migration: Add event_number tracking to staging_matches and matches tables
-- Purpose: Support Events 1-6 with separate stats per event

-- Add event_number column to staging_matches
ALTER TABLE staging_matches 
ADD COLUMN IF NOT EXISTS event_number INTEGER CHECK (event_number BETWEEN 1 AND 7);

-- Add event_number column to matches
ALTER TABLE matches 
ADD COLUMN IF NOT EXISTS event_number INTEGER CHECK (event_number BETWEEN 1 AND 7);

-- Add detailed stat columns for Stage 2 scraping
ALTER TABLE staging_matches
ADD COLUMN IF NOT EXISTS player_1_100_plus INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS player_1_120_plus INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS player_1_140_plus INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS player_1_160_plus INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS player_2_100_plus INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS player_2_120_plus INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS player_2_140_plus INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS player_2_160_plus INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS player_1_doubles_hit INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS player_1_doubles_attempted INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS player_2_doubles_hit INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS player_2_doubles_attempted INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS is_knockout BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS scrape_stage VARCHAR(20) DEFAULT 'match_results' CHECK (scrape_stage IN ('match_results', 'match_details', 'complete'));

-- Add same columns to production matches table
ALTER TABLE matches
ADD COLUMN IF NOT EXISTS player_1_100_plus INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS player_1_120_plus INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS player_1_140_plus INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS player_1_160_plus INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS player_2_100_plus INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS player_2_120_plus INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS player_2_140_plus INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS player_2_160_plus INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS player_1_doubles_hit INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS player_1_doubles_attempted INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS player_2_doubles_hit INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS player_2_doubles_attempted INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS is_knockout BOOLEAN DEFAULT FALSE;

-- Create index for faster event-based queries
CREATE INDEX IF NOT EXISTS idx_staging_matches_event_number ON staging_matches(event_number);
CREATE INDEX IF NOT EXISTS idx_matches_event_number ON matches(event_number);
CREATE INDEX IF NOT EXISTS idx_staging_matches_scrape_stage ON staging_matches(scrape_stage);

-- Update event_standings view to include event_number
DROP VIEW IF EXISTS event_standings;
CREATE OR REPLACE VIEW event_standings AS
SELECT 
    e.id AS event_id,
    e.event_number,
    e.event_name,
    p.id AS player_id,
    p.name AS player_name,
    COUNT(DISTINCT m.id) AS matches_played,
    SUM(CASE WHEN m.winner_id = p.id THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN m.winner_id != p.id THEN 1 ELSE 0 END) AS losses,
    SUM(CASE 
        WHEN m.player_1_id = p.id THEN m.player_1_legs 
        WHEN m.player_2_id = p.id THEN m.player_2_legs 
        ELSE 0 
    END) AS legs_won,
    SUM(CASE 
        WHEN m.player_1_id = p.id THEN m.player_2_legs 
        WHEN m.player_2_id = p.id THEN m.player_1_legs 
        ELSE 0 
    END) AS legs_lost,
    (SUM(CASE 
        WHEN m.player_1_id = p.id THEN m.player_1_legs 
        WHEN m.player_2_id = p.id THEN m.player_2_legs 
        ELSE 0 
    END) - SUM(CASE 
        WHEN m.player_1_id = p.id THEN m.player_2_legs 
        WHEN m.player_2_id = p.id THEN m.player_1_legs 
        ELSE 0 
    END)) AS leg_difference,
    AVG(CASE 
        WHEN m.player_1_id = p.id THEN m.player_1_average 
        WHEN m.player_2_id = p.id THEN m.player_2_average 
    END) AS average_3da,
    MAX(CASE 
        WHEN m.player_1_id = p.id THEN m.player_1_highest_checkout 
        WHEN m.player_2_id = p.id THEN m.player_2_highest_checkout 
    END) AS highest_checkout,
    SUM(CASE 
        WHEN m.player_1_id = p.id THEN m.player_1_180s 
        WHEN m.player_2_id = p.id THEN m.player_2_180s 
        ELSE 0 
    END) AS total_180s,
    m.group_name
FROM 
    matches m
    JOIN events e ON m.event_id = e.id
    JOIN players p ON (m.player_1_id = p.id OR m.player_2_id = p.id)
GROUP BY 
    e.id, e.event_number, e.event_name, p.id, p.name, m.group_name
ORDER BY 
    e.event_number, wins DESC, leg_difference DESC, average_3da DESC;

COMMENT ON COLUMN staging_matches.event_number IS 'AADS Event number (1-6 for regular events, 7 for Tournament of Champions)';
COMMENT ON COLUMN matches.event_number IS 'AADS Event number (1-6 for regular events, 7 for Tournament of Champions)';
COMMENT ON COLUMN staging_matches.scrape_stage IS 'Tracks scraping progress: match_results (Stage 1), match_details (Stage 2), complete';
COMMENT ON COLUMN staging_matches.is_knockout IS 'TRUE for set play (knockout), FALSE for best of 5 legs (round robin)';
