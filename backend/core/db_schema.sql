-- ============================================================
-- Straxon-Qart — Supabase Şema Betiği (Faz 1 Güncellemeleri)
-- Supabase SQL Editor'da çalıştırın.
-- ============================================================

-- 1. Digital Footprints (Kullanıcının entegre platform verileri)
CREATE TABLE IF NOT EXISTS digital_footprints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    username VARCHAR(100) NOT NULL,
    data_summary JSONB NOT NULL DEFAULT '{}'::jsonb,
    last_synced_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
    UNIQUE(profile_id, platform)
);

-- 2. News Feed (Jarvis tarafından filtrelenmiş teknoloji haberleri)
CREATE TABLE IF NOT EXISTS news_feed (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    source VARCHAR(50) NOT NULL,       -- 'devto' | 'hackernews'
    summary TEXT,
    tags TEXT[] DEFAULT '{}',
    published_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 3. User Tasks (Genel görev takip: kilometre taşları, Q1-Q4 hedefleri vb.)
CREATE TABLE IF NOT EXISTS user_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    task_type VARCHAR(50) NOT NULL DEFAULT 'milestone', -- 'milestone' | 'q_goal' | 'custom'
    title TEXT NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT false,
    completed_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 4. News Click Logs (Haber tıklaması puanlama için)
CREATE TABLE IF NOT EXISTS news_click_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    news_id UUID REFERENCES news_feed(id) ON DELETE SET NULL,
    clicked_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- İndeksler (performans için)
CREATE INDEX IF NOT EXISTS idx_digital_footprints_profile ON digital_footprints(profile_id);
CREATE INDEX IF NOT EXISTS idx_news_feed_tags ON news_feed USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_news_feed_created ON news_feed(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_user_tasks_profile ON user_tasks(profile_id);
CREATE INDEX IF NOT EXISTS idx_user_tasks_completed ON user_tasks(profile_id, is_completed);
