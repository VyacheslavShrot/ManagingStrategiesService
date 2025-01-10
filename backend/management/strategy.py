from backend.database import Queries
from backend.management.models import Strategy


class StrategyService(
    Queries
):
    _buy_sell_conditions_keys: list = [
        "indicator", "threshold"
    ]

    def validate_buy_sell_conditions(
            self,
            buy_conditions: dict = None,
            sell_conditions: dict = None,
            only_buy: bool = False,
            only_sell: bool = False
    ) -> tuple | list:
        """
        Check If Not Exist Another Data
        """
        if only_buy:
            if buy_conditions:
                extra_buy_data: list = [
                    key for key in buy_conditions.keys() if key not in self._buy_sell_conditions_keys
                ]

                return extra_buy_data

        if only_sell:
            if sell_conditions:
                extra_sell_data: list = [
                    key for key in sell_conditions.keys() if key not in self._buy_sell_conditions_keys
                ]
                return extra_sell_data

        if buy_conditions and sell_conditions:
            extra_buy_data: list = [
                key for key in buy_conditions.keys() if key not in self._buy_sell_conditions_keys
            ]
            extra_sell_data: list = [
                key for key in sell_conditions.keys() if key not in self._buy_sell_conditions_keys
            ]
            return extra_buy_data, extra_sell_data

    def create_strategy(
            self,
            user_id: int,
            name: str,
            description: str,
            asset_type: str,
            buy_conditions: dict,
            sell_conditions: dict
    ) -> Strategy:
        """
        Create New Strategy and Save into DB
        """
        strategy: Strategy = Strategy(
            user_id=user_id,
            name=name,
            description=description,
            asset_type=asset_type,
            buy_conditions=buy_conditions,
            sell_conditions=sell_conditions
        )

        # Create and Save Strategy
        self.add_and_commit(
            models_object=strategy
        )

        return strategy

    @staticmethod
    def get_strategy_by_id(
            strategy_id: int
    ) -> Strategy | None:
        """
        Get Strategy by ID
        """
        strategy: Strategy = Strategy.query.get(
            strategy_id
        )

        return strategy if strategy else None

    @staticmethod
    def get_user_strategies(
            user_id: int
    ) -> list[Strategy] | None:
        """
        Get ALL User Strategies by User ID
        """
        strategies: list = Strategy.query.filter_by(user_id=user_id).all()

        return strategies if strategies else None

    def delete_strategy(
            self,
            strategy: Strategy
    ) -> None:
        """
        Delete Strategy
        """
        self.delete_and_commit(
            models_object=strategy
        )
