"""Paquete ``Model`` (equivalente al paquete Java ``Model``).

    - ``db_data.DbData``          -> datos de conexión (como ``DbData.java``)
    - ``db_connection``           -> apertura de conexión / cursores
    - ``model_dog.modelDog``      -> CRUD de perros (como ``modelDog.java``)
    - ``model_cat.modelCat``      -> CRUD de gatos (como ``modelCat.java``)
"""

from .db_connection import (DatabaseConnectionError, DriverNotInstalledError,
                            connection, create_cursor, cursor, get_connection,
                            get_primary_key_column, test_connection)
from .db_data import DbData
from .model_cat import modelCat
from .model_dog import modelDog

__all__ = [
    "DbData",
    "DatabaseConnectionError",
    "DriverNotInstalledError",
    "connection",
    "create_cursor",
    "cursor",
    "get_connection",
    "get_primary_key_column",
    "modelCat",
    "modelDog",
    "test_connection",
]
