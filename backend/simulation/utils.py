def check_input_historical_data(
        data: dict
) -> tuple | None:
    """
    Validate Input Historical Data from Simulate Strategy
    """

    # Get Required Data
    date: str = data.get("date", None)
    open: float = data.get("open", None)
    close: float = data.get("close", None)
    high: float = data.get("high", None)
    low: float = data.get("low", None)
    volume: int = data.get("volume", None)

    if not all(
            [date, open, close, high, low, volume]
    ):
        return None

    if not isinstance(open, float):
        return None

    if not isinstance(close, float):
        return None

    if not isinstance(high, float):
        return None

    if not isinstance(low, float):
        return None

    if not isinstance(volume, int):
        return None

    if not isinstance(date, str):
        return None

    return (
        date, open, close, high, low, volume
    )
