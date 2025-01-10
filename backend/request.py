from backend.management.models import Strategy
from backend.user.models import User


class APIRequest:

    def get_data(
            self,
            data: dict,
            params: list
    ) -> tuple:
        """
        Get Required Data from Request and Output as Tuple
        """
        response: tuple = tuple(
            data.get(param, None) for param in params
        )
        return response

    @staticmethod
    def user_response(
            user: User,
            token: str
    ) -> dict:
        """
        Format User Response
        """

        return {
            "success": True,
            "user": {
                "id": user.id,
                "username": user.username
            },
            "token": token
        }

    @staticmethod
    def strategy_response(
            user: User,
            strategy: Strategy
    ) -> dict:
        """
        Format Strategy Response
        """

        return {
            "success": True,
            "strategy": {
                "user": {
                    "id": user.id,
                    "username": user.username
                },
                "id": strategy.id,
                "name": strategy.name,
                "description": strategy.description,
                "asset_type": strategy.asset_type,
                "buy_conditions": strategy.buy_conditions,
                "sell_condition": strategy.sell_conditions,
                "status": strategy.status
            }
        }
