import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_integration.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)


@pytest.mark.integration
def test_create_product():
    category = client.post("/categories/", json={"name": "Hogar"}).json()

    payload = {
        "name": "Silla Gamer",
        "description": "Silla ergonómica",
        "price": 500,
        "category_id": category["id"]
    }

    response = client.post("/products/", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["name"] == "Silla Gamer"
    assert data["price"] == 500

    assert "category_id" not in data


@pytest.mark.integration
def test_list_products():
    response = client.get("/products/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

