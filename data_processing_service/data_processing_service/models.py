from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from data_processing_service.db import Base


class SensorData(Base):
    """Таблица для сохранения данных с датчиков."""
    __tablename__ = 'sensor_data'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sensor_name: Mapped[str] = mapped_column(String(256))
    geotag: Mapped[str] = mapped_column(String(64))
    timestamp: Mapped[int]
    temperature: Mapped[float]
    humidity: Mapped[float]
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __str__(self):
        return f'Запись {self.id}. Датчик: {self.sensor_name}'

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}, id = {self.id}>'
