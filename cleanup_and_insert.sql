-- Καθαρισμός των πινάκων
TRUNCATE TABLE article_categories CASCADE;
TRUNCATE TABLE articles CASCADE;
TRUNCATE TABLE categories CASCADE;
TRUNCATE TABLE laws CASCADE;

-- Εισαγωγή του Ποινικού Κώδικα
INSERT INTO laws (name) VALUES ('Ποινικός Κώδικας') RETURNING law_id;

-- Εισαγωγή των άρθρων από το CSV
CREATE TEMPORARY TABLE temp_articles (
    article_number VARCHAR(50),
    title TEXT,
    text TEXT
);

\copy temp_articles (article_number, title, text) FROM 'penal_codes_utf8.csv' WITH (FORMAT csv, DELIMITER ';', HEADER true, ENCODING 'UTF8');

-- Μεταφορά των δεδομένων στον κανονικό πίνακα articles με το σωστό law_id
INSERT INTO articles (article_number, title, text, law_id)
SELECT 
    article_number,
    title,
    text,
    (SELECT law_id FROM laws WHERE name = 'Ποινικός Κώδικας')
FROM temp_articles;

-- Καθαρισμός του προσωρινού πίνακα
DROP TABLE temp_articles; 