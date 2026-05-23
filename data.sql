-- ============================================================
--  edge_tutor_data.db – Edge-Optimized Long-Term Memory
--  Hardware Target: Raspberry Pi 5 (LPDDR4X / SD Card)
--  Architecture: Deterministic Telemetry (No Background LLM)
-- ============================================================

PRAGMA journal_mode=WAL; 
PRAGMA foreign_keys=ON;

-- 1. USERS (Authentication & Routing)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    display_name TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    last_login TEXT
);

-- 2. MASTER LEARNING PROFILE (The "System Persona" Injector)
CREATE TABLE IF NOT EXISTS learning_profile (
    user_id INTEGER NOT NULL,
    topic TEXT NOT NULL,                      
    proficiency_score REAL DEFAULT 0.5,       
    total_questions_attempted INTEGER DEFAULT 0,
    total_correct INTEGER DEFAULT 0,
    last_updated TEXT DEFAULT (datetime('now')),
    PRIMARY KEY (user_id, topic),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 3. TEST SESSIONS (Quiz Mode Telemetry)
CREATE TABLE IF NOT EXISTS test_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    topic TEXT NOT NULL,
    started_at TEXT DEFAULT (datetime('now')),
    completed_at TEXT,
    score REAL,                               
    total_questions INTEGER,
    correct_answers INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 4. QUESTION RESPONSES (Granular Telemetry)
CREATE TABLE IF NOT EXISTS question_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    user_answer TEXT,
    is_correct INTEGER,                       
    response_time_seconds REAL,               
    FOREIGN KEY (session_id) REFERENCES test_sessions(id)
);

-- 5. TUTORING LOG (Development / Thesis Evaluation)
CREATE TABLE IF NOT EXISTS tutoring_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    intent_classification TEXT,               
    rag_distance_score REAL,                  
    latency_ms INTEGER,                       
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Indices for ultra-fast LPDDR4X lookups
CREATE INDEX IF NOT EXISTS idx_learning_profile_user ON learning_profile(user_id);
CREATE INDEX IF NOT EXISTS idx_test_sessions_user ON test_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_question_responses_session ON question_responses(session_id);