from re import search
from typing import Any
from typing import Optional

from sqlalchemy import Table
from sqlalchemy import create_engine as _create_engine
from sqlalchemy.engine import URL
from sqlalchemy.engine import Engine
from sqlalchemy.exc import DatabaseError
from sqlalchemy.exc import OperationalError
from sqlalchemy.pool import NullPool
from sqlalchemy.pool import Pool


def create_engine(
    drivername: str,
    /,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[int] = None,
    database: Optional[str] = None,
    poolclass: Optional[type[Pool]] = NullPool,
) -> Engine:
    """Create a SQLAlchemy engine."""

    url = URL.create(
        drivername,
        username=username,
        password=password,
        host=host,
        port=port,
        database=database,
    )
    return _create_engine(url, future=True, poolclass=poolclass)


def ensure_table_created(table_or_model: Any, engine: Engine, /) -> None:
    """Ensure a table is created."""

    table = get_table(table_or_model)
    try:
        with engine.begin() as conn:
            table.create(conn)
    # note that OperationalError < DatabaseError
    except OperationalError as error:
        # sqlite
        (msg,) = error.args
        if not search("table .* already exists", msg):  # pragma: no cover
            raise
    except DatabaseError as error:  # pragma: no cover
        # oracle
        (msg,) = error.args
        if not search(
            "ORA-00955: name is already used by an existing object", msg
        ):
            raise


def ensure_table_dropped(table_or_model: Any, engine: Engine, /) -> None:
    """Ensure a table is dropped."""

    table = get_table(table_or_model)
    try:
        with engine.begin() as conn:
            table.drop(conn)
    # note that OperationalError < DatabaseError
    except OperationalError as error:
        # sqlite
        (msg,) = error.args
        if not search("no such table", msg):  # pragma: no cover
            raise
    except DatabaseError as error:  # pragma: no cover
        # oracle
        (msg,) = error.args
        if not search("ORA-00942: table or view does not exist", msg):
            raise


def get_column_names(table_or_model: Any, /) -> list[str]:
    """Get the column names from a table or model."""

    return [col.name for col in get_columns(table_or_model)]


def get_columns(table_or_model: Any, /) -> list[Any]:
    """Get the columns from a table or model."""

    return list(get_table(table_or_model).columns)


def get_table(table_or_model: Any, /) -> Table:
    """Get the table from a ORM model."""

    if isinstance(table_or_model, Table):
        return table_or_model
    else:
        return table_or_model.__table__
