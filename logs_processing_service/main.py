import json

from kafka import KafkaConsumer, KafkaProducer
from sqlalchemy import insert

from logs_processing_service.models import LogData
from logs_processing_service.db import session_factory

LOG_TOPIC: str = 'log_topic'
CONSUMER_GROUP: str = 'sensor_logs_consumer_group'
LOG_PRODUCER_NAME: str = 'log_producer'
LOG_PRODUCER_KEY: str = 'log_producer_key'
NOTIFICATION_TOPIC: str = 'notification_topic'

consumer = KafkaConsumer(
        bootstrap_servers=['localhost:29092', 'localhost:39092'],
        group_id=CONSUMER_GROUP
    )

producer = KafkaProducer(
    bootstrap_servers=['localhost:29092', 'localhost:39092'],
    client_id=LOG_PRODUCER_NAME,
    acks=1,
    linger_ms=100,
)


def consumer_loop():
    try:
        consumer.subscribe(LOG_TOPIC)
        while True:
            for msg in consumer:
                decoded_msg = json.loads(msg.value.decode('utf-8'))
                print(decoded_msg)
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
                    bot_msg = json.dumps(decoded_msg)
                    producer.send(
                        NOTIFICATION_TOPIC,
                        value=bot_msg.encode('utf-8'),
                        key=LOG_PRODUCER_KEY.encode('utf-8')
                    )
                    producer.flush()
    finally:
        consumer.close()


def main():
    consumer_loop()


if __name__ == '__main__':
    main()
