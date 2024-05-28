'''historial_paciente(id, ssn, nif, nome, data, ano, mes, dia_do_mes, localidade, especialidade, tipo, chave,
valor'''
CREATE MATERIALIZED VIEW historial_paciente [IF NOT EXISTS] historial_paciente AS 
    SELECT id , ssn, nif, c.nome , data, EXTRACT(YEAR FROM data) AS ano, EXTRACT(MONTH FROM data) AS mes, EXTRACT(DAY FROM data) AS dia_do_mes, SUBSTRING(morada, CHARINDEX(',', REVERSE(morada)) + 10) , especialidade, 'obeservacao' AS tipo, parametro as chave, valor
    FROM observacao JOIN consulta USING(id) JOIN medico USING(nif) JOIN paciente USING(ssn) JOIN clinica c USING(c.nome) 
    UNION
    SELECT id , ssn, nif, c.nome, data, EXTRACT(YEAR FROM data) AS ano, EXTRACT(MONTH FROM data) AS mes, EXTRACT(DAY FROM data) AS dia_do_mes, SUBSTRING(morada, CHARINDEX(',', REVERSE(morada)) + 10) , especialidade, 'receita' AS tipo, medicamento as chave, quantidade as valor
    FROM receita JOIN consulta USING(codigo_sns) JOIN medico USING(nif) JOIN paciente USING(ssn) JOIN clinica c USING(c.nome)

