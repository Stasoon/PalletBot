from enum import Enum


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

    def __str__(self):
        return self.value
