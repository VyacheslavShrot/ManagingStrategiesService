from environs import Env
from pika import ConnectionParameters, BasicProperties, PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection

# Read ENV File
env = Env()
env.read_env('.env')


def get_rabbitmq_channel(
) -> tuple[
    BlockingChannel, BlockingConnection
]:
    """
    Connect with Message Broker
    """
    connection: BlockingConnection = BlockingConnection(
        ConnectionParameters(
            'rabbitmq',
            5672,
            '/',
            credentials=PlainCredentials(env("RABBITMQ_DEFAULT_USER"), env("RABBITMQ_DEFAULT_PASS"))
        )
    )

    # Get Channel
    channel: BlockingChannel = connection.channel()

    channel.queue_declare(
        queue='strategy',
        durable=True
    )

    return channel, connection


def publish_message(
        message: str
) -> None:
    """
    Send Message into Channel and Close Connection
    """
    # Get Channel and Connection
    channel, connection = get_rabbitmq_channel()
    channel: BlockingChannel
    connection: BlockingConnection

    # Send Message
    channel.basic_publish(
        exchange='',
        routing_key='strategy',
        body=message.encode('utf-8'),
        properties=BasicProperties(
            delivery_mode=2,
        )
    )

    # Close Connection
    connection.close()
