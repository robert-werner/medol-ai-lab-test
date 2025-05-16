from datetime import datetime
import json
import logging
from logging.handlers import RotatingFileHandler
import os


class JsonFormatter(logging.Formatter):
    """Форматтер для вывода логов в JSON формате."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
        }

        # Добавляем дополнительные поля из extra
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id

        # Добавляем информацию об исключении, если оно есть
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info),
            }

        # Добавляем все дополнительные поля из extra
        extra_fields = {
            key: value
            for key, value in record.__dict__.items()
            if key not in logging.LogRecord.__dict__ and key != "exc_info"
        }
        if extra_fields:
            log_data["extra"] = extra_fields

        return json.dumps(log_data, ensure_ascii=False)


class CLogger:
    """Расширенный логгер с поддержкой JSON форматирования и ротации файлов."""

    def __init__(
        self,
        name: str,
        level: int = logging.INFO,
        log_file: str = "app.log",
        log_dir: str = "logs",
        max_bytes: int = 10 * 1024 * 1024,  # 10 MB
        backup_count: int = 5,
        is_to_file: bool = False,
        json_format: bool = True,
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Очищаем существующие обработчики
        self.logger.handlers = []

        # Создаем форматтер
        if json_format:
            formatter = JsonFormatter()
        else:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - "
                "%(module)s:%(lineno)d - %(message)s"
            )

        # Консольный обработчик
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Файловый обработчик с ротацией
        if is_to_file:
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            file_path = os.path.join(log_dir, log_file)
            file_handler = RotatingFileHandler(
                file_path,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8",
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        """Возвращает настроенный логгер."""
        return self.logger


# Создаем экземпляр логгера для всего приложения
logger = CLogger(
    name="app", level=logging.INFO, is_to_file=True, json_format=True
).get_logger()
