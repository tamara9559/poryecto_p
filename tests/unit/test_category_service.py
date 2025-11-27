import pytest
from app.services.category_service import CategoryService
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.exceptions import ResourceNotFoundException, DuplicateResourceException


@pytest.mark.unit
class TestCategoryService:
    
    def test_create_category_success(self, db_session):
        """Prueba la creación exitosa de una categoría"""
        category_data = CategoryCreate(name="Books")
        category = CategoryService.create_category(db_session, category_data)
        
        assert category.id is not None
        assert category.name == "Books"
    
    def test_create_category_duplicate(self, db_session, sample_category):
        """Prueba que no se pueden crear categorías duplicadas"""
        category_data = CategoryCreate(name=sample_category.name)
        
        with pytest.raises(DuplicateResourceException):
            CategoryService.create_category(db_session, category_data)
    
    def test_get_category_success(self, db_session, sample_category):
        """Prueba obtener una categoría por ID"""
        category = CategoryService.get_category(db_session, sample_category.id)
        
        assert category.id == sample_category.id
        assert category.name == sample_category.name
    
    def test_get_category_not_found(self, db_session):
        """Prueba obtener una categoría que no existe"""
        with pytest.raises(ResourceNotFoundException):
            CategoryService.get_category(db_session, 9999)
    
    def test_get_categories(self, db_session, sample_category):
        """Prueba obtener todas las categorías"""
        # Crear categorías adicionales
        CategoryService.create_category(db_session, CategoryCreate(name="Sports"))
        CategoryService.create_category(db_session, CategoryCreate(name="Food"))
        
        categories = CategoryService.get_categories(db_session)
        
        assert len(categories) >= 3
    
    def test_update_category_success(self, db_session, sample_category):
        """Prueba actualizar una categoría"""
        update_data = CategoryUpdate(name="Updated Electronics")
        updated_category = CategoryService.update_category(
            db_session, sample_category.id, update_data
        )
        
        assert updated_category.name == "Updated Electronics"
    
    def test_update_category_not_found(self, db_session):
        """Prueba actualizar una categoría que no existe"""
        update_data = CategoryUpdate(name="New Name")
        
        with pytest.raises(ResourceNotFoundException):
            CategoryService.update_category(db_session, 9999, update_data)
    
    def test_delete_category_success(self, db_session, sample_category):
        """Prueba eliminar una categoría"""
        result = CategoryService.delete_category(db_session, sample_category.id)
        
        assert result is True
        
        with pytest.raises(ResourceNotFoundException):
            CategoryService.get_category(db_session, sample_category.id)
    
    def test_delete_category_not_found(self, db_session):
        """Prueba eliminar una categoría que no existe"""
        with pytest.raises(ResourceNotFoundException):
            CategoryService.delete_category(db_session, 9999)
    
    def test_get_category_by_name(self, db_session, sample_category):
        """Prueba buscar categoría por nombre"""
        category = CategoryService.get_category_by_name(db_session, sample_category.name)
        
        assert category is not None
        assert category.name == sample_category.name
    
    def test_get_category_by_name_not_found(self, db_session):
        """Prueba buscar categoría por nombre que no existe"""
        category = CategoryService.get_category_by_name(db_session, "NonExistent")
        
        assert category is None