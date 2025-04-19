-- Δημιουργία πίνακα Laws (Νόμοι)
CREATE TABLE IF NOT EXISTS laws (
    law_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Δημιουργία πίνακα Articles (Άρθρα)
CREATE TABLE IF NOT EXISTS articles (
    article_id SERIAL PRIMARY KEY,
    law_id INTEGER NOT NULL,
    article_number VARCHAR(50) NOT NULL,
    title VARCHAR(255),
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (law_id) REFERENCES laws(law_id) ON DELETE CASCADE
);

-- Δημιουργία πίνακα Categories (Κατηγορίες)
CREATE TABLE IF NOT EXISTS categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Δημιουργία πίνακα Article_Categories (Σύνδεση Άρθρων-Κατηγοριών)
CREATE TABLE IF NOT EXISTS article_categories (
    article_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (article_id, category_id),
    FOREIGN KEY (article_id) REFERENCES articles(article_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE
);

-- Δημιουργία ευρετηρίου για γρήγορη αναζήτηση άρθρων
CREATE INDEX idx_articles_law_id ON articles(law_id);
CREATE INDEX idx_articles_article_number ON articles(article_number);
CREATE INDEX idx_article_categories_article_id ON article_categories(article_id);
CREATE INDEX idx_article_categories_category_id ON article_categories(category_id);

-- Δημιουργία trigger για αυτόματη ενημέρωση του updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Εφαρμογή του trigger στους πίνακες
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