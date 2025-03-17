import logging

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
                response_json = response.json()
                if 'result' in response_json:
                    return response_json['result'] # Если в ответе есть 'result', возвращаем его
                else:
                    logging.error('Данных в result для поиска нет')
                    return {}  # Возвращаем пустой словарь, если 'result' нет
        except httpx.RequestError as e:
            logging.error(f'Ошибка при запросе к API: {e}')
            return {} # Возвращаем пустой словарь в случае ошибки запроса

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
