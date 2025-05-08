from typing import Any

from decouple import config, UndefinedValueError


class Settings(object):  # noqa: WPS230
    """Class with server settings."""

    def __init__(self) -> None:
        """Create class with server settings."""
        self.db_user = self.get_setting("DB_USER", "medol")
        self.db_password = self.get_setting("DB_PASSWORD", "medol")
        self.db_name = self.get_setting("DB_NAME", "medol")
        self.db_host = self.get_setting("DB_HOST", "localhost")
        self.db_port = self.get_setting("DB_PORT", "6432")

    def get_setting(self, name: str, default: Any) -> Any:
        """Get setting.

        :param name: Setting name
        :param default: Default value
        :return: Setting value
        """
        setting = None
        try:
            setting = config(name)
        except UndefinedValueError:
            setting = default

        return setting


settings = Settings()