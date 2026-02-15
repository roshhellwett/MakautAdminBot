import logging
import sys
from core.config import LOG_LEVEL

class ColoredFormatter(logging.Formatter):
    RESET, CYAN, GREEN, YELLOW, RED, BOLD_RED, WHITE, GRAY = "\033[0m", "\033[36m", "\033[32m", "\033[33m", "\033[31m", "\033[1;31m", "\033[37m", "\033[90m"

    def format(self, record):
        COLORS = {logging.DEBUG: self.CYAN, logging.INFO: self.GREEN, logging.WARNING: self.YELLOW, logging.ERROR: self.RED, logging.CRITICAL: self.BOLD_RED}
        color = COLORS.get(record.levelno, self.WHITE)
        log_fmt = f"{self.GRAY}%(asctime)s{self.RESET} │ {color}%(levelname)-8s{self.RESET} │ {self.CYAN}%(name)-12s{self.RESET} │ {color}%(message)s{self.RESET}"
        return logging.Formatter(log_fmt, datefmt="%H:%M:%S").format(record)

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(ColoredFormatter())
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
        logger.propagate = False
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    return logger