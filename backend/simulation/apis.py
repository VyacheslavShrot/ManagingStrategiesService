from flask import Blueprint, jsonify, request, g
from flask_jwt_extended import jwt_required

from backend.management.models import Strategy
from backend.simulation.utils import check_input_historical_data
from backend.user.models import User
from config.logger import logger

simulate_bp: Blueprint = Blueprint('simulate', __name__)


class SimulateApis:

    @staticmethod
    @simulate_bp.route(
        "/strategy/<int:strategy_id>/simulate",
        methods=[
            "POST"
        ]
    )
    @jwt_required()
    def create_strategy(
            strategy_id: int
    ) -> jsonify:
        """
        Simulate Strategy
        User Authenticate is Required
        """
        logger.info(f"----\nStart Simulate Strategy API")

        try:
            # Get User
            user: User | None = g.get("current_user", None)
            if not user:
                return jsonify(
                    {
                        "error": "Unauthorized"
                    }
                ), 401

            # Get Strategy
            strategy: Strategy = Strategy.query.get(strategy_id)
            if not strategy:
                return jsonify(
                    {
                        "error": "No Such Strategy"
                    }
                ), 404

            if strategy.user_id != user.id:
                return jsonify(
                    {
                        "error": "Such Strategy is NOT Your Strategy"
                    }
                ), 404

            # Get Data
            data: list[dict] = request.get_json()
            if not isinstance(data, list):
                return jsonify(
                    {
                        "error": "Data Can be ONLY List with Dict Inside"
                    }
                ), 400

            # Example Trade Data
            # TODO -> Integrate with Real Project Logic
            total_trades: int = 0
            profit_loss: float = 0.0
            successful_trades: int = 0
            balances: list = []
            current_balance: int = 100000
            buy_price = None

            # Iterate through Input Date
            for record in data:
                record: dict

                # Validate and Get Data
                (
                    date, open, close_price, high_price, low_price, volume
                ) = check_input_historical_data(record)

                # Extract Conditions from Strategy
                buy_indicator: float = close_price
                sell_indicator: float = high_price

                # Check Buy Condition
                if buy_indicator and buy_indicator < strategy.buy_conditions.get("threshold") and buy_price is None:
                    buy_price: float = close_price
                    total_trades += 1

                # Check Sell Condition
                elif sell_indicator and sell_indicator > strategy.sell_conditions.get("threshold") and buy_price:
                    sell_price: float = close_price

                    profit_loss += (sell_price - buy_price)
                    successful_trades += 1 if sell_price > buy_price else 0
                    total_trades += 1
                    buy_price = None

                # Track Balance Changes
                current_balance += profit_loss
                balances.append(current_balance)

            # Calculate Win Rate
            win_rate: float | int = (successful_trades / total_trades * 100) if total_trades > 0 else 0

            # Calculate Max Drawdown
            max_drawdown: int = 0
            peak: int = balances[0] if balances else 0

            for balance in balances:
                if balance > peak:
                    peak: int = balance

                drawdown: int = peak - balance

                max_drawdown: int = max(max_drawdown, drawdown)

            logger.info(f"----\nSuccessful Simulate Strategy")
            return jsonify(
                {
                    "success": True,
                    "strategy_id": strategy.id,
                    "total_trades": total_trades,
                    "profit_loss": profit_loss,
                    "win_rate": win_rate,
                    "max_drawdown": max_drawdown
                }
            ), 200
        except Exception as e:
            logger.error(f"An Unexpected Error occurred while Simulate Strategy | {e}")
