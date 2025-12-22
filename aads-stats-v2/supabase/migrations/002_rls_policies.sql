-- AADS Stats Engine V2 - Row Level Security Policies
-- Access Control for Admin and Public Data

-- ============================================
-- Enable RLS on all tables
-- ============================================
ALTER TABLE players ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE matches ENABLE ROW LEVEL SECURITY;
ALTER TABLE staging_matches ENABLE ROW LEVEL SECURITY;
ALTER TABLE event_standings ENABLE ROW LEVEL SECURITY;
ALTER TABLE series_leaderboard ENABLE ROW LEVEL SECURITY;
ALTER TABLE brand_sponsors ENABLE ROW LEVEL SECURITY;
ALTER TABLE admin_users ENABLE ROW LEVEL SECURITY;

-- ============================================
-- HELPER FUNCTION: Check if user is admin
-- ============================================
CREATE OR REPLACE FUNCTION is_admin()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM admin_users
        WHERE email = auth.jwt()->>'email'
        AND is_active = TRUE
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================
-- PLAYERS TABLE POLICIES
-- ============================================
-- Public can read all players
CREATE POLICY "Public read access to players"
    ON players FOR SELECT
    USING (true);

-- Only admins can insert/update/delete players
CREATE POLICY "Admins can manage players"
    ON players FOR ALL
    USING (is_admin())
    WITH CHECK (is_admin());

-- ============================================
-- EVENTS TABLE POLICIES
-- ============================================
-- Public can read all events
CREATE POLICY "Public read access to events"
    ON events FOR SELECT
    USING (true);

-- Only admins can manage events
CREATE POLICY "Admins can manage events"
    ON events FOR ALL
    USING (is_admin())
    WITH CHECK (is_admin());

-- ============================================
-- MATCHES TABLE POLICIES (Production Data)
-- ============================================
-- Public can read all matches
CREATE POLICY "Public read access to matches"
    ON matches FOR SELECT
    USING (true);

-- Only admins can insert/update/delete matches
CREATE POLICY "Admins can manage matches"
    ON matches FOR ALL
    USING (is_admin())
    WITH CHECK (is_admin());

-- ============================================
-- STAGING_MATCHES TABLE POLICIES (Admin Only)
-- ============================================
-- Only admins can access staging data
CREATE POLICY "Admins only access to staging"
    ON staging_matches FOR ALL
    USING (is_admin())
    WITH CHECK (is_admin());

-- ============================================
-- EVENT_STANDINGS TABLE POLICIES
-- ============================================
-- Public can read event standings
CREATE POLICY "Public read access to event standings"
    ON event_standings FOR SELECT
    USING (true);

-- System can update standings (via triggers)
CREATE POLICY "System can manage event standings"
    ON event_standings FOR ALL
    USING (true)
    WITH CHECK (true);

-- ============================================
-- SERIES_LEADERBOARD TABLE POLICIES
-- ============================================
-- Public can read series leaderboard
CREATE POLICY "Public read access to series leaderboard"
    ON series_leaderboard FOR SELECT
    USING (true);

-- System can update leaderboard (via triggers)
CREATE POLICY "System can manage series leaderboard"
    ON series_leaderboard FOR ALL
    USING (true)
    WITH CHECK (true);

-- ============================================
-- BRAND_SPONSORS TABLE POLICIES
-- ============================================
-- Public can read active sponsors
CREATE POLICY "Public read active sponsors"
    ON brand_sponsors FOR SELECT
    USING (is_active = true);

-- Admins can manage all sponsors
CREATE POLICY "Admins can manage sponsors"
    ON brand_sponsors FOR ALL
    USING (is_admin())
    WITH CHECK (is_admin());

-- ============================================
-- ADMIN_USERS TABLE POLICIES
-- ============================================
-- Only admins can read admin users
CREATE POLICY "Admins can view admin users"
    ON admin_users FOR SELECT
    USING (is_admin());

-- Only super admins can modify admin users
CREATE POLICY "Super admins can manage admin users"
    ON admin_users FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM admin_users
            WHERE email = auth.jwt()->>'email'
            AND role = 'super_admin'
            AND is_active = TRUE
        )
    )
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM admin_users
            WHERE email = auth.jwt()->>'email'
            AND role = 'super_admin'
            AND is_active = TRUE
        )
    );

-- ============================================
-- API HELPER FUNCTIONS FOR FRONTEND
-- ============================================

