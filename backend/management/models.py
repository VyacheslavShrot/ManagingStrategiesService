from sqlalchemy import func, ForeignKey
from sqlalchemy.dialects.postgresql import JSON

from config.database import db


class Strategy(db.Model):
    __tablename__ = 'strategies'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id = db.Column(
        db.Integer,
        ForeignKey('users.id', ondelete="CASCADE"),
        nullable=False
    )
    name = db.Column(
        db.String(255),
        nullable=False
    )
    description = db.Column(
        db.String(500),
        nullable=False
    )
    asset_type = db.Column(
        db.String(50),
        nullable=False
    )
    buy_conditions = db.Column(
        JSON,
        nullable=False
    )
    sell_conditions = db.Column(
        JSON,
        nullable=False
    )
    status = db.Column(
        db.String(50),
        nullable=False,
        default="active"
    )
    created_at = db.Column(
        db.DateTime,
        default=func.now(),
        nullable=False
    )

    def __str__(self):
        return f"{self.id}. {self.name}"
