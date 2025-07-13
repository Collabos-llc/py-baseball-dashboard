-- PostgreSQL initialization script for Baseball Analytics
-- This script creates the necessary tables for storing baseball data and betting insights

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create players table
CREATE TABLE IF NOT EXISTS players (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    player_name VARCHAR(255) NOT NULL,
    team VARCHAR(10),
    position VARCHAR(10),
    batting_side CHAR(1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create games table
CREATE TABLE IF NOT EXISTS games (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game_pk BIGINT UNIQUE NOT NULL,
    game_date DATE NOT NULL,
    home_team VARCHAR(10) NOT NULL,
    away_team VARCHAR(10) NOT NULL,
    weather_temp FLOAT,
    weather_wind_speed FLOAT,
    weather_wind_direction VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create pitches table for detailed Statcast data
CREATE TABLE IF NOT EXISTS pitches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game_pk BIGINT NOT NULL,
    player_name VARCHAR(255),
    pitcher VARCHAR(255),
    batter VARCHAR(255),
    events VARCHAR(100),
    description VARCHAR(100),
    pitch_type VARCHAR(10),
    release_speed FLOAT,
    launch_speed FLOAT,
    launch_angle FLOAT,
    hit_distance_sc FLOAT,
    plate_x FLOAT,
    plate_z FLOAT,
    sz_top FLOAT,
    sz_bot FLOAT,
    estimated_woba_using_speedangle FLOAT,
    woba_value FLOAT,
    at_bat_number INTEGER,
    pitch_number INTEGER,
    inning INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (game_pk) REFERENCES games(game_pk)
);

-- Create betting_insights table for storing analysis results
CREATE TABLE IF NOT EXISTS betting_insights (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    player_name VARCHAR(255) NOT NULL,
    insight_type VARCHAR(50) NOT NULL, -- 'sweet_spot', 'fatigue', 'weather', 'umpire', etc.
    insight_value JSONB NOT NULL,
    confidence_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    game_date DATE,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create umpire_analysis table
CREATE TABLE IF NOT EXISTS umpire_analysis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    umpire_name VARCHAR(255) NOT NULL,
    game_pk BIGINT NOT NULL,
    zone VARCHAR(20),
    total_calls INTEGER,
    correct_calls INTEGER,
    accuracy_percentage FLOAT,
    strike_rate FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (game_pk) REFERENCES games(game_pk)
);

-- Create player_profiles table for aggregated metrics
CREATE TABLE IF NOT EXISTS player_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    player_name VARCHAR(255) NOT NULL,
    season INTEGER NOT NULL,
    avg_exit_velocity FLOAT,
    barrel_rate FLOAT,
    hard_hit_rate FLOAT,
    sweet_spot_rate FLOAT,
    pull_rate FLOAT,
    expected_woba FLOAT,
    power_score FLOAT,
    betting_grade VARCHAR(10), -- 'ELITE', 'ABOVE_AVG', 'DEVELOPING'
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(player_name, season)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_pitches_player_name ON pitches(player_name);
CREATE INDEX IF NOT EXISTS idx_pitches_game_pk ON pitches(game_pk);
CREATE INDEX IF NOT EXISTS idx_pitches_events ON pitches(events);
CREATE INDEX IF NOT EXISTS idx_games_date ON games(game_date);
CREATE INDEX IF NOT EXISTS idx_betting_insights_player ON betting_insights(player_name);
CREATE INDEX IF NOT EXISTS idx_betting_insights_type ON betting_insights(insight_type);
CREATE INDEX IF NOT EXISTS idx_betting_insights_date ON betting_insights(game_date);

-- Create a view for quick betting insights
CREATE OR REPLACE VIEW active_betting_insights AS
SELECT 
    bi.*,
    pp.power_score,
    pp.betting_grade
FROM betting_insights bi
LEFT JOIN player_profiles pp ON bi.player_name = pp.player_name
WHERE bi.is_active = TRUE 
AND bi.created_at >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY bi.confidence_score DESC;

-- Sample data insertion function
CREATE OR REPLACE FUNCTION insert_sample_data()
RETURNS void AS $$
BEGIN
    -- Insert sample teams if games table is empty
    IF NOT EXISTS (SELECT 1 FROM games LIMIT 1) THEN
        INSERT INTO games (game_pk, game_date, home_team, away_team, weather_temp, weather_wind_speed) VALUES
        (123456, CURRENT_DATE - 1, 'NYY', 'BOS', 75.0, 8.5),
        (123457, CURRENT_DATE - 1, 'LAD', 'SF', 82.0, 12.3),
        (123458, CURRENT_DATE, 'HOU', 'TEX', 88.0, 15.2);
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Run the sample data function
SELECT insert_sample_data();

-- Grant permissions to parlayjaye user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO parlayjaye;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO parlayjaye;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO parlayjaye;