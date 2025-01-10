from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from backend.request import APIRequest
from backend.user.auth import Auth
from backend.user.models import User
from config.logger import logger

user_bp: Blueprint = Blueprint('user', __name__)


class UserApis:

    @staticmethod
    @user_bp.route(
        "/auth/register",
        methods=[
            "POST"
        ]
    )
    def register(
    ) -> jsonify:
        """
        Create New User
        """

        logger.info(f"----\nStart Register API")

        # Global Variables
        api_request: APIRequest = APIRequest()
        auth: Auth = Auth()

        try:
            # Get Data
            data: dict = request.get_json()

            username, password = api_request.get_data(
                data=data,
                params=[
                    "username", "password"
                ]
            )
            if not username or not password:
                return jsonify(
                    {
                        "error": "'username' and 'password' are Required Params"
                    }
                ), 400

            # Check Such User with Such Params
            user: User = User.query.filter_by(username=username).first()
            if user:
                return jsonify(
                    {
                        "error": "Such User with Such username Already Exists"
                    }
                ), 400

            # Create New User
            new_user: User = auth.create_user(
                username=username,
                password=password
            )

            # Create JWT Token
            token: str = create_access_token(
                identity=str(new_user.id)
            )

            logger.info(f"----\nSuccessful Register User")
            return jsonify(
                api_request.user_response(
                    user=new_user,
                    token=token
                )
            ), 201
        except Exception as e:
            logger.error(f"An Unexpected Error occurred while Register User | {e}")

    @staticmethod
    @user_bp.route(
        "/auth/login",
        methods=[
            "POST"
        ]
    )
    def login(
    ) -> jsonify:
        """
        Login User by Username and Password
        """

        logger.info(f"----\nStart Login API")

        # Global Variables
        api_request: APIRequest = APIRequest()

        try:
            # Get Data
            data: dict = request.get_json()

            username, password = api_request.get_data(
                data=data,
                params=[
                    "username", "password"
                ]
            )
            if not username or not password:
                return jsonify(
                    {
                        "error": "'username' and 'password' are Required Params"
                    }
                ), 400

            user: User = User.query.filter_by(username=username).first()
            if not user or not user.check_password(password):
                return jsonify(
                    {
                        "error": "Invalid username or password"
                    }
                ), 401

            # Create JWT Token
            token: str = create_access_token(
                identity=str(user.id)
            )

            logger.info(f"----\nSuccessful Login User")

            return jsonify(
                api_request.user_response(
                    user=user,
                    token=token
                )
            ), 200
        except Exception as e:
            logger.error(f"An Unexpected Error occurred while Login User | {e}")
