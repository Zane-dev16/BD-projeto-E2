DROP TABLE IF EXISTS horarios_validos;
CREATE TABLE horarios_validos (
    data DATE NOT NULL,
    hora TIME NOT NULL,
    PRIMARY KEY (data, hora)
);

WITH RECURSIVE times_manha AS (
    SELECT TIME '08:00:00' AS time
    UNION ALL
    SELECT time + INTERVAL '30 minute'
    FROM times_manha
    WHERE time < '13:00:00'
), times_tarde AS (
    SELECT TIME '14:00:00' AS time
    UNION ALL
    SELECT time + INTERVAL '30 minute'
    FROM times_tarde
    WHERE time < '19:00:00'
), dates AS (
    SELECT generate_series('2024-01-01'::date, '2024-12-31'::date, INTERVAL '1 day') AS date
)
INSERT INTO horarios_validos (data, hora)
SELECT dates.date, times_manha.time
FROM dates, times_manha
UNION ALL
SELECT dates.date, times_tarde.time
FROM dates, times_tarde;

DROP TABLE IF EXISTS times_manha;
DROP TABLE IF EXISTS times_tarde;
