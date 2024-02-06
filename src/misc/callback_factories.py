from typing import Literal

from aiogram.filters.callback_data import CallbackData

from src.misc.enums import DealType, DeliveryOption, UsageStatus, PaymentTerms, PalletSort


class DealTypeCallback(CallbackData, prefix='deal_type'):
    deal_type: DealType


class UsageStatusCallback(CallbackData, prefix='usage_status'):
    status: UsageStatus


class DeliveryOptionCallback(CallbackData, prefix='delivery_option'):
    option: DeliveryOption


class SizeCallback(CallbackData, prefix='size'):
    size: str


class PaymentTermsCallback(CallbackData, prefix='payment_terms'):
    term: PaymentTerms


class PostRequestValidationCallback(CallbackData, prefix='request_validation'):
    request_id: int
    confirm: Literal['True', 'False']


class PalletSortCallback(CallbackData, prefix='sort'):
    sort: PalletSort
