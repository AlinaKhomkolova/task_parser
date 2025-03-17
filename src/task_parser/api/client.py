import httpx


class APIClient:
    """Отвечает за отправку запросов к API и получение данных."""

    def __init__(self, url):
        self.url = url

    async def get_data(self):
        """Отправляет GET-запрос и возвращает данные в формате JSON"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.url)
                response.raise_for_status()
                return response.json().get('result', {})
        except httpx.RequestError as e:
            print(f'Ошибка при запросе к API: {e}')
            return {}

    async def get_problems(self):
        """Возвращает список задач"""
        data = await self.get_data()
        return data.get('problems', [])

    async def get_problem_statistics(self):
        """Возвращает статистику по задачам"""
        data = await self.get_data()
        return data.get('problemStatistics', [])

    async def get_unique_tags(self):
        """Возвращает уникальные теги из задач"""
        problems = await self.get_problems()
        unique_tags = set()
        for problem in problems:
            unique_tags.update(problem.get('tags', []))
        return unique_tags
