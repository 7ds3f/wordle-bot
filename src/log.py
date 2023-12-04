import logging
from pathlib import Path
from typing import Mapping

path = Path(__file__).parent.parent / "logs"
"The path to the log directory."
if not path.is_dir():
    path.mkdir(exist_ok=True)


class AdvancedFormatter(logging.Formatter):
    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style: str = '%',
        validate: bool = True,
        *,
        defaults: Mapping[str, "Any"] = None,
        handle_errors: bool = True
    ):
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)
        self.handle_errors = handle_errors

    def format(self, record):
        if record.levelname == "ERROR":
            record.levelname = "ERRO"
        record.levelname = record.levelname.center(8)
        record.message = record.getMessage()

        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
            record.asctime = record.asctime.replace(" ", " | ", 1)

        s = self.formatMessage(record)
        if self.handle_errors:
            if record.exc_info:
                # Cache the traceback text to avoid converting it multiple times
                # (it's constant anyway)
                if not record.exc_text:
                    record.exc_text = self.formatException(record.exc_info)
            if record.exc_text:
                if s[-1:] != "\n":
                    s = s + "\n"
                s = s + record.exc_text
            if record.stack_info:
                if s[-1:] != "\n":
                    s = s + "\n"
                s = s + self.formatStack(record.stack_info)
        return s


# [loggers]
bottle = logging.getLogger("bottle")
"Logs all warnings, errors, and critical messages in a file."
bottle.setLevel(logging.INFO)
bottle.propagate = 0

game = logging.getLogger("game")
"Logs all game messages in the console."
game.setLevel(logging.INFO)
bottle.propagate = 0


# [formatters]
advanced_format = AdvancedFormatter('[%(asctime)s] [%(levelname)s] %(name)s: %(message)s')
advanced_format.datefmt = '%m/%d/%Y %I:%M:%S %p'

disable_erro_format = AdvancedFormatter('[%(asctime)s] [%(levelname)s] %(name)s: %(message)s', handle_errors=False)
disable_erro_format.datefmt = '%m/%d/%Y %I:%M:%S %p'

# [handlers]
consolehandler = logging.StreamHandler()
consolehandler.setLevel(logging.INFO)
consolehandler.setFormatter(disable_erro_format)

filehandler = logging.FileHandler(path / "bottle.log", "w")
filehandler.setLevel(logging.WARNING)
filehandler.setFormatter(advanced_format)


# Add handlers
bottle.addHandler(filehandler)
bottle.addHandler(consolehandler)
game.addHandler(consolehandler)
