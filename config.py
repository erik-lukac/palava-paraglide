from dataclasses import dataclass
from typing import Final

@dataclass(frozen=True)
class Config:
    SCHEDULE_TIMES: Final[tuple[str, ...]] = (":02", ":17", ":32", ":47")
    DB_NAME: Final[str] = "database.db"
    LOG_FORMAT: Final[str] = "%(asctime)s - %(levelname)s - %(message)s" 