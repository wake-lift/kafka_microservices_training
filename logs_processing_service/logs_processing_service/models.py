from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from logs_processing_service.db import Base


class LogData(Base):
    """Таблица для сохранения логов датчиков."""
    __tablename__ = 'log_data'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sensor_name: Mapped[str] = mapped_column(String(256))
    timestamp: Mapped[int]
    level: Mapped[str] = mapped_column(String(32))
    log_message: Mapped[str] = mapped_column(String(512))
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __str__(self):
        return f'Запись {self.id}. Уровень: {self.level}'

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}, id = {self.id}>'
