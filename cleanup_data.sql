-- Διαγραφή δεδομένων με τη σωστή σειρά λόγω foreign key constraints
DELETE FROM article_categories;
DELETE FROM articles;
DELETE FROM categories;
DELETE FROM laws;

-- Επαναφορά των sequences στα 1
ALTER SEQUENCE laws_law_id_seq RESTART WITH 1;
ALTER SEQUENCE articles_article_id_seq RESTART WITH 1;
ALTER SEQUENCE categories_category_id_seq RESTART WITH 1; 