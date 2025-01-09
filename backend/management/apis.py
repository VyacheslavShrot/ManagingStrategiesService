from flask import Blueprint, jsonify, request, g
from flask_jwt_extended import jwt_required

from backend.management.models import Strategy
from backend.user.models import User
from config.database import db
from config.logger import logger

strategy_bp: Blueprint = Blueprint('strategy', __name__)


class StrategyApis:

    @staticmethod
    @strategy_bp.route(
        "/strategy/create",
        methods=[
            "POST"
        ]
    )
    @jwt_required()
    def create_strategy(
    ) -> jsonify:
        """
        Create Strategy by User
        User Authenticate is Required
        """
        logger.info(f"----\nStart Create Strategy API")

        try:
            # Get User
            user: User | None = g.get("current_user", None)
            if not user:
                return jsonify(
                    {
                        "error": "Unauthorized"
                    }
                ), 401

            # Get Data
            data: dict = request.get_json()

            name: str = data.get("name", None)
            description: str = data.get("description", None)
            asset_type: str = data.get("asset_type", None)
            buy_conditions: dict = data.get("buy_conditions", None)
            sell_conditions: dict = data.get("sell_conditions", None)

            if not all(
                    [name, description, asset_type, buy_conditions, sell_conditions]
            ):
                return jsonify(
                    {
                        "error": "'name', 'description', 'asset_type', 'buy_conditions' and 'sell_conditions' are Required Params"
                    }
                ), 400

            if not isinstance(buy_conditions, dict) or not isinstance(sell_conditions, dict):
                return jsonify(
                    {
                        "error": "'buy_conditions' and 'sell_conditions' Can be ONLY Dict"
                    }
                ), 400

            indicator_buy: str = buy_conditions.get("indicator", None)
            indicator_sell: str = sell_conditions.get("indicator", None)
            threshold_buy: float = buy_conditions.get("threshold", None)
            threshold_sell: float = sell_conditions.get("threshold", None)

            if not all(
                    [indicator_buy, indicator_sell, threshold_buy, threshold_sell]
            ):
                return jsonify(
                    {
                        "error": "'indicator' and 'threshold' are Required Params in 'buy_conditions' and 'sell_conditions'"
                    }
                ), 400

            # Check If Not Exist Another Data
            extra_buy_data: list = [
                key for key in buy_conditions.keys() if key not in ["indicator", "threshold"]
            ]
            extra_sell_data: list = [
                key for key in sell_conditions.keys() if key not in ["indicator", "threshold"]
            ]

            if extra_buy_data:
                return jsonify(
                    {
                        "error": "'buy_conditions' Can Accept ONLY 'indicator' and 'threshold' Params"
                    }
                ), 400
            if extra_sell_data:
                return jsonify(
                    {
                        "error": "'sell_conditions' Can Accept ONLY 'indicator' and 'threshold' Params"
                    }
                ), 400

            # Create Strategy Object
            strategy: Strategy = Strategy(
                user_id=user.id,
                name=name,
                description=description,
                asset_type=asset_type,
                buy_conditions=buy_conditions,
                sell_conditions=sell_conditions
            )

            # Save Strategy
            db.session.add(strategy)
            db.session.commit()

            logger.info(f"----\nSuccessful Create Strategy")
            return jsonify(
                {
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
                        "buy_conditions": {
                            "indicator": indicator_buy,
                            "threshold": threshold_buy
                        },
                        "sell_condition": {
                            "indicator": indicator_sell,
                            "threshold": threshold_sell
                        },
                        "status": strategy.status
                    }
                }
            ), 201
        except Exception as e:
            logger.error(f"An Unexpected Error occurred while Create Strategy | {e}")

    @staticmethod
    @strategy_bp.route(
        "/strategy/<int:strategy_id>",
        methods=[
            "GET"
        ]
    )
    @jwt_required()
    def get_strategy(
            strategy_id: int
    ) -> jsonify:
        """
        Get Strategy by Strategy Id
        User Authenticate is Required
        """
        logger.info(f"----\nStart Get Strategy API")

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

            # Get Strategy Data
            buy_conditions: dict = strategy.buy_conditions
            sell_conditions: dict = strategy.sell_conditions

            indicator_buy: str = buy_conditions.get("indicator")
            threshold_buy: float = buy_conditions.get("threshold")
            indicator_sell: str = sell_conditions.get("indicator")
            threshold_sell: float = sell_conditions.get("threshold")

            logger.info(f"----\nSuccessful Get Strategy")
            return jsonify(
                {
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
                        "buy_conditions": {
                            "indicator": indicator_buy,
                            "threshold": threshold_buy
                        },
                        "sell_condition": {
                            "indicator": indicator_sell,
                            "threshold": threshold_sell
                        },
                        "status": strategy.status
                    }
                }
            ), 200
        except Exception as e:
            logger.error(f"An Unexpected Error occurred while Get Strategy | {e}")

    @staticmethod
    @strategy_bp.route(
        "/strategy/update/<int:strategy_id>",
        methods=[
            "PUT"
        ]
    )
    @jwt_required()
    def update_strategy(
            strategy_id: int
    ) -> jsonify:
        """
        Update Strategy by Strategy Id
        User Authenticate is Required
        """
        logger.info(f"----\nStart Update Strategy API")

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
            data: dict = request.get_json()

            name: str = data.get("name", None)
            description: str = data.get("description", None)
            asset_type: str = data.get("asset_type", None)
            status: str = data.get("status", None)
            buy_conditions: dict = data.get("buy_conditions", None)
            sell_conditions: dict = data.get("sell_conditions", None)

            if not any(
                    [name, description, asset_type, status, buy_conditions, sell_conditions]
            ):
                return jsonify(
                    {
                        "error": "At Least ONE of the Fields 'name', 'description', 'asset_type', 'status', 'buy_conditions' or 'sell_conditions' is Required"
                    }
                ), 400

            # Update Strategy with Changes
            if name:
                strategy.name = name
            if description:
                strategy.description = description
            if asset_type:
                strategy.asset_type = asset_type
            if status:
                strategy.status = status

            if buy_conditions:
                if not isinstance(buy_conditions, dict):
                    return jsonify(
                        {
                            "error": "'buy_conditions' Can be ONLY Dict"
                        }
                    ), 400

                # Check If Not Exist Another Data
                extra_buy_data: list = [
                    key for key in buy_conditions.keys() if key not in ["indicator", "threshold"]
                ]
                if extra_buy_data:
                    return jsonify(
                        {
                            "error": "'buy_conditions' Can Accept ONLY 'indicator' and 'threshold' Params"
                        }
                    ), 400

                indicator_buy: str = buy_conditions.get("indicator", None)
                threshold_buy: float = buy_conditions.get("threshold", None)

                if not indicator_buy and not threshold_buy:
                    return jsonify(
                        {
                            "error": "'indicator' and 'threshold' are Required Params"
                        }
                    ), 400

                strategy.buy_conditions = buy_conditions

            if sell_conditions:
                if not isinstance(sell_conditions, dict):
                    return jsonify(
                        {
                            "error": "'sell_conditions' Can be ONLY Dict"
                        }
                    ), 400

                # Check If Not Exist Another Data
                extra_sell_data: list = [
                    key for key in sell_conditions.keys() if key not in ["indicator", "threshold"]
                ]
                if extra_sell_data:
                    return jsonify(
                        {
                            "error": "'sell_conditions' Can Accept ONLY 'indicator' and 'threshold' Params"
                        }
                    ), 400

                indicator_sell: str = sell_conditions.get("indicator", None)
                threshold_sell: float = sell_conditions.get("threshold", None)

                if not indicator_sell and not threshold_sell:
                    return jsonify(
                        {
                            "error": "'indicator' and 'threshold' are Required Params"
                        }
                    ), 400

                strategy.sell_conditions = sell_conditions

            # Save Changes
            db.session.commit()

            # Get Strategy Data
            buy_conditions: dict = strategy.buy_conditions
            sell_conditions: dict = strategy.sell_conditions

            indicator_buy: str = buy_conditions.get("indicator")
            threshold_buy: float = buy_conditions.get("threshold")
            indicator_sell: str = sell_conditions.get("indicator")
            threshold_sell: float = sell_conditions.get("threshold")

            logger.info(f"----\nSuccessful Update Strategy")
            return jsonify(
                {
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
                        "buy_conditions": {
                            "indicator": indicator_buy,
                            "threshold": threshold_buy
                        },
                        "sell_condition": {
                            "indicator": indicator_sell,
                            "threshold": threshold_sell
                        },
                        "status": strategy.status
                    }
                }
            ), 200
        except Exception as e:
            logger.error(f"An Unexpected Error occurred while Update Strategy | {e}")

    @staticmethod
    @strategy_bp.route(
        "/strategy/delete/<int:strategy_id>",
        methods=[
            "DELETE"
        ]
    )
    @jwt_required()
    def delete_strategy(
            strategy_id: int
    ) -> jsonify:
        """
        Delete Strategy by Strategy Id
        User Authenticate is Required
        """
        logger.info(f"----\nStart Delete Strategy API")

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

            # Delete Strategy
            db.session.delete(strategy)
            db.session.commit()

            logger.info(f"----\nSuccessful Deleted Strategy")
            return jsonify(
                {
                    "success": True
                }
            ), 200
        except Exception as e:
            logger.error(f"An Unexpected Error occurred while Delete Strategy | {e}")
