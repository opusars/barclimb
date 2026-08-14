import json
import logging
import os
from datetime import UTC, datetime


class StructuredFormatter(logging.Formatter):
    """Small JSON formatter for process-identifiable logs without record payload dumping."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "environment": os.environ.get("APP_ENV", "local"),
            "process": os.environ.get("DYNO", "local"),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, separators=(",", ":"))
