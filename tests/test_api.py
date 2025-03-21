from unittest import mock
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from src.task_parser.api.client import APIClient

mock_response = {
    "status": "OK",
    "result": {
        "problems": [
            {
                "contestId": 2082,
                "index": "B",
                "name": "Округлить вверх или вниз",
                "type": "PROGRAMMING",
                "points": 1000,
                "rating": 1600,
                "tags": [
                    "brute force",
                    "greedy"
                ]
            },
            {
                "contestId": 2082,
                "index": "A",
                "name": "Бинарная матрица",
                "type": "PROGRAMMING",
                "points": 500,
                "rating": 800,
                "tags": [
                    "constructive algorithms",
                    "greedy"]}
        ],
        "problemStatistics": [{
            "contestId": 1075,
            "index": "B",
            "solvedCount": 4333
        },
            {
                "contestId": 722,
                "index": "D",
                "solvedCount": 3215
            },
        ]
    }
}


# Фикстура для мокирования httpx.AsyncClient
@pytest.fixture
def mock_httpx_client():
    with patch('httpx.AsyncClient') as MockAsyncClient:
        mock_get = AsyncMock()
        MockAsyncClient.return_value.__aenter__.return_value.get = mock_get
        mock_get.return_value.json = AsyncMock(return_value=mock_response)
        yield MockAsyncClient


@pytest.mark.asyncio
async def test_get_data_success(mock_httpx_client):
    client = APIClient(url="https://fakeapi.com")

    data = await client.get_data()
    # Проверяем что метод get_data возвращает нужные данные
    assert data == mock_response['result']


@pytest.mark.asyncio
async def test_get_data_error_handling():
    with mock.patch('httpx.AsyncClient') as MockAsyncClient:
        mock_get = AsyncMock()

        # Имитация ошибки при запросе
        mock_get.side_effect = httpx.RequestError("Request failed", request=None)

        MockAsyncClient.return_value.__aenter__.return_value.get = mock_get

        client = APIClient(url="https://fakeapi.com")
        data = await client.get_data()
        # Проверяем что метод get_data возвращает нужные данные
        assert data == {}

        # Проверяем, что ошибка была залогирована
        with mock.patch('logging.error') as mock_log_error:
            await client.get_data()
            mock_log_error.assert_called_with('Ошибка при запросе к API: Request failed')


@pytest.mark.asyncio
async def test_get_problem_success(mock_httpx_client):
    client = APIClient(url="https://fakeapi.com")

    data = await client.get_problems()
    # Проверяем что метод get_problems возвращает нужные данные
    assert data == mock_response['result']['problems']


@pytest.mark.asyncio
async def test_get_statistics_success(mock_httpx_client):
    client = APIClient(url="https://fakeapi.com")

    data = await client.get_problem_statistics()
    # Проверяем что метод get_problem_statistics возвращает нужные данные
    assert data == mock_response['result']['problemStatistics']


@pytest.mark.asyncio
async def test_get_get_unique_tags_success(mock_httpx_client):
    client = APIClient(url="https://fakeapi.com")

    data = await client.get_unique_tags()
    # Проверяем что метод get_unique_tags возвращает нужные данные
    mock_tags = {"brute force", "greedy", "constructive algorithms"}
    assert data == mock_tags
