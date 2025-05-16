import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient):
    data = {"username": "user",
            "password": "pass"}
    await client.post("/register", json=data)
    response = await client.post("/login", data=data)
    tokens = response.json()


    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {tokens["access_token"]}"}
    )
    assert response.status_code == 200
    assert "username" in response.json()