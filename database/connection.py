import logging
from urllib.parse import quote

from psycopg import AsyncConnection
from psycopg_pool import AsyncConnectionPool

logger = logging.getLogger(__name__)


# Функция, возвращающая безопасную строку `conninfo` для подключения к PostgreSQL
def build_pg_conninfo(
    db_name: str,
    host: str,
    port: int,
    user: str,
    password: str,
) -> str:
    conninfo = (
        f"postgresql://{quote(user, safe='')}:{quote(password, safe='')}"
        f"@{host}:{port}/{db_name}"
    )
    logger.debug(
        f"Building PostgreSQL connection string (password omitted): "
        f"postgresql://{quote(user, safe='')}@{host}:{port}/{db_name}"
    )
    return conninfo


# Функция, логирующая версию СУБД, к которой происходит подключение
async def log_db_version(connection: AsyncConnection) -> None:
    try:
        async with connection.cursor() as cursor:
            await cursor.execute("SELECT version();")
            db_version = await cursor.fetchone()
            db_version_str = db_version[0] if db_version else "unknown"
            logger.info(f"Connected to PostgreSQL version: {db_version_str}")
    except Exception as e:
        logger.warning("Failed to fetch DB version: %s", e)


# Функция, возвращающая открытое соединение с СУБД PostgreSQL
async def get_pg_connection(
    db_name: str,
    host: str,
    port: int,
    user: str,
    password: str,
) -> AsyncConnection:
    conninfo = build_pg_conninfo(db_name, host, port, user, password)
    connection: AsyncConnection | None = None

    try:
        connection = await AsyncConnection.connect(conninfo=conninfo)
        await log_db_version(connection)
        return connection
    except Exception as e:
        logger.exception("Failed to connect to PostgreSQL: %s", e)
        if connection:
            await connection.close()
        raise


# Функция, возвращающая пул соединений с СУБД PostgreSQL
async def get_pg_pool(
    db_name: str,
    host: str,
    port: int,
    user: str,
    password: str,
    min_size: int = 1,
    max_size: int = 3,
    timeout: float = 10.0,
) -> AsyncConnectionPool:
    conninfo = build_pg_conninfo(db_name, host, port, user, password)
    db_pool: AsyncConnectionPool | None = None

    try:
        db_pool = AsyncConnectionPool(
            conninfo=conninfo,
            min_size=min_size,
            max_size=max_size,
            timeout=timeout,
            open=False,
        )

        await db_pool.open()

        async with db_pool.connection() as connection:
            await log_db_version(connection)

        return db_pool
    except Exception as e:
        logger.exception("Failed to initialize PostgreSQL pool: %s", e)
        if db_pool and not db_pool.closed:
            await db_pool.close()
        raise
