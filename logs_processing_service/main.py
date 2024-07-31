import json
import logging
from io import BytesIO

from fastavro import schemaless_writer
from fastavro.schema import load_schema
from kafka import KafkaConsumer, KafkaProducer
from sqlalchemy import insert

from logs_processing_service.db import session_factory
from logs_processing_service.models import LogData

LOG_TOPIC: str = 'log_topic'
CONSUMER_GROUP: str = 'sensor_logs_consumer_group'
LOG_PRODUCER_NAME: str = 'log_producer'
LOG_PRODUCER_KEY: str = 'log_producer_key'
TELEGRAM_BOT_TOPIC: str = 'telegram_bot_topic'

consumer = KafkaConsumer(
        # bootstrap_servers=['localhost:29092', 'localhost:39092'],
        bootstrap_servers=['kafka-1:19092', 'kafka-2:19092'],
        group_id=CONSUMER_GROUP
    )

producer = KafkaProducer(
    # bootstrap_servers=['localhost:29092', 'localhost:39092'],
    bootstrap_servers=['kafka-1:19092', 'kafka-2:19092'],
    client_id=LOG_PRODUCER_NAME,
    acks=1,
    linger_ms=100,
)

avro_schema: dict = load_schema('critical_log_schema.avsc')


def avro_serialize(schema: dict, data: dict) -> bytes:
    """Сериализатор в формат avro."""
    bytes_writer = BytesIO()
    schemaless_writer(bytes_writer, schema, data)
    return bytes_writer.getvalue()


def consumer_loop():
    try:
        consumer.subscribe(LOG_TOPIC)
        while True:
            for msg in consumer:
                decoded_msg = json.loads(msg.value.decode('utf-8'))
                logging.info(f'logs processing: {decoded_msg}')
                stmt = (
                    insert(LogData)
                    .values(
                        sensor_name=decoded_msg['sensor_name'],
                        timestamp=decoded_msg['timestamp'],
                        level=decoded_msg['level'],
                        log_message=decoded_msg['log_message']
                    )
                )
                with session_factory() as sf:
                    sf.execute(stmt)
                    sf.commit()
                if decoded_msg['level'] == 'CRITICAL':
                    bot_msg = avro_serialize(avro_schema, decoded_msg)
                    logging.warning(f'Получен лог CRITICAL: {decoded_msg}')
                    producer.send(
                        TELEGRAM_BOT_TOPIC,
                        value=bot_msg,
                        key=LOG_PRODUCER_KEY.encode('utf-8')
                    )
                    producer.flush()
    finally:
        consumer.close()


def main():
    consumer_loop()


if __name__ == '__main__':
    main()
