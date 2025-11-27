import pytest
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductUpdate
from app.exceptions import ResourceNotFoundException, InvalidOperationException


@pytest.mark.unit
class TestProductService:
    
    def test_create_product_success(self, db_session, sample_category):
        """Prueba la creación exitosa de un producto"""
        product_data = ProductCreate(
            name="Smartphone",
            description="Latest model",
            price=599.99,
            stock=20,
            category_id=sample_category.id
        )
        product = ProductService.create_product(db_session, product_data)
        
        assert product.id is not None
        assert product.name == "Smartphone"
        assert product.price == 599.99
        assert product.stock == 20
    
    def test_create_product_invalid_category(self, db_session):
        """Prueba crear un producto con categoría inexistente"""
        product_data = ProductCreate(
            name="Invalid Product",
            description="Test",
            price=100.0,
            stock=5,
            category_id=9999
        )
        
        with pytest.raises(ResourceNotFoundException):
            ProductService.create_product(db_session, product_data)
    
    def test_get_product_success(self, db_session, sample_product):
        """Prueba obtener un producto por ID"""
        product = ProductService.get_product(db_session, sample_product.id)
        
        assert product.id == sample_product.id
        assert product.name == sample_product.name
    
    def test_get_product_not_found(self, db_session):
        """Prueba obtener un producto que no existe"""
        with pytest.raises(ResourceNotFoundException):
            ProductService.get_product(db_session, 9999)
    
    def test_get_products(self, db_session, sample_product, sample_category):
        """Prueba obtener todos los productos"""
        # Crear productos adicionales
        ProductService.create_product(db_session, ProductCreate(
            name="Mouse",
            description="Wireless mouse",
            price=29.99,
            stock=50,
            category_id=sample_category.id
        ))
        
        products = ProductService.get_products(db_session)
        
        assert len(products) >= 2
    
    def test_get_products_by_category(self, db_session, sample_product, sample_category):
        """Prueba filtrar productos por categoría"""
        products = ProductService.get_products(
            db_session, category_id=sample_category.id
        )
        
        assert len(products) >= 1
        assert all(p.category_id == sample_category.id for p in products)
    
    def test_update_product_success(self, db_session, sample_product):
        """Prueba actualizar un producto"""
        update_data = ProductUpdate(
            name="Updated Laptop",
            price=1099.99,
            stock=15
        )
        updated_product = ProductService.update_product(
            db_session, sample_product.id, update_data
        )
        
        assert updated_product.name == "Updated Laptop"
        assert updated_product.price == 1099.99
        assert updated_product.stock == 15
    
    def test_update_product_not_found(self, db_session):
        """Prueba actualizar un producto que no existe"""
        update_data = ProductUpdate(name="New Name")
        
        with pytest.raises(ResourceNotFoundException):
            ProductService.update_product(db_session, 9999, update_data)
    
    def test_delete_product_success(self, db_session, sample_product):
        """Prueba eliminar un producto"""
        result = ProductService.delete_product(db_session, sample_product.id)
        
        assert result is True
        
        with pytest.raises(ResourceNotFoundException):
            ProductService.get_product(db_session, sample_product.id)
    
    def test_delete_product_not_found(self, db_session):
        """Prueba eliminar un producto que no existe"""
        with pytest.raises(ResourceNotFoundException):
            ProductService.delete_product(db_session, 9999)
    
    def test_update_stock_add(self, db_session, sample_product):
        """Prueba incrementar el stock"""
        initial_stock = sample_product.stock
        updated_product = ProductService.update_stock(db_session, sample_product.id, 5)
        
        assert updated_product.stock == initial_stock + 5
    
    def test_update_stock_subtract(self, db_session, sample_product):
        """Prueba decrementar el stock"""
        initial_stock = sample_product.stock
        updated_product = ProductService.update_stock(db_session, sample_product.id, -3)
        
        assert updated_product.stock == initial_stock - 3
    
    def test_update_stock_insufficient(self, db_session, sample_product):
        """Prueba decrementar el stock más allá de cero"""
        with pytest.raises(InvalidOperationException):
            ProductService.update_stock(db_session, sample_product.id, -100)