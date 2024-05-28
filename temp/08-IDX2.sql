CREATE INDEX especilidade_nif_idx ON medico(especialidade, nif);
CREATE INDEX consulta_dia_idx ON consulta(data);
CREATE INDEX receita_codigo_sns_idx ON receita(codigo_sns);