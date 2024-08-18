from typing import Optional

from src.domain.entities.category_entity import CategoryEntity
from src.domain.entities.inventory_entity import InventoryEntity
from src.domain.entities.price_entity import PriceEntity
from src.domain.exceptions import InvalidEntity


class ProductEntity:
    def __init__(
        self,
        sku: str,
        name: str,
        category: CategoryEntity,
        price: PriceEntity,
        inventory: InventoryEntity,
        id: Optional[int] = None,
    ):
        self._id = id
        self._sku = sku
        self._name = name
        self._category = category
        self._price = price
        self._inventory = inventory

        # Validate attributes during initialization
        self._validate_id(self._id)
        self._validate_sku(self._sku)
        self._validate_name(self._name)

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: Optional[int]):
        self._validate_id(value)
        self._id = value

    @property
    def sku(self) -> str:
        return self._sku

    @sku.setter
    def sku(self, value: str):
        self._validate_sku(value)
        self._sku = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._validate_name(value)
        self._name = value

    @property
    def category(self) -> CategoryEntity:
        return self._category

    @category.setter
    def category(self, value: CategoryEntity):
        if not isinstance(value, CategoryEntity):
            raise InvalidEntity(
                "Invalid category. Must be a CategoryEntity instance."
            )
        self._category = value

    @property
    def price(self) -> PriceEntity:
        return self._price

    @price.setter
    def price(self, value: PriceEntity):
        if not isinstance(value, PriceEntity):
            raise InvalidEntity(
                "Invalid price. Must be a PriceEntity instance."
            )
        self._price = value

    @property
    def inventory(self) -> InventoryEntity:
        return self._inventory

    @inventory.setter
    def inventory(self, value: InventoryEntity):
        if not isinstance(value, InventoryEntity):
            raise InvalidEntity(
                "Invalid inventory. Must be an InventoryEntity instance."
            )
        self._inventory = value

    def set_inventory(self, quantity: int):
        self.inventory.set_quantity(quantity)

    def set_price(self, amount: float):
        self.price.amount = amount

    def add_inventory(self, quantity: int):
        if quantity < 0:
            raise InvalidEntity("Quantity to add must be positive.")
        self.inventory.quantity += quantity

    def subtract_inventory(self, quantity: int):
        if quantity < 0:
            raise InvalidEntity("Quantity to subtract must be positive.")
        if self.inventory.quantity < quantity:
            raise InvalidEntity(
                f"Cannot subtract {quantity} items. Only "
                f"{self.inventory.quantity} available."
            )
        self.inventory.quantity -= quantity

    def _validate_id(self, id_value: Optional[int]):
        if id_value is not None and (
            not isinstance(id_value, int) or id_value <= 0
        ):
            raise InvalidEntity(
                f"Invalid id: {id_value}. ID must be a positive integer or None."
            )

    def _validate_sku(self, sku_value: str):
        if not isinstance(sku_value, str) or not sku_value.strip():
            raise InvalidEntity(
                f"Invalid SKU: {sku_value}. SKU must be a non-empty string."
            )

    def _validate_name(self, name_value: str):
        if not isinstance(name_value, str) or not name_value.strip():
            raise InvalidEntity(
                f"Invalid name: {name_value}. Name must be a non-empty string."
            )

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "sku": self._sku,
            "name": self._name,
            "category": self._category.to_dict(),
            "price": self._price.to_dict(),
            "inventory": self._inventory.to_dict(),
        }
