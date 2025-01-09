from flask import g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from backend.user.models import User


def load_user():
    """
    Middleware to Load User from JWT Token
    """
    try:
        verify_jwt_in_request()

        # Get User Id
        user_id: int = get_jwt_identity()
        if user_id:
            # Get User
            user: User = User.query.get(int(user_id))
            if user:
                g.current_user = user
            else:
                g.current_user = None
        else:
            g.current_user = None
    except Exception as e:
        g.current_user = None
