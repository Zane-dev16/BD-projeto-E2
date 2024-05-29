#!/usr/bin/python3
# Copyright (c) BDist Development Team
# Distributed under the terms of the Modified BSD License.
import os
from logging.config import dictConfig

from flask import Flask, jsonify, request
from psycopg.rows import namedtuple_row
from psycopg_pool import ConnectionPool

# Use the DATABASE_URL environment variable if it exists, otherwise use the default.
# Use the format postgres://username:password@hostname/database_name to connect to the database.
DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://bank:bank@postgres/bank")

pool = ConnectionPool(
    conninfo=DATABASE_URL,
    kwargs={
        "autocommit": True,  # If True don’t start transactions automatically.
        "row_factory": namedtuple_row,
    },
    min_size=4,
    max_size=10,
    open=True,
    # check=ConnectionPool.check_connection,
    name="postgres_pool",
    timeout=5,
)

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s:%(lineno)s - %(funcName)20s(): %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

app = Flask(__name__)
app.config.from_prefixed_env()
log = app.logger


def is_decimal(s):
    """Returns True if string is a parseable float number."""
    try:
        float(s)
        return True
    except ValueError:
        return False


@app.route("/", methods=("GET",))
def clnicas():
    """Mostra todas as clínicas(nome e morada)."""

    with pool.connection() as conn:
        with conn.cursor() as cur:
            clinicas = cur.execute(
                """
                SELECT nome, morada
                FROM clinica
                """,
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    return jsonify(clinicas), 200


@app.route("/c/<clinica>/", methods=("GET",))
def espec_por_clinica(clinica):
    """Lista todas as especialidades oferecidas na <clinica>."""

    with pool.connection() as conn:
        with conn.cursor() as cur:
            especialidades = cur.execute(
                """
                SELECT DISTINCT m.especialidade
                FROM medico m
                JOIN trabalha t ON m.nif = t.nif
                WHERE t.nome = %(nome_da_clinica)s;
                """,
                {"nome_da_clinica": clinica},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    return jsonify(especialidades), 200


@app.route("/c/<clinica>/<especialidade>/", methods=("GET",))
def medico_espec_clinica(clinica, especialidade):
    """Lista todas as especialidades oferecidas na <clinica>."""

    with pool.connection() as conn:
        with conn.cursor() as cur:
            medicos = cur.execute(
                """
                SELECT nome, nif
                FROM medico m
                JOIN trabalha t ON m.nif = t.nif
                WHERE t.nome = %(nome_da_clinica)s
                AND m.especialidade = %(especialidade)s;
                """,
                {"nome_da_clinica": clinica, "especialidade": especialidade},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

            resultado = []

            for medico in medicos:
                medico_nome = medico['nome']
                medico_nif = medico['nif']

                horarios = cur.execute(
                    """
                    SELECT data, hora
                    FROM consulta
                    WHERE nif = %(medico_nif)s
                    AND (data > CURRENT_DATE OR (data = CURRENT_DATE AND hora >= CURRENT_TIME))
                    ORDER BY data, hora
                    LIMIT 3;
                    """,
                    {"medico_nif": medico_nif},
                ).fetchall()
                log.debug(f"Found {cur.rowcount} rows.")    

                info_medico = [medico_nome, [horario["data"], horario["hora"]] for horario in horarios]
                resultado.append(info_medico)


    return jsonify(resultado), 200



@app.route("/a/<clinica>/registar/", methods=("POST",))
def marcar_consulta(clinica, paciente, medico, data, hora):
    """Marca uma consulta na <clinica>"""

    paciente = request.args.get("paciente")
    medico = request.args.get("medico")
    data = request.args.get("data")
    hora = request.args.get("hora")

    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO consulta (ssn, nif, nome, data, hora, codigo_sns)
                VALUES (paciente, medico, clinica, data, hora, NULL);
                WHERE paciente = %(paciente)s
                AND medico = %(medico)s
                AND clinica = %(clinica)s
                AND data = %(data)s
                AND hora = %(hora)s;
                """,
                {"clinica": clinica, "paciente": paciente, "medico": medico, "data": data, "hora": hora},
            )
            # The result of this statement is persisted immediately by the database
            # because the connection is in autocommit mode.
            log.debug(f"Inserted {cur.rowcount} rows.")

            if cur.rowcount == 0:
                return (
                    jsonify({"message": "Clinica not found.", "status": "error"}),
                    404,
                )

    # The connection is returned to the pool at the end of the `connection()` context but,
    # because it is not in a transaction state, no COMMIT is executed.

    return "", 204


@app.route(
    "/a/<clinica>/cancelar/",
    methods=(
        "DELETE",
        "POST",
    ),
)
def cancelar_consulta(clinica, paciente, medico, data, hora):
    """Cancela uma marcação de consulta que ainda não se realizou na <clinica>."""


    paciente = request.args.get("paciente")
    medico = request.args.get("medico")
    data = request.args.get("data")
    hora = request.args.get("hora")

    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                with conn.transaction():
                    # BEGIN is executed, a transaction started
                    cur.execute(
                        """
                        DELETE FROM receita
                        WHERE codigo_sns IN (
                            SELECT codigo_sns FROM consulta
                            WHERE ssn = %(paciente)s
                            AND nif = %(medico)s
                            AND nome = %(clinica)s
                            AND data = %(data)s
                            AND hora = %(hora)s
                            AND (data > CURRENT_DATE OR (data = CURRENT_DATE AND hora > CURRENT_TIME))
                        );
                        """,
                        {"clinica": clinica, "paciente": paciente, "medico": medico, "data": data, "hora": hora},
                    )
                    cur.execute(
                        """
                        DELETE FROM observacao
                        WHERE codigo_sns IN (
                            SELECT codigo_sns FROM consulta
                            WHERE ssn = %(paciente)s
                            AND nif = %(medico)s
                            AND nome = %(clinica)s
                            AND data = %(data)s
                            AND hora = %(hora)s
                            AND (data > CURRENT_DATE OR (data = CURRENT_DATE AND hora > CURRENT_TIME))
                        );
                        """,
                        {"clinica": clinica, "paciente": paciente, "medico": medico, "data": data, "hora": hora},
                    )
                    cur.execute(
                        """
                        DELETE FROM consulta
                        WHERE ssn = %(paciente)s
                        AND nif = %(medico)s
                        AND nome = %(clinica)s
                        AND data = %(data)s
                        AND hora = %(hora)s
                        AND (data > CURRENT_DATE OR (data = CURRENT_DATE AND hora > CURRENT_TIME))
                        """,
                        {"clinica": clinica, "paciente": paciente, "medico": medico, "data": data, "hora": hora},
                    )
                    # These three operations run atomically in the same transaction
            except Exception as e:
                return jsonify({"message": str(e), "status": "error"}), 500
            else:
                # COMMIT is executed at the end of the block.
                # The connection is in idle state again.
                log.debug(f"Deleted {cur.rowcount} rows.")

                if cur.rowcount == 0:
                    return (
                        jsonify({"message": "Clinica not found.", "status": "error"}),
                        404,
                    )

    # The connection is returned to the pool at the end of the `connection()` context

    return "", 204


@app.route("/ping", methods=("GET",))
def ping():
    log.debug("ping!")
    return jsonify({"message": "pong!", "status": "success"})


if __name__ == "__main__":
    app.run()
