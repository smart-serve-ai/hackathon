import string

import nanoid
from sqlalchemy import JSON, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


def generate_nanoid(size: int = 21) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return nanoid.generate(alphabet=alphabet, size=size)


class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(String(21), primary_key=True, default=generate_nanoid)
    phone: Mapped[str] = mapped_column(String, unique=True)
    goals: Mapped[list["Goal"]] = relationship(back_populates="user")


class Goal(Base):
    __tablename__ = "goal"

    id: Mapped[str] = mapped_column(String(21), primary_key=True, default=generate_nanoid)
    user_id: Mapped[str] = mapped_column(String(21), ForeignKey("user.id"))
    title: Mapped[str]
    description: Mapped[str] = mapped_column(Text)
    conversation_history: Mapped[list[dict]] = mapped_column(JSON)
    user: Mapped[User] = relationship(back_populates="goals")
    results: Mapped[list["Result"]] = relationship(back_populates="goal")


class Result(Base):
    __tablename__ = "result"

    id: Mapped[str] = mapped_column(String(21), primary_key=True, default=generate_nanoid)
    goal_id: Mapped[str] = mapped_column(String(21), ForeignKey("goal.id"))
    details: Mapped[dict] = mapped_column(JSON)
    goal: Mapped[Goal] = relationship(back_populates="results")
