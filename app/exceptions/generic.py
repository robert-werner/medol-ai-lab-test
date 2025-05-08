import json
import traceback
from datetime import datetime
from http import HTTPStatus


class GenericException(Exception):
    message = "Generic Game Exception"
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, *args, custom_message=None):
        super().__init__(*args)
        if args:
            self.message = args[0]
        self.custom_message = (
            custom_message if custom_message is not None else self.message
        )

    @property
    def traceback(self):
        return traceback.TracebackException.from_exception(self).format()

    def log_exception(self):
        exception = {
            "type": type(self).__name__,
            "message": self.message,
            "args": self.args[1:],
            "traceback": list(self.traceback),
        }
        timestamp = datetime.now(datetime.UTC).isoformat()
        print(f"EXCEPTION: {timestamp}: {json.dumps(exception, indent=2)}")

    def to_json(self):
        response = {
            "code": self.http_status.value,
            "message": f"{self.http_status.phrase}: {self.custom_message}",
            "category": type(self).__name__,
            "time_utc": datetime.now(datetime.UTC).isoformat(),
        }
        return json.dumps(response)
