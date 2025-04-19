-- Δημιουργία βάσης δεδομένων
CREATE DATABASE casewise_db;

-- Σύνδεση στη βάση δεδομένων
\c casewise_db;

-- Δημιουργία πίνακα Laws
CREATE TABLE laws (
    law_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Δημιουργία πίνακα Articles
CREATE TABLE articles (
    article_id SERIAL PRIMARY KEY,
    law_id INTEGER REFERENCES laws(law_id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    article_number VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Δημιουργία πίνακα Categories
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Δημιουργία πίνακα Article_Categories (για τη σχέση N:M)
CREATE TABLE article_categories (
    article_id INTEGER REFERENCES articles(article_id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(category_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (article_id, category_id)
);

-- Δημιουργία triggers για ενημέρωση του updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Εφαρμογή triggers στους πίνακες
CREATE TRIGGER update_laws_updated_at
    BEFORE UPDATE ON laws
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_articles_updated_at
    BEFORE UPDATE ON articles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_categories_updated_at
    BEFORE UPDATE ON categories
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Δημιουργία indexes για καλύτερη απόδοση
CREATE INDEX idx_articles_law_id ON articles(law_id);
CREATE INDEX idx_article_categories_article_id ON article_categories(article_id);
CREATE INDEX idx_article_categories_category_id ON article_categories(category_id);
CREATE INDEX idx_categories_name ON categories(name); 