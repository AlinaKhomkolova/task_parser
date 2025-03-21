from sqlalchemy import String, Integer, UniqueConstraint, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Основной базовый класс для всех моделей базы данных."""
    ...


class Tags(Base):
    """Таблица хранит список тегов, каждый тег имеет уникальное название."""
    __tablename__ = 'tags'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)


class Problems(Base):
    """Таблица хранит задачи, которые принадлежат определенному контесту."""
    __tablename__ = 'problems'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    contest_id: Mapped[int] = mapped_column(nullable=False)
    index: Mapped[str] = mapped_column(String(15), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=True)
    solved_count: Mapped[int] = mapped_column(Integer, nullable=True)

    __table_args__ = (UniqueConstraint('contest_id', 'index', name='uq_contest_index'),)


class ProblemsTags(Base):
    """Таблица связывает задачи и теги. Каждая задача может быть связана с несколькими тегами, и каждый тег может быть связан с несколькими задачами."""
    __tablename__ = 'problem_tags'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    problem_id: Mapped[int] = mapped_column(Integer, ForeignKey(
        'problems.id', ondelete='CASCADE'), primary_key=True)
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey(
        'tags.id', ondelete='CASCADE'), primary_key=True)

    __table_args__ = (UniqueConstraint('problem_id', 'tag_id', name='uq_problem_tag'),)
