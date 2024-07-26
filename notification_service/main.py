import json

from kafka import KafkaConsumer


CONSUMER_GROUP: str = 'notification_consumer_group'
NOTIFICATION_TOPIC: str = 'notification_topic'

operation: bool = False

consumer = KafkaConsumer(
        bootstrap_servers=['localhost:29092', 'localhost:39092'],
        group_id=CONSUMER_GROUP
    )


def consumer_loop():
    try:
        consumer.subscribe(NOTIFICATION_TOPIC)
        while True:
            for msg in consumer:
                decoded_msg = json.loads(msg.value.decode('utf-8'))
                print(decoded_msg)
                # some message processing
    finally:
        consumer.close()


def main():
    consumer_loop()


if __name__ == '__main__':
    main()
