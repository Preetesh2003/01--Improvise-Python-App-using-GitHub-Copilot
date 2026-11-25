import hashlib

import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as test_client:
        yield test_client


@pytest.mark.anyio
async def test_home_page_has_welcome_and_checksum_form(client):
    response = await client.get("/")

    assert response.status_code == 200
    assert "Welcome, Preetesh Singha!" in response.text
    assert 'id="checksum-form"' in response.text


@pytest.mark.anyio
async def test_generate_route_returns_sha256_checksum(client):
    response = await client.post("/generate", json={"text": "hello"})

    assert response.status_code == 200
    assert response.json() == {
        "checksum": hashlib.sha256(b"hello").hexdigest()
    }


@pytest.mark.anyio
async def test_checksum_route_returns_sha256_checksum(client):
    response = await client.post("/checksum", json={"text": "hello"})

    assert response.status_code == 200
    assert response.json() == {
        "checksum": hashlib.sha256(b"hello").hexdigest()
    }


@pytest.mark.anyio
async def test_checksum_route_requires_text(client):
    response = await client.post("/checksum", json={})

    assert response.status_code == 422
