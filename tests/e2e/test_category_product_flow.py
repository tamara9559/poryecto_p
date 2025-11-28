import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_e2e_flow.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.mark.e2e
def test_category_product_flow():
    """
    FLUJO AUTOMATIZADO:
    1. Crear categoría
    2. Crear producto asociado
    3. Verificar producto en el listado
    """

    cat_res = client.post("/categories/", json={"name": "Tecnologia"})
    assert cat_res.status_code == 201

    category = cat_res.json()
    assert "id" in category

    prod_res = client.post("/products/", json={
        "name": "Laptop Gamer",
        "description": "Laptop con GPU dedicada",
        "price": 3500,
        "category_id": category["id"]
    })
    assert prod_res.status_code == 201

    product = prod_res.json()
    assert product["name"] == "Laptop Gamer"
    assert product["price"] == 3500

    list_res = client.get("/products/")
    assert list_res.status_code == 200

    product_list = list_res.json()
    assert any(p["id"] == product["id"] for p in product_list)
