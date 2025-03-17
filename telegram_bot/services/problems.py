from settings import db_config
from src.task_parser.database.handler import DatabaseHandler


class Problems:
    def __init__(self, name_column, name_table):
        self.db = DatabaseHandler(db_config)
        self.name_column = name_column
        self.name_table = name_table

    async def get_items(self):
        async with self.db as db:
            query = f'SELECT DISTINCT {self.name_column} FROM {self.name_table} WHERE {self.name_column} IS NOT NULL'
            rows = await self.db.fetch_query(query)
            return sorted(list(set([row[self.name_column] for row in rows])))

    @staticmethod
    async def get_problem_to_criteria(db, tag_name, rating):
        async with db as db_conn:
            query = """
                SELECT p.name, p.rating, p.contest_id, p.index, p.solved_count, t.name AS tag_name
                FROM problems p
                JOIN problem_tags pt ON p.id = pt.problem_id
                JOIN tags t ON pt.tag_id = t.id
                WHERE t.name = $1 AND p.rating = $2
                ORDER BY p.rating
                """
            rows = await db_conn.fetch_query(query, (tag_name, rating))

            return rows
