import pytest
from app.services.product_service import ProductService
from app.services.category_service import CategoryService
from app.schemas.product import ProductCreate, ProductUpdate
from app.schemas.category import CategoryCreate
from app.exceptions import BadRequestException, NotFoundException


class TestProductService:

    def setup_category(self, db):
        """Crea una categoría auxiliar para productos."""
        cat_service = CategoryService(db)
        return cat_service.create(CategoryCreate(name="Tecnología"))

    def test_create_product(self, db):
        category = self.setup_category(db)
        service = ProductService(db)

        payload = ProductCreate(
            name="Laptop",
            description="Gamer",
            price=2500,
            stock=5,
            category_id=category.id
        )

        product = service.create(payload)

        assert product.id == 1
        assert product.name == "Laptop"

    def test_create_product_invalid_category(self, db):
        service = ProductService(db)

        payload = ProductCreate(
            name="Mouse",
            description="Inalámbrico",
            price=50,
            stock=10,
            category_id=999
        )

        with pytest.raises(BadRequestException):
            service.create(payload)

    def test_list_all_products(self, db):
        category = self.setup_category(db)
        service = ProductService(db)

        service.create(ProductCreate(
            name="A",
            description="Desc A",
            price=10,
            stock=1,
            category_id=category.id
        ))

        service.create(ProductCreate(
            name="B",
            description="Desc B",
            price=20,
            stock=2,
            category_id=category.id
        ))

        result = service.list_all()

        assert len(result) == 2
        assert result[0].name == "A"
        assert result[1].name == "B"

    def test_get_or_404(self, db):
        category = self.setup_category(db)
        service = ProductService(db)

        product = service.create(ProductCreate(
            name="Teclado",
            description="Mecánico",
            price=100,
            stock=3,
            category_id=category.id
        ))

        found = service.get_or_404(product.id)

        assert found.id == product.id

    def test_get_or_404_not_found(self, db):
        service = ProductService(db)

        with pytest.raises(NotFoundException):
            service.get_or_404(100)

    def test_update_product(self, db):
        category = self.setup_category(db)
        service = ProductService(db)

        product = service.create(ProductCreate(
            name="Monitor",
            description="24 pulgadas",
            price=800,
            stock=2,
            category_id=category.id
        ))

        payload = ProductUpdate(
            name="Monitor FHD",
            price=900
        )

        updated = service.update(product.id, payload)

        assert updated.name == "Monitor FHD"
        assert updated.price == 900

    def test_delete_product(self, db):
        category = self.setup_category(db)
        service = ProductService(db)

        product = service.create(ProductCreate(
            name="USB",
            description="32GB",
            price=20,
            stock=50,
            category_id=category.id
        ))

        service.delete(product.id)

        with pytest.raises(NotFoundException):
            service.get_or_404(product.id)
