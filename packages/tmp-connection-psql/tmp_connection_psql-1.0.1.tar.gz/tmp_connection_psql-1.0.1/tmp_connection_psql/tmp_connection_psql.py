"""Main file to create a temporary connection to a psql database."""

# Standard imports
import os.path
import platform
import subprocess
from contextlib import contextmanager
from tempfile import gettempdir, mkdtemp
from typing import Generator

# Third party imports
import psycopg
from port_for import get_port
from psycopg import Connection, Error
from pytest_postgresql.executor import PostgreSQLExecutor
from pytest_postgresql.janitor import DatabaseJanitor


class PSQLConnectionError(Exception):
    """Error raised if we can't connect to a database."""


class NonePortError(Exception):
    """Error raised if the port get by `get_port()` is None."""


def connect(
    user: str,
    password: str,
    host: str,
    port: str,
    database: str,
) -> Connection:
    """
    Connect to a database.

    Returns :
        A connection to a database if all is working.

    Raises :
        ConnectionError : If we got an error while connecting to the data base.
    """
    try:
        connection = psycopg.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            dbname=database,
        )
        return connection
    except (Exception, Error) as err:
        raise PSQLConnectionError(f"Error while connecting to posgeSQL {err}") from err


@contextmanager
def tmp_connection(
    db_password: str,
    sql_cmd_path: str | None,
) -> Generator[Connection, None, None]:
    """
    Get a temporary connection on a postgresql database.

    Args:
        - db_password: dummy password to create a database
        - sql_cmd_path: path of the sql file with command to load in the tmp database.

    Returns:
        Connection on the temporary database.
    """
    pg_dbname = "db_tmp_empty"
    pg_load = [sql_cmd_path]
    postgresql_ctl = "/usr/lib/postgresql/13/bin/pg_ctl"

    if not os.path.exists(postgresql_ctl):
        pg_bindir = subprocess.check_output(  # nosec B607 B603
            ["pg_config", "--bindir"],
            universal_newlines=True,
        ).strip()
        postgresql_ctl = os.path.join(pg_bindir, "pg_ctl")

    tmpdir = mkdtemp()

    pg_port = get_port(None)
    if not pg_port:
        raise NonePortError("Port get by `get_port()` is None")
    datadir = f"{tmpdir}data-{pg_port}"
    logfile_path = f"{tmpdir}postgresql.{pg_port}.log"

    if platform.system() == "FreeBSD":
        with (datadir / "pg_hba.conf").open(mode="a") as conf_file:  # type: ignore
            conf_file.write("host all all 0.0.0.0/0 trust\n")

    psql_executor = PostgreSQLExecutor(
        executable=postgresql_ctl,
        host="127.0.0.1",
        port=pg_port,
        password=db_password,
        dbname=pg_dbname,
        datadir=str(datadir),
        unixsocketdir=gettempdir(),
        logfile=str(logfile_path),
        startparams="-w",
    )

    # start server
    with psql_executor:
        psql_executor.wait_for_postgres()
        with DatabaseJanitor(
            user=psql_executor.user,
            host=psql_executor.host,
            port=psql_executor.port,
            dbname=psql_executor.dbname,
            version=psql_executor.version,
            password=psql_executor.password,
        ) as janitor:
            if pg_load:
                for load_element in pg_load:
                    janitor.load(load_element)  # type: ignore

            conn = connect(
                database=psql_executor.dbname,
                user=psql_executor.user,
                password=db_password,
                host=psql_executor.host,
                port=str(psql_executor.port),
            )
            yield conn
