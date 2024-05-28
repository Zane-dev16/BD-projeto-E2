ALTER TABLE consulta
ADD CONSTRAINT consulta_hora_check CHECK ((EXTRACT(MINUTE FROM hora) = 0 OR EXTRACT(MINUTE FROM hora) = 30) AND
    (hora >= '08:00:00' AND hora <= '13:00:00') OR
    (hora >= '14:00:00' AND hora <= '19:00:00'))