import logging
from logging import handlers

from sever.settings import LOG_DIR


class CommonLog:
    def __init__(self, when='D', backupCount=30, console=True):
        self.check_log_folder()
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - %(module)s %(filename)s[%(lineno)d] : %(message)s',
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        debug_handler = handlers.TimedRotatingFileHandler(
            filename=f'{LOG_DIR / "debug" / "debug.log"}',
            when=when,
            backupCount=backupCount
        )
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(formatter)

        info_handler = handlers.TimedRotatingFileHandler(
            filename=f'{LOG_DIR / "info" / "info.log"}',
            when=when,
            backupCount=backupCount
        )
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(formatter)

        warning_handler = handlers.TimedRotatingFileHandler(
            filename=f'{LOG_DIR / "warning" / "warning.log"}',
            when=when,
            backupCount=backupCount
        )
        warning_handler.setLevel(logging.WARNING)
        warning_handler.setFormatter(formatter)

        error_handler = handlers.TimedRotatingFileHandler(
            filename=f'{LOG_DIR / "error" / "error.log"}',
            when=when,
            backupCount=backupCount
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)

        fatal_handler = handlers.TimedRotatingFileHandler(
            filename=f'{LOG_DIR / "fatal" / "fatal.log"}',
            when=when,
            backupCount=backupCount
        )
        fatal_handler.setLevel(logging.FATAL)
        fatal_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        self.log = logging.getLogger('')
        self.log.setLevel(logging.INFO)
        self.log.addHandler(debug_handler)
        self.log.addHandler(info_handler)
        self.log.addHandler(warning_handler)
        self.log.addHandler(error_handler)
        self.log.addHandler(fatal_handler)
        if console:
            self.log.addHandler(console_handler)

    def check_log_folder(self):
        dir = LOG_DIR
        if not dir.exists():
            dir.mkdir(parents=True)
            for level in ["debug", "info", "warning", "error", "fatal"]:
                (dir / level).mkdir()
        else:
            for level in ["debug", "info", "warning", "error", "fatal"]:
                if not (dir / level).exists():
                    (dir / level).mkdir()


log = CommonLog("D", 30, False).log