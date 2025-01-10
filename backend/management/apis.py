from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from backend.cache import RedisCache
from backend.database import Queries
from backend.management.models import Strategy
from backend.management.strategy import StrategyService
from backend.messages import publish_create_strategy_message, publish_update_strategy_message
from backend.request import APIRequest
from backend.user.auth import Auth
from backend.user.models import User
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

        # Global Variables
        api_request: APIRequest = APIRequest()
        auth: Auth = Auth()
        strategy_service: StrategyService = StrategyService()
        cache: RedisCache = RedisCache()

        try:
            # Get User
            user: User | None = auth.get_current_user()
            if not user:
                return jsonify(
                    {
                        "error": "Unauthorized"
                    }
                ), 401

            # Get Data
            data: dict = request.get_json()

            name, description, asset_type, buy_conditions, sell_conditions = api_request.get_data(
                data=data,
                params=[
                    "name", "description", "asset_type", "buy_conditions", "sell_conditions"
                ]
            )
            name: str
            description: str
            asset_type: str
            buy_conditions: dict
            sell_conditions: dict

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

            extra_buy_data, extra_sell_data = strategy_service.validate_buy_sell_conditions(
                buy_conditions=buy_conditions,
                sell_conditions=sell_conditions
            )
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

            strategy: Strategy = strategy_service.create_strategy(
                user_id=user.id,
                name=name,
                description=description,
                asset_type=asset_type,
                buy_conditions=buy_conditions,
                sell_conditions=sell_conditions
            )

            # Delete Cached Strategies
            cache.delete_cache_value(
                f"strategies_{user.id}"
            )

            # Send Message into Channel
            publish_create_strategy_message(
                strategy_name=strategy.name,
                user_id=user.id
            )

            logger.info(f"----\nSuccessful Create Strategy")
            return jsonify(
                api_request.strategy_response(
                    user=user,
                    strategy=strategy
                )
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
    @strategy_bp.route(
        "/strategy",
        methods=["GET"]
    )
    @jwt_required()
    def get_strategy(
            strategy_id: int = None
    ) -> jsonify:
        """
        Get Strategy by Strategy Id
        User Authenticate is Required
        """
        logger.info(f"----\nStart Get Strategy API")

        # Global Variables
        api_request: APIRequest = APIRequest()
        auth: Auth = Auth()
        strategy_service: StrategyService = StrategyService()
        cache: RedisCache = RedisCache()

        try:
            # Get User
            user: User | None = auth.get_current_user()
            if not user:
                return jsonify(
                    {
                        "error": "Unauthorized"
                    }
                ), 401

            if strategy_id:
                # Get Strategy
                strategy: Strategy | None = strategy_service.get_strategy_by_id(
                    strategy_id=strategy_id
                )
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

                logger.info(f"----\nSuccessful Get ONE Strategy")
                return jsonify(
                    api_request.strategy_response(
                        user=user,
                        strategy=strategy
                    )
                ), 200
            else:
                # Get Cached Strategies
                cached_strategies: list | None = cache.get_cache(
                    f"strategies_{user.id}"
                )

                if not cached_strategies:
                    # Get ALL User Strategies
                    strategies: list[Strategy] | None = strategy_service.get_user_strategies(
                        user_id=user.id
                    )
                    if not strategies:
                        return jsonify(
                            {
                                "error": "No Such Strategies for This User"
                            }
                        ), 400

                    # Format Response
                    strategy_list: list = [
                        {
                            "id": strategy.id,
                            "name": strategy.name,
                            "description": strategy.description,
                            "asset_type": strategy.asset_type,
                            "buy_conditions": strategy.buy_conditions,
                            "sell_conditions": strategy.sell_conditions,
                            "status": strategy.status,
                        }
                        for strategy in strategies
                    ]

                    # Save to Cache Strategies
                    cache.set_cache(
                        f"strategies_{user.id}",
                        strategy_list
                    )

                logger.info(f"----\nSuccessful Get ALL User Strategies")
                return jsonify(
                    {
                        "success": True,
                        "user": {
                            "id": user.id,
                            "username": user.username
                        },
                        "strategies": cached_strategies if cached_strategies else strategy_list
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

        # Global Variables
        api_request: APIRequest = APIRequest()
        auth: Auth = Auth()
        strategy_service: StrategyService = StrategyService()
        cache: RedisCache = RedisCache()
        queries: Queries = Queries()

        try:
            # Get User
            user: User | None = auth.get_current_user()
            if not user:
                return jsonify(
                    {
                        "error": "Unauthorized"
                    }
                ), 401

            # Get Strategy
            strategy: Strategy | None = strategy_service.get_strategy_by_id(
                strategy_id=strategy_id
            )
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

            name, description, asset_type, buy_conditions, sell_conditions, status = api_request.get_data(
                data=data,
                params=[
                    "name", "description", "asset_type", "buy_conditions", "sell_conditions", "status"
                ]
            )
            name: str
            description: str
            asset_type: str
            buy_conditions: dict
            sell_conditions: dict
            status: str

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
                extra_buy_data: list = strategy_service.validate_buy_sell_conditions(
                    buy_conditions=buy_conditions,
                    only_buy=True
                )
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
                extra_sell_data: list = strategy_service.validate_buy_sell_conditions(
                    sell_conditions=sell_conditions,
                    only_sell=True
                )
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
            queries.commit()

            # Delete Cached Strategies
            cache.delete_cache_value(
                f"strategies_{user.id}"
            )

            # Send Message into Channel
            publish_update_strategy_message(
                strategy_name=strategy.name,
                user_id=user.id
            )

            logger.info(f"----\nSuccessful Update Strategy")
            return jsonify(
                api_request.strategy_response(
                    user=user,
                    strategy=strategy
                )
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

        # Global Variables
        api_request: APIRequest = APIRequest()
        auth: Auth = Auth()
        strategy_service: StrategyService = StrategyService()
        cache: RedisCache = RedisCache()
        queries: Queries = Queries()

        try:
            # Get User
            user: User | None = auth.get_current_user()
            if not user:
                return jsonify(
                    {
                        "error": "Unauthorized"
                    }
                ), 401

            # Get Strategy
            strategy: Strategy | None = strategy_service.get_strategy_by_id(
                strategy_id=strategy_id
            )
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
            strategy_service.delete_strategy(strategy=strategy)

            # Delete Cached Strategies
            cache.delete_cache_value(
                f"strategies_{user.id}"
            )

            logger.info(f"----\nSuccessful Deleted Strategy")
            return jsonify(
                {
                    "success": True
                }
            ), 200
        except Exception as e:
            logger.error(f"An Unexpected Error occurred while Delete Strategy | {e}")
