import json
from random import choice, choices, randint, uniform
from string import ascii_letters
import time

from fastapi import BackgroundTasks, FastAPI
from kafka import KafkaProducer

SENSOR_NAME: str = 'sensor_02'
SENSOR_KEY: str = 'sensor_02_key'
LOG_KEY: str = 'log_02_key'
DATA_TOPIC: str = 'data_topic'
LOG_TOPIC: str = 'log_topic'

operation_flag: bool = True
imitator_in_operation: bool = False

kafka_producer = KafkaProducer(
    bootstrap_servers=['localhost:29092', 'localhost:39092'],
    client_id=SENSOR_NAME,
    acks=1,
    linger_ms=100,
)

app = FastAPI(
    title='sensor_service_02',
    description='Микросервис, имитирующий работу сенсора №2',
    redoc_url=None,
)


@app.get('/start', summary='Запустить сервис')
async def start_operation(background_tasks: BackgroundTasks):
    """Начать генерацию данных сенсора."""
    global operation_flag, imitator_in_operation
    if not imitator_in_operation:
        operation_flag = True
        background_tasks.add_task(imitate_operation)
        return {'message': 'starting service'}
    return {'message': 'service already in operation'}


@app.get('/stop', summary='Остановить сервис')
async def stop_operation():
    """Закончить генерацию данных сенсора."""
    global operation_flag, imitator_in_operation
    if imitator_in_operation:
        operation_flag = False
        return {'message': 'stopping service'}
    return {'message': 'service already stopped'}


def generate_sensor_data():
    return {
        'sensor_name': SENSOR_NAME,
        'geotag': """0°11'39.4"N 51°05'43.2"W""",
        'timestamp': int(time.time()),
        'temperature': round(uniform(10.0, 60.0), 3),
        'humidity': round(uniform(0.0, 100.0), 3),
    }


def generate_log_data():
    logging_levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL',)
    return {
        'sensor_name': SENSOR_NAME,
        'timestamp': int(time.time()),
        'level': choice(logging_levels),
        'log_message': ''.join(choices(ascii_letters, k=randint(10, 50))),
    }


def send_message(topic: str, data: str, key: str):
    kafka_producer.send(
        topic,
        value=data.encode('utf-8'),
        key=key.encode('utf-8')
    )
    kafka_producer.flush()


def imitate_operation():
    global operation_flag, imitator_in_operation
    imitator_in_operation = True
    log_dice = 0
    while operation_flag:
        print(log_dice)
        sensor_data = generate_sensor_data()
        serialized_sensor_data = json.dumps(sensor_data)
        send_message(DATA_TOPIC, serialized_sensor_data, SENSOR_KEY)
        print(f'Sent sensor data: {serialized_sensor_data}')
        time.sleep(5)
        if log_dice == 5:
            log_data = generate_log_data()
            serialized_log_data = json.dumps(log_data)
            send_message(LOG_TOPIC, serialized_log_data, LOG_KEY)
            print(f'Sent log data: {serialized_log_data}')
        # log_dice = randint(0, 20)
        log_dice = randint(4, 6)
    imitator_in_operation = False
    kafka_producer.flush()