-- Get player stats with filtering
CREATE OR REPLACE FUNCTION get_player_stats(
    p_player_id UUID,
    p_filter VARCHAR DEFAULT 'all' -- 'all', 'event_1', 'knockouts', 'series'
)
RETURNS TABLE (
    player_name VARCHAR,
    total_matches INTEGER,
    total_wins INTEGER,
    total_losses INTEGER,
    legs_won INTEGER,
    legs_lost INTEGER,
    leg_difference INTEGER,
    average_3da DECIMAL,
    highest_checkout INTEGER,
    total_180s INTEGER
) AS $$
BEGIN
    IF p_filter = 'event_1' THEN
        RETURN QUERY
        SELECT 
            p.name,
            COUNT(m.id)::INTEGER,
            COUNT(CASE WHEN m.winner_id = p_player_id THEN 1 END)::INTEGER,
            COUNT(CASE WHEN m.winner_id != p_player_id THEN 1 END)::INTEGER,
            SUM(CASE WHEN m.player_1_id = p_player_id THEN m.player_1_legs ELSE m.player_2_legs END)::INTEGER,
            SUM(CASE WHEN m.player_1_id = p_player_id THEN m.player_2_legs ELSE m.player_1_legs END)::INTEGER,
            (SUM(CASE WHEN m.player_1_id = p_player_id THEN m.player_1_legs ELSE m.player_2_legs END) -
             SUM(CASE WHEN m.player_1_id = p_player_id THEN m.player_2_legs ELSE m.player_1_legs END))::INTEGER,
            AVG(CASE WHEN m.player_1_id = p_player_id THEN m.player_1_average ELSE m.player_2_average END)::DECIMAL,
            MAX(CASE WHEN m.player_1_id = p_player_id THEN m.player_1_highest_checkout ELSE m.player_2_highest_checkout END)::INTEGER,
            SUM(CASE WHEN m.player_1_id = p_player_id THEN m.player_1_180s ELSE m.player_2_180s END)::INTEGER
        FROM players p
        JOIN matches m ON (m.player_1_id = p.id OR m.player_2_id = p.id)
        JOIN events e ON m.event_id = e.id
        WHERE p.id = p_player_id AND e.event_number = 1
        GROUP BY p.name;
    
    ELSIF p_filter = 'knockouts' THEN
        RETURN QUERY
        SELECT 
            p.name,
            COUNT(m.id)::INTEGER,
            COUNT(CASE WHEN m.winner_id = p_player_id THEN 1 END)::INTEGER,
            COUNT(CASE WHEN m.winner_id != p_player_id THEN 1 END)::INTEGER,
            SUM(CASE WHEN m.player_1_id = p_player_id THEN m.player_1_legs ELSE m.player_2_legs END)::INTEGER,
            SUM(CASE WHEN m.player_1_id = p_player_id THEN m.player_2_legs ELSE m.player_1_legs END)::INTEGER,
            (SUM(CASE WHEN m.player_1_id = p_player_id THEN m.player_1_legs ELSE m.player_2_legs END) -
             SUM(CASE WHEN m.player_1_id = p_player_id THEN m.player_2_legs ELSE m.player_1_legs END))::INTEGER,
            AVG(CASE WHEN m.player_1_id = p_player_id THEN m.player_1_average ELSE m.player_2_average END)::DECIMAL,
            MAX(CASE WHEN m.player_1_id = p_player_id THEN m.player_1_highest_checkout ELSE m.player_2_highest_checkout END)::INTEGER,
            SUM(CASE WHEN m.player_1_id = p_player_id THEN m.player_1_180s ELSE m.player_2_180s END)::INTEGER
        FROM players p
        JOIN matches m ON (m.player_1_id = p.id OR m.player_2_id = p.id)
        WHERE p.id = p_player_id AND m.phase != 'round_robin'
        GROUP BY p.name;
    
    ELSE -- 'all' or 'series'
        RETURN QUERY
        SELECT 
            p.name,
            sl.total_matches_played,
            sl.total_match_wins,
            sl.total_match_losses,
            sl.total_legs_won,
            sl.total_legs_lost,
            sl.leg_difference,
            sl.overall_3da,
            sl.highest_checkout,
            sl.total_180s
        FROM players p
        LEFT JOIN series_leaderboard sl ON p.id = sl.player_id
        WHERE p.id = p_player_id;
    END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Get tournament bracket for an event
CREATE OR REPLACE FUNCTION get_knockout_bracket(p_event_id UUID)
RETURNS TABLE (
    round VARCHAR,
    match_number INTEGER,
    player_1_name VARCHAR,
    player_2_name VARCHAR,
    player_1_score INTEGER,
    player_2_score INTEGER,
    winner_name VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        m.phase::VARCHAR,
        m.match_number,
        p1.name,
        p2.name,
        m.player_1_legs,
        m.player_2_legs,
        pw.name
    FROM matches m
    JOIN players p1 ON m.player_1_id = p1.id
    JOIN players p2 ON m.player_2_id = p2.id
    LEFT JOIN players pw ON m.winner_id = pw.id
    WHERE m.event_id = p_event_id
        AND m.phase IN ('quarterfinal', 'semifinal', 'final')
    ORDER BY 
        CASE m.phase
            WHEN 'quarterfinal' THEN 1
            WHEN 'semifinal' THEN 2
            WHEN 'final' THEN 3
        END,
        m.match_number;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
