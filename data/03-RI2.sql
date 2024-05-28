CREATE OR REPLACE FUNCTION check_medico_paciente_nif(nif_medico CHAR(9), consulta_ssn CHAR(11)) RETURNS BOOLEAN AS $$
BEGIN
    RETURN NOT EXISTS (SELECT 1 FROM paciente WHERE ssn = consulta_ssn AND nif = nif_medico);
END;
$$ LANGUAGE plpgsql;

ALTER TABLE consulta
ADD CONSTRAINT consultar_proprio_medico_check CHECK (check_medico_paciente_nif(nif, ssn));