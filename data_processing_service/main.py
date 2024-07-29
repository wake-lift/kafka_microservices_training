import json

from kafka import KafkaConsumer
from sqlalchemy import insert

from data_processing_service.db import session_factory
from data_processing_service.models import SensorData

DATA_TOPIC: str = 'data_topic'
CONSUMER_GROUP: str = 'sensor_data_consumer_group'

consumer = KafkaConsumer(
        # bootstrap_servers=['localhost:29092', 'localhost:39092'],
        bootstrap_servers=['kafka-1:19092', 'kafka-2:19092'],
        group_id=CONSUMER_GROUP
    )


def consumer_loop():
    try:
        consumer.subscribe(DATA_TOPIC)
        while True:
            for msg in consumer:
                decoded_msg = json.loads(msg.value.decode('utf-8'))
                stmt = (
                    insert(SensorData)
                    .values(
                        sensor_name=decoded_msg['sensor_name'],
                        geotag=decoded_msg['geotag'],
                        timestamp=decoded_msg['timestamp'],
                        temperature=decoded_msg['temperature'],
                        humidity=decoded_msg['humidity']
                    )
                )
                with session_factory() as sf:
                    sf.execute(stmt)
                    sf.commit()
    finally:
        consumer.close()


def main():
    consumer_loop()


if __name__ == '__main__':
    main()
