from aiogram import html


class UserMessages:

    @staticmethod
    def get_welcome(user_name: str) -> str:
        return f'👋 Привет, {html.quote(user_name)}!'

    @staticmethod
    def ask_for_deal_type() -> str:
        return 'Выберите тип сделки:'

    @staticmethod
    def ask_for_usage_status() -> str:
        return 'Новый или БУ?'

    @staticmethod
    def ask_for_delivery_terms() -> str:
        return 'Выберите условия поставки:'

    @staticmethod
    def ask_for_pickup_address() -> str:
        return 'Напишите адрес, с которого можно осуществить самовывоз:\n\n<i>(Область, Город, Улица, Номер дома)</i>'

    @staticmethod
    def ask_for_delivery_address() -> str:
        return 'Напишите, куда вы готовы осуществить доставку: \n\n<i>(Область, Город)</i>'

    @staticmethod
    def ask_for_cost() -> str:
        return 'Выберите стоимость:'

    @staticmethod
    def ask_for_sort() -> str:
        return 'Выберите сорт:'

    @staticmethod
    def ask_for_size() -> str:
        return '📐 Выберите размер поддона'

    @staticmethod
    def ask_payment_terms() -> str:
        return 'Выберите условия оплаты:'

    @staticmethod
    def ask_for_phone() -> str:
        return '☎ Введите контактный номер телефона:'

    @staticmethod
    def ask_for_email() -> str:
        return '✉ Введите адрес вашей электронной почты: '

