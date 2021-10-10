import pytest
from httpx import AsyncClient
from starlette import status

pytestmark = pytest.mark.asyncio


async def test_main(async_client: AsyncClient) -> None:
    response = await async_client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}
