from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardBuilder

from src.misc.callback_factories import DealTypeCallback, DeliveryOptionCallback, UsageStatusCallback, SizeCallback, \
    PaymentTermsCallback, PalletSortCallback, ProductTypeCallback, MaterialCallback
from src.misc.enums import DealType, DeliveryOption, UsageStatus, PaymentTerms, PalletSort, ProductType, ProductMaterial


class UserKeyboards:

    @staticmethod
    def get_want_to_create_request() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        builder.button(text='ХОЧУ')
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def get_create_request() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        builder.button(text='Создать заявку')
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def get_cancel_reply() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        builder.button(text='Отменить')
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def get_product_types() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()

        for product_type in ProductType:
            builder.button(text=product_type)

        cancel_builder = ReplyKeyboardBuilder()
        builder.button(text='Отменить')

        builder.attach(cancel_builder)
        builder.adjust(2)
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def get_deal_types() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(text='🛒 Хочу купить', callback_data=DealTypeCallback(deal_type=DealType.BUY))
        builder.button(text='💸 Хочу продать', callback_data=DealTypeCallback(deal_type=DealType.CELL))
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def get_usage_statuses() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(text='🆕 Новый', callback_data=UsageStatusCallback(status=UsageStatus.NEW))
        builder.button(text='🗜 Б/У', callback_data=UsageStatusCallback(status=UsageStatus.USED))
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def get_materials() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(text='Деревянные', callback_data=MaterialCallback(material=ProductMaterial.WOODEN))
        builder.button(text='Пластиковые', callback_data=MaterialCallback(material=ProductMaterial.PLASTIC))
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def get_delivery_options() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(text='🚚 Доставка', callback_data=DeliveryOptionCallback(option=DeliveryOption.DELIVERY))
        builder.button(text='🙌 Самовывоз', callback_data=DeliveryOptionCallback(option=DeliveryOption.PICKUP))
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def get_sizes() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(text='1200x800', callback_data=SizeCallback(size='1200x800'))
        builder.button(text='1200x1000', callback_data=SizeCallback(size='1200x1000'))

        builder.button(text='✍ Нестандартный', callback_data=SizeCallback(size='write'))
        return builder.adjust(2, 1).as_markup()

    @staticmethod
    def get_sorts() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(text='Первый (1)', callback_data=PalletSortCallback(sort=PalletSort.FIRST))
        builder.button(text='Второй (2)', callback_data=PalletSortCallback(sort=PalletSort.SECOND))
        builder.button(text='Третий (3)', callback_data=PalletSortCallback(sort=PalletSort.THIRD))
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def get_cost() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(text='🤝 Договорная', callback_data='cost_by_agreement')
        builder.button(text='✍ Ввести вручную', callback_data='write_cost')
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def get_payment_terms() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(text='Наличными', callback_data=PaymentTermsCallback(term=PaymentTerms.CASH))
        builder.button(text='Переводом на карту', callback_data=PaymentTermsCallback(term=PaymentTerms.CARD))
        builder.button(text='На счёт с НДС', callback_data=PaymentTermsCallback(term=PaymentTerms.WITH_NDS))
        builder.button(text='На счёт без НДС', callback_data=PaymentTermsCallback(term=PaymentTerms.WITHOUT_NDS))
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def get_pass_email_entering() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(text='Пропустить ➡', callback_data='pass_email_empty')
        return builder.as_markup()
