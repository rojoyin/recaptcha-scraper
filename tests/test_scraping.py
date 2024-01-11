from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_scrape_invalid_url():
    invalid_url = "invalidvalue"
    response = client.post("/scrape/", json={"url": invalid_url})
    assert response.status_code == 422
    assert response.json().get("detail") is not None
