import logging

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from queries.models import Tags, Problems, ProblemsTags


class ProblemProcessor:
    """Обрабатывает полученные данные и сохраняет их в базу данных."""

    def __init__(self, db_session: AsyncSession, api_client):
        self.db_session = db_session
        self.api_client = api_client

    async def save_tags(self):
        """Сохраняет уникальные теги(темы)"""
        tags = await self.api_client.get_unique_tags()

        # Создание списка словарей для вставки
        tag_objects = [{'name': tag} for tag in tags]

        # Вставка с игнорированием дублирующихся значений
        stmt = insert(Tags).values(tag_objects)
        stmt = stmt.on_conflict_do_nothing(index_elements=['name'])  # Игнорируем конфликты

        try:
            await self.db_session.execute(stmt)
            await self.db_session.commit()
            print('Данные о тегах успешно записаны')
        except IntegrityError:
            await self.db_session.rollback()
            logging.error("Ошибка при добавлении тегов.")

    async def save_problems(self):
        """Сохраняет задачи"""
        problems = await self.api_client.get_problems()

        for problem in problems:
            contest_id = problem.get('contestId')
            index = problem.get('index')
            name = problem.get('name')
            rating = problem.get('rating')

            stmt = select(Problems).where(
                Problems.contest_id == contest_id, Problems.index == index
            )
            check_id_index = await self.db_session.execute(stmt)
            check_id_index = check_id_index.scalars().first()

            if check_id_index:
                check_id_index.name = name
                check_id_index.rating = rating
            else:
                new_problem = Problems(contest_id=contest_id, index=index, name=name,
                                       rating=rating)
                self.db_session.add(new_problem)

        try:
            await self.db_session.commit()
            print('Данные о задачах успешно записаны')
        except IntegrityError:
            await self.db_session.rollback()
            logging.error(f"Ошибка при добавлении задач")

    async def save_problem_statistics(self):
        """Сохраняет статистику задач"""
        statistics = await self.api_client.get_problem_statistics()
        for stat in statistics:
            contest_id = stat.get('contestId')
            index = stat.get('index')
            solved_count = stat.get('solvedCount', 0)

            stmt = select(Problems).where(
                Problems.contest_id == contest_id, Problems.index == index
            )

            check_id_index = await self.db_session.execute(stmt)
            check_id_index = check_id_index.scalars().first()

            if check_id_index:
                check_id_index.solved_count = solved_count

            else:
                new_problem = Problems(solved_count=solved_count)
                self.db_session.add(new_problem)

        try:
            await self.db_session.commit()
            print('Данные о статистике успешно записаны')
        except IntegrityError:
            await self.db_session.rollback()
            logging.error(f"Ошибка при добавлении статистики")

    async def save_problem_tags(self):
        problems = await self.api_client.get_problems()
        for problem in problems:
            contest_id = problem.get('contestId')
            index = problem.get('index')
            tags = problem.get('tags', [])

            stmt = select(Problems.id).where(Problems.contest_id == contest_id, Problems.index == index)

            problem_result = await self.db_session.execute(stmt)
            problem_id = problem_result.scalars().first()

            if problem_id:
                for tag_name in tags:
                    stmt = select(Tags.id).where(Tags.name == tag_name)
                    tag_result = await self.db_session.execute(stmt)
                    tag_id = tag_result.scalars().first()

                    if tag_id:
                        stmt = insert(ProblemsTags).values(
                            problem_id=problem_id, tag_id=tag_id
                        ).on_conflict_do_nothing()

                        await self.db_session.execute(stmt)

        try:
            await self.db_session.commit()
            print('Связи между задачами и тегами успешно сохранены')
        except Exception as e:
            await self.db_session.rollback()
            print("Ошибка при создании связи между темам и задачами")
