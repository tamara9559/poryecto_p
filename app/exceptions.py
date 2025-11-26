class InventoryException(Exception):
    """Excepción base para el sistema de inventario"""
    pass


class ResourceNotFoundException(InventoryException):
    """Excepción cuando no se encuentra un recurso"""
    def __init__(self, resource: str, resource_id: int):
        self.resource = resource
        self.resource_id = resource_id
        super().__init__(f"{resource} with id {resource_id} not found")


class DuplicateResourceException(InventoryException):
    """Excepción cuando se intenta crear un recurso duplicado"""
    def __init__(self, resource: str, field: str, value: str):
        self.resource = resource
        self.field = field
        self.value = value
        super().__init__(f"{resource} with {field}='{value}' already exists")


class InvalidOperationException(InventoryException):
    """Excepción para operaciones inválidas"""
    pass


class DatabaseException(InventoryException):
    """Excepción para errores de base de datos"""
    pass