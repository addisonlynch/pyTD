from sqlalchemy import (Integer, DateTime, String, Text, ForeignKey, Column)
from sqlalchemy.orm import relationship

from db.engine import session
from db.models.base import Base


class Grant(Base):
    """
    TODO: Local caching for optimization
    """
    __tablename__ = "grant"

    # Meta
    id = Column(Integer, primary_key=True)

    # User information
    user_id = Column(ForeignKey('user.id'))
    user = relationship('User')

    # Body
    code = Column(String(255), index=True, nullable=False)

    redirect_uri = Column(String(255))
    expires = Column(DateTime)

    _scopes = Column(Text)

    def delete(self):
        session.delete(self)
        session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []
