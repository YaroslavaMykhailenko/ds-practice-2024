import json
import logging

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_message = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage()
        }

        if hasattr(record, 'exc_info') and record.exc_info:
            log_message["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_message)



def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setFormatter(JsonFormatter())

    logger.addHandler(ch)
    return logger
