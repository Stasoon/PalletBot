from peewee import (
    Model, PostgresqlDatabase, SqliteDatabase, AutoField,
    SmallIntegerField, BigIntegerField, IntegerField,
    DateTimeField, CharField, TextField, BooleanField,
    ForeignKeyField, Field
)

from src.misc.enums import DealType, UsageStatus, DeliveryOption, PaymentTerms, PalletSort, ProductMaterial

db = SqliteDatabase(
    database='data.db'
    # DatabaseConfig.NAME,
    # user=DatabaseConfig.USER, password=DatabaseConfig.PASSWORD,
    # host=DatabaseConfig.HOST, port=DatabaseConfig.PORT
)


class EnumField(Field):
    def __init__(self, enum_class, *args, **kwargs):
        self.enum_class = enum_class
        super(EnumField, self).__init__(*args, **kwargs)

    def db_value(self, value):
        return value.value if value is not None else None

    def python_value(self, value):
        if value is not None:
            return self.enum_class(value)
        return None


class _BaseModel(Model):
    class Meta:
        database = db


class User(_BaseModel):
    """ Пользователь бота """
    class Meta:
        db_table = 'users'

    telegram_id = BigIntegerField(primary_key=True, unique=True, null=False)
    name = CharField(default='Пользователь')
    username = CharField(null=True, default='Пользователь')
    referral_link = CharField(null=True)
    last_activity = DateTimeField(null=True)
    registration_timestamp = DateTimeField()


class PostRequest(_BaseModel):
    class Meta:
        db_table = 'post_request'

    number = IntegerField(primary_key=True, unique=True, null=False)
    user = ForeignKeyField(model=User)

    product_type = CharField()
    size = CharField()
    sort = EnumField(enum_class=PalletSort)
    material = EnumField(enum_class=ProductMaterial)

    usage_status = EnumField(enum_class=UsageStatus)
    delivery_option = EnumField(enum_class=DeliveryOption)
    address = CharField(max_length=800)
    payment_terms = EnumField(enum_class=PaymentTerms)

    deal_type = EnumField(enum_class=DealType)
    cost = CharField(null=True)
    phone_number = CharField()
    email = CharField(null=True)


class PostPublication(_BaseModel):
    class Meta:
        db_table = 'post_publication'

    number = IntegerField(primary_key=True, unique=True, null=False)
    post = ForeignKeyField(model=PostRequest)


class Admin(_BaseModel):
    """ Администратор бота """
    class Meta:
        db_table = 'admins'

    telegram_id = BigIntegerField(unique=True, null=False)
    name = CharField()


def register_models() -> None:
    for model in _BaseModel.__subclasses__():
        model.create_table()
