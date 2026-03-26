CREATE TABLE IF NOT EXISTS currency_db_elt.public.series_metadata (
    series_id TEXT PRIMARY KEY,
    label TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS currency_db_elt.public.calendar (
    date_id DATE PRIMARY KEY,
    year INT,
    month INT,
    day INT,
    is_weekend BOOLEAN,
    day_name TEXT
);

CREATE TABLE IF NOT EXISTS currency_db_elt.public.observations (
    series_id TEXT REFERENCES currency_db_elt.public.series_metadata(series_id),
    date_id DATE REFERENCES currency_db_elt.public.calendar(date_id),
    value NUMERIC,
    PRIMARY KEY (series_id, date_id)
);

INSERT INTO currency_db_elt.public.series_metadata (series_id, label, description)
SELECT 
    key AS series_id,
    value->>'label',
    value->>'description'
FROM currency_db_elt.public.raw_valet_data,
LATERAL jsonb_each(raw_content->'seriesDetail')
ON CONFLICT (series_id) DO NOTHING;

INSERT INTO currency_db_elt.public.calendar (date_id, year, month, day, is_weekend, day_name)
SELECT 
    datum AS date_id,
    EXTRACT(YEAR FROM datum),
    EXTRACT(MONTH FROM datum),
    EXTRACT(DAY FROM datum),
    CASE WHEN EXTRACT(ISODOW FROM datum) IN (6, 7) THEN TRUE ELSE FALSE END,
    TO_CHAR(datum, 'Day')
FROM generate_series(
    '2017-01-01'::DATE, 
    '2030-12-31'::DATE, 
    '1 day'::interval
) AS datum
ON CONFLICT (date_id) DO NOTHING;

INSERT INTO currency_db_elt.public.observations (series_id, date_id, value)
SELECT 
	kv.key AS series_id,
	(obs->>'d')::DATE,
    (kv.value->>'v')::NUMERIC
FROM currency_db_elt.public.raw_valet_data,
LATERAL jsonb_array_elements(raw_content->'observations') AS obs,
LATERAL jsonb_each(obs - 'd') AS kv
WHERE kv.key <> 'd'AND kv.value ? 'v' AND (kv.value->>'v') <> ''
ON CONFLICT DO NOTHING;

-- CREATE OR REPLACE VIEW currency_db_elt.public.v_daily_exchange_rates AS
-- SELECT 
--     obs.date_id AS date,
--     obs.series_id,
--     meta.label AS currency,
--     obs.value AS rate,
--     meta.description
-- FROM currency_db_elt.public.observations obs
-- JOIN currency_db_elt.public.series_metadata meta ON obs.series_id = meta.series_id
-- ORDER BY obs.date_id DESC, meta.label ASC;

-- Use CASCADE to ensure any dependencies (like other views) are also cleared
DROP VIEW IF EXISTS currency_db_elt.public.v_daily_exchange_rates CASCADE;
DROP TABLE IF EXISTS currency_db_elt.public.v_daily_exchange_rates CASCADE;

-- Ensure every table in the JOIN is fully qualified with the schema name
CREATE VIEW currency_db_elt.public.v_daily_exchange_rates AS
SELECT 
    obs.date_id AS date,
    obs.series_id,
    meta.label AS currency,
    obs.value AS rate,
    meta.description
FROM currency_db_elt.public.observations obs
JOIN currency_db_elt.public.series_metadata meta ON obs.series_id = meta.series_id
ORDER BY obs.date_id DESC, meta.label ASC;
