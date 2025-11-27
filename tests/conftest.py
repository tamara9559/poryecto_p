import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.config import get_settings

settings = get_settings()

# Configurar base de datos de pruebas
TEST_DATABASE_URL = settings.DATABASE_URL.replace("/p-pruebas", "/p-pruebas_test")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Fixture que proporciona una sesión de base de datos para pruebas"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def sample_category(db_session):
    """Fixture que crea una categoría de prueba"""
    from app.models.category import Category
    category = Category(name="Electronics")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


@pytest.fixture(scope="function")
def sample_product(db_session, sample_category):
    """Fixture que crea un producto de prueba"""
    from app.models.product import Product
    product = Product(
        name="Laptop",
        description="High-performance laptop",
        price=999.99,
        stock=10,
        category_id=sample_category.id
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product