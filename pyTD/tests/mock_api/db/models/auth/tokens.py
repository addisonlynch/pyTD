from sqlalchemy import (Column, ForeignKey, Integer, String, DateTime,
                        Text)
from sqlalchemy.orm import relationship

from db.models.base import Base
from db.engine import session


class Token(Base):
    __tablename__ = "token"

    # Meta
    id = Column(Integer, primary_key=True)

    # Client information
    client_id = Column(
            String(40), ForeignKey('client.client_id'),
            nullable=False
        )
    client = relationship('Client')

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
    expires = Column(DateTime)
    _scopes = Column(Text)

    def delete(self):
        session.delete(self)
        session.commit()
        return self
