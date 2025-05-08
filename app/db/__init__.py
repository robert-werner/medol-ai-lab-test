from app.settings import Settings

DB_USER = Settings().db_user
DB_PASSWORD = Settings().db_password
DB_NAME = Settings().db_name
DB_HOST = Settings().db_host
DB_PORT = Settings().db_port


def get_db_string(
    host: str,
    port: str,
    database: str,
    user: str,
    password: str,
):
    """Get database connection string.

    :param host: Database address
    :param port: Database port
    :param database: Database name
    :param user: Username
    :param password: User password
    :return: Connection string
    """
    credentials = f"{user}:{password}"
    address = f"{host}:{port}/{database}"
    return "".join(["postgresql+asyncpg://", credentials, "@", address])