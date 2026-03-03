import enum
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from app.db import Base


class LinkPrecedence(str, enum.Enum):
    Primary = "primary"
    Secondary = "secondary"

class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phoneNumber = Column(String(20), index=True, nullable=True)
    email = Column(String(255), index=True, nullable=True)

    linkedId = Column(Integer, ForeignKey("contact.id"), index=True, nullable=True)

    createdAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updatedAt = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    deletedAt = Column(DateTime(timezone=True), nullable=True)

    linkPrecedence = Column(
        Enum(LinkPrecedence),
        nullable=False,
        default=LinkPrecedence.Primary
    )
