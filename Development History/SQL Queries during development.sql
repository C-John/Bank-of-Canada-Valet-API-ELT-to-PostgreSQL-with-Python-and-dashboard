DROP TABLE IF EXISTS raw_valet_data;

CREATE TABLE raw_valet_data (
    raw_content JSONB
);

SELECT * 
FROM raw_valet_data;

SELECT length(raw_content::text) FROM raw_valet_data;

SELECT raw_content ->> 'terms' FROM raw_valet_data;

SELECT raw_content -> 'observations' FROM raw_valet_data;

DELETE FROM raw_valet_data
WHERE raw_content IS NOT NULL;

SELECT 
    c.date_id, 
    c.day_name
FROM calendar c
LEFT JOIN observations o ON c.date_id = o.date_id
WHERE c.is_weekend = FALSE 
  AND c.date_id <= (SELECT MAX(date_id) FROM observations) -- Only look at the past
  AND o.date_id IS NULL                                   -- Find the gaps
ORDER BY c.date_id DESC;

CREATE OR REPLACE VIEW v_daily_exchange_rates AS
SELECT 
    obs.date_id AS date,
    meta.label AS currency,
    obs.value AS rate,
    meta.description
FROM observations obs
JOIN series_metadata meta ON obs.series_id = meta.series_id
ORDER BY obs.date_id DESC, meta.label ASC;

SELECT date, currency, rate, description 
                    FROM v_daily_exchange_rates;

SELECT * FROM series_metadata;

SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';