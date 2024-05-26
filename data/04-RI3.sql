CREATE OR REPLACE FUNCTION check_medico_clinica_dia(nif_medico CHAR(9), nome_clinica VARCHAR(80), consulta_data DATE) RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM trabalha 
        WHERE nif = nif_medico 
        AND nome = nome_clinica
        AND dia_da_semana = EXTRACT(DOW FROM consulta_data)
    );
END;
$$ LANGUAGE plpgsql;

ALTER TABLE consulta
ADD CHECK (check_medico_clinica_dia(nif, nome, data));