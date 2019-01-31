from datetime import datetime, timedelta
import time

from sqlalchemy import (Column, ForeignKey, Integer, String, DateTime,
                        Text)
from sqlalchemy.orm import relationship

from db.models.base import Base
from db.engine import session
import uuid


class Token(Base):
    __tablename__ = "token"

    # Meta
    id = Column(Integer, primary_key=True)

    # Client information
    client_id = Column(
            String(40), ForeignKey('client.client_id'),
            nullable=False
        )
    client = relationship('Client', back_populates="tokens")

    # User information
    user_id = Column(
            String(40), ForeignKey('user.id')
        )
    user = relationship('User')

    # Body
    # Currently only bearer is supported
    token_type = Column(String(40))

    access_token = Column(String(255), unique=True)
    refresh_token = Column(String(255), unique=True)
    access_expires = Column(DateTime)
    refresh_expires = Column(DateTime)
    scope = Column(Text)

    def delete(self):
        session.delete(self)
        session.commit()
        return self

    @staticmethod
    def generate_tokens():
        now = datetime.now()

        d = {
            "refresh_token": uuid.uuid4().hex,
            "access_token": uuid.uuid4().hex,
            "refresh_expires": now + timedelta(minutes=90),
            "access_expires": now + timedelta(days=90),
            "scope": "",
            "token_type": "string"
        }

        return d

    @property
    def access_valid(self):
        now = datetime.now()
        return self.access_token and self.access_expires > now
