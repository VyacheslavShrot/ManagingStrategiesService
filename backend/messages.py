from config.broker import publish_message


def publish_create_strategy_message(
        user_id: int,
        strategy_name: str
) -> None:
    """
    Send Message into Channel
   """
    message: str = f"User {user_id} created strategy {strategy_name}"

    publish_message(message)


def publish_update_strategy_message(
        user_id: int,
        strategy_name: str
) -> None:
    """
    Send Message into Channel
    """
    message: str = f"User {user_id} updated strategy {strategy_name}"

    publish_message(message)
