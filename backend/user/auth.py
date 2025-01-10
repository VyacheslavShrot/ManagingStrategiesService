from flask import g

from backend.database import Queries
from backend.user.models import User


class Auth(
    Queries
):
    # Name of Variable from Middleware
    _current_user: str = "current_user"

    def create_user(
            self,
            username: str,
            password: str
    ) -> User:
        """
        Create New User and Save into DB
        """
        # Create User
        user: User = User(
            username=username
        )
        user.set_password(password)

        # Add into DB and Save
        self.add_and_commit(
            models_object=user
        )

        return user

    def get_current_user(
            self
    ) -> User | None:
        """
        Get Current User by Token
        """
        return g.get(self._current_user, None)
