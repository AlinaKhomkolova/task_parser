from sqlalchemy import distinct
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from queries.models import Tags, ProblemsTags, Problems


class ProblemsQueries:
    """Класс для выполнения запросов к базе данных, связанных с задачами и тегами."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_tags(self):
        """Получение списка всех уникальных названий тегов из базы данных."""
        stmt = (
            select(Tags.name)
            .where(Tags.name.isnot(None))
            .distinct()
            .order_by(Tags.name)
        )
        async with self.db_session as db:
            result = await db.execute(stmt)
        return result.scalars().all()

    async def get_rating(self, tag_name):
        """Получение всех уникальных значений рейтинга задач для заданного тега."""
        stmt = (
            select(distinct(Problems.rating))
            .join(ProblemsTags, Problems.id == ProblemsTags.problem_id)
            .join(Tags, ProblemsTags.tag_id == Tags.id)
            .where(Tags.name == tag_name, Problems.rating.isnot(None))
            .order_by(Problems.rating)
        )
        async with self.db_session as db:
            result = await db.execute(stmt)
        return result.scalars().all()

    async def get_problem_to_criteria(self, tag_name, rating):
        """Получение списка задач, соответствующих заданному тегу и рейтингу."""
        stmt = (
            select(Problems.name, Problems.rating, Problems.contest_id, Problems.index, Problems.solved_count,
                   Tags.name)
            .join(ProblemsTags, Problems.id == ProblemsTags.problem_id)
            .join(Tags, ProblemsTags.tag_id == Tags.id)
            .where(Tags.name == tag_name, Problems.rating == rating)
            .order_by(Problems.rating)
        )
        async with self.db_session as db:
            result = await db.execute(stmt)
        return result.mappings().fetchall()
