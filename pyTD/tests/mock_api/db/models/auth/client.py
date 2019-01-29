from sqlalchemy import (Column, Integer, String, Text, Boolean, ForeignKey)
from sqlalchemy.orm import relationship

from db.models.account import Account
from db.models.base import Base
from db.models.auth.tokens import Token


class Client(Base):
    __tablename__ = "client"

    # Meta
    id = Column(Integer, primary_key=True)
    name = Column(String(40))

    # Client information
    client_id = Column(String(40), index=True,
                       nullable=False)
    redirect_uri = Column(String(55), nullable=False)

    # User information
    user_id = Column(ForeignKey('user.id'))
    user = relationship('User')

    # Token information
    tokens = relationship(Token, uselist=False, back_populates="client")

    # Account informatin
    account = relationship(Account, uselist=False, back_populates="client")

    # public or confidential
    is_confidential = Column(Boolean)

    _redirect_uris = Column(Text)
    _default_scopes = Column(Text)

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []
