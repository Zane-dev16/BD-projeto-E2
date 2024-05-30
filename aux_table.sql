DROP TABLE IF EXISTS horarios_validos;
CREATE TABLE horarios_validos (
    data DATE NOT NULL,
    hora TIME NOT NULL,
    PRIMARY KEY (data, hora)
);

WITH RECURSIVE times AS (
    SELECT TIME '08:00:00' AS time
    UNION ALL
    SELECT time + INTERVAL '30 minute'
    FROM times
    WHERE (time < '13:00:00') OR (time >= '14:00:00' AND time < '19:00:00')
), dates AS (
    SELECT generate_series('2024-01-01'::date, '2024-12-31'::date, INTERVAL '1 day') AS date
)
INSERT INTO horarios_validos (data, hora)
SELECT dates.date, times.time
FROM dates, times;

DROP TABLE IF EXISTS times;
