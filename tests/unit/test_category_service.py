import pytest
from app.services.category_service import CategoryService
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.exceptions import ConflictException, NotFoundException


class TestCategoryService:

    def test_create_category(self, db):
        service = CategoryService(db)

        payload = CategoryCreate(name="Electrónica")
        category = service.create(payload)

        assert category.id == 1
        assert category.name == "Electrónica"

    def test_create_category_duplicate(self, db):
        service = CategoryService(db)

        service.create(CategoryCreate(name="Ropa"))

        with pytest.raises(ConflictException):
            service.create(CategoryCreate(name="Ropa"))

    def test_list_all(self, db):
        service = CategoryService(db)

        service.create(CategoryCreate(name="A"))
        service.create(CategoryCreate(name="B"))

        result = service.list_all()

        assert len(result) == 2
        assert result[0].name == "A"
        assert result[1].name == "B"

    def test_get_or_404_success(self, db):
        service = CategoryService(db)

        created = service.create(CategoryCreate(name="Juegos"))
        fetched = service.get_or_404(created.id)

        assert fetched.id == created.id

    def test_get_or_404_not_found(self, db):
        service = CategoryService(db)

        with pytest.raises(NotFoundException):
            service.get_or_404(999)

    def test_update_category(self, db):
        service = CategoryService(db)
        created = service.create(CategoryCreate(name="Computo"))

        payload = CategoryUpdate(name="Tecnología")
        updated = service.update(created.id, payload)

        assert updated.name == "Tecnología"

    def test_delete_category(self, db):
        service = CategoryService(db)
        created = service.create(CategoryCreate(name="Eliminar"))

        service.delete(created.id)

        with pytest.raises(NotFoundException):
            service.get_or_404(created.id)
