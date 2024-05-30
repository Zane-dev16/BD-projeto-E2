DROP TABLE IF EXISTS horarios_validos;
CREATE TABLE horarios_validos (
    data DATE NOT NULL,
    hora TIME NOT NULL,
    PRIMARY KEY (data, hora)
);

WITH RECURSIVE dates AS (
    SELECT DATE '2024-01-01' AS date
    UNION ALL
    SELECT date + INTERVAL '1 day'
    FROM dates
    WHERE date < '2024-12-31'
),
times AS (
    SELECT TIME '08:00:00' AS time
    UNION ALL
    SELECT time + INTERVAL '30 minute'
    FROM times
    WHERE (time < '13:00:00') OR (time >= '14:00:00' AND time < '19:00:00')
)
INSERT INTO horarios_validos (data, hora)
SELECT d.date AS data, t.time AS hora
FROM dates d, times t;

DROP TABLE IF EXISTS dates;
DROP TABLE IF EXISTS times;
