from kafka import KafkaConsumer

DATA_TOPIC: str = 'data_topic'
CONSUMER_GROUP: str = 'sensor_data_consumer_group'

consumer = KafkaConsumer(
        bootstrap_servers=['localhost:29092', 'localhost:39092'],
        group_id=CONSUMER_GROUP
    )


def consumer_loop():
    try:
        consumer.subscribe(DATA_TOPIC)
        while True:
            for msg in consumer:
                print(msg.value.decode('utf-8'))
    finally:
        consumer.close()


def main():
    consumer_loop()


if __name__ == '__main__':
    main()
