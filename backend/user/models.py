from flask_bcrypt import Bcrypt
from sqlalchemy import func

from config.database import db

bcrypt: Bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    username = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )
    password_hash = db.Column(
        db.String(255),
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        default=func.now(),
        nullable=False
    )

    def __str__(self):
        return f"{self.id}. {self.username}"

    def set_password(
            self,
            password: str
    ) -> None:
        """
        Hash and set the password
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(
            self,
            password: str
    ) -> bool:
        """
        Check if the password matches the hash
        """
        return bcrypt.check_password_hash(self.password_hash, password)
