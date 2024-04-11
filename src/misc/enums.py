from enum import Enum


class ProductType(str, Enum):
    PALLETS = 'Поддоны'
    CONTAINERS = 'Ящики'
    PALLET_COVER = 'Паллетные крышки'
    PALLET_BOARDS = 'Паллетные борта'


class DealType(Enum):
    BUY = 'Покупка'
    CELL = 'Продажа'

    def __str__(self):
        return self.value


class UsageStatus(Enum):
    NEW = 'Новый'
    USED = 'БУ'

    def __str__(self):
        return self.value


class DeliveryOption(Enum):
    PICKUP = 'Самовывоз'
    DELIVERY = 'Доставка'

    def __str__(self):
        return self.value


class PaymentTerms(Enum):
    CARD = 'Переводом на карту'
    CASH = 'Наличными'
    WITHOUT_NDS = 'без НДС'
    WITH_NDS = 'с НДС'

    def __str__(self):
        return self.value


class PalletSort(Enum):
    FIRST = '1'
    SECOND = '2'
    THIRD = '3'

    def __str__(self):
        return self.value


class ProductMaterial(Enum):
    WOODEN = 'Деревянные'
    PLASTIC = 'Пластиковые'

    def __str__(self):
        return self.value
