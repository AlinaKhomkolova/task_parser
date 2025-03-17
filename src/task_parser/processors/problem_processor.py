class ProblemProcessor:
    """Обрабатывает полученные данные и сохраняет их в базу данных."""

    def __init__(self, db_handler, api_client):
        self.db_handler = db_handler
        self.api_client = api_client

    async def save_tags(self):
        """Сохраняет уникальные теги(темы)"""
        tags = await self.api_client.get_unique_tags()
        for tag in tags:

            await  self.db_handler.execute_query(
                """
                INSERT INTO tags (name)
                VALUES ($1)
                ON CONFLICT (name) DO NOTHING;
                """,
                (tag,)
            )
        print('Данные о тегах успешно записаны')

    async def save_problems(self):
        """Сохраняет задачи"""
        problems = await self.api_client.get_problems()
        for problem in problems:
            contest_id = problem.get('contestId')
            index = problem.get('index')
            name = problem.get('name')
            rating = problem.get('rating')
            await self.db_handler.execute_query(
                """
               INSERT INTO problems (contest_id, index, name, rating)
               VALUES ($1, $2, $3, $4)
               ON CONFLICT (contest_id, index) DO NOTHING;
               """,
                (contest_id, index, name, rating),
            )
        print('Данные о задачах успешно записаны')

    async def save_problem_statistics(self):
        """Сохраняет статистику задач"""
        statistics = await self.api_client.get_problem_statistics()
        for stat in statistics:
            contest_id = stat.get('contestId')
            index = stat.get('index')
            solved_count = stat.get('solvedCount', 0)
            await self.db_handler.execute_query(
                """
                UPDATE problems
                SET solved_count = $1
                WHERE contest_id = $2 AND index = $3;
                """,
                (solved_count, contest_id, index),
            )
        print('Данные о статистике успешно записаны')

    async def save_problem_tags(self):
        problems = await self.api_client.get_problems()
        for problem in problems:
            contest_id = problem.get('contestId')
            index = problem.get('index')
            tags = problem.get('tags', [])

            # Получение ID задачи
            problem_id = await self.db_handler.fetch_one(
                """
                SELECT id FROM problems WHERE contest_id = $1 AND index = $2;
                """,
                (contest_id, index)
            )
            if problem_id:
                for tag_name in tags:
                    # Получение ID темы
                    tag_id = await self.db_handler.fetch_one(
                        """
                        SELECT id FROM tags WHERE name = $1;
                        """,
                        (tag_name,)
                    )
                    if tag_id:
                        # Сохранение в таблицу
                        await self.db_handler.execute_query(
                            """
                            INSERT INTO problem_tags (problem_id, tag_id)
                            VALUES ($1, $2)
                            ON CONFLICT DO NOTHING;
                            """,
                            (problem_id[0], tag_id[0])
                        )

        print('Связи между задачами и тегами успешно сохранены')
