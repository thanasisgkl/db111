-- Δημιουργία του πίνακα penal_code_articles
CREATE TABLE IF NOT EXISTS penal_code_articles (
    id SERIAL PRIMARY KEY,
    article_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
); 