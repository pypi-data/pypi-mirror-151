from __future__ import annotations

from collections import ChainMap
from datetime import datetime
from typing import Any, Optional

import ckan.model as model
from ckan.lib.dictization import table_dictize
from ckan.model.types import make_uuid
from sqlalchemy import Column, DateTime, ForeignKey, UnicodeText, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey
from typing_extensions import Self

from .base import Base


class Flake(Base):
    __tablename__ = "flakes_flake"

    id = Column(UnicodeText, primary_key=True, default=make_uuid)
    name: Optional[str] = Column(UnicodeText, unique=True, nullable=True)
    data: dict[str, Any] = Column(JSONB, nullable=False)
    modified_at: datetime = Column(DateTime, nullable=False, default=datetime.utcnow)
    author_id: str = Column(UnicodeText, ForeignKey(model.User.id), nullable=False)
    parent_id: Optional[str] = Column(UnicodeText, ForeignKey("flakes_flake.id"))
    extras: dict[str, Any] = Column(JSONB, nullable=False, default=dict)

    UniqueConstraint(name, author_id)

    author = relationship(
        model.User,
        backref=backref("flakes", cascade="all, delete-orphan"),
    )
    parent = relationship(
        "Flake",
        backref=backref("flakes", cascade="all, delete-orphan", single_parent=True),
        remote_side=[id],
    )

    def dictize(self, context: dict[str, Any]):
        result = table_dictize(self, context)

        if context.get("expand"):
            sources = [self.data]
            parent = self.parent

            while parent:
                sources.append(parent.data)
                parent = parent.parent

            result["data"] = dict(ChainMap(*sources))

        return result

    @classmethod
    def by_name(cls, name: str, author_id: str) -> Optional[Self]:
        return (
            model.Session.query(cls)
            .filter_by(name=name, author_id=author_id)
            .one_or_none()
        )
