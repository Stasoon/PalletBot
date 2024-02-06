from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter

from src.database import users
from src.database.models import PostRequest
from src.handlers.admin.requests_approving import send_post_to_admins_approving
from src.keyboards.user import UserKeyboards
from src.messages.user import UserMessages
from src.database.users import create_user_if_not_exist
from src.misc.callback_factories import DealTypeCallback, UsageStatusCallback, DeliveryOptionCallback, SizeCallback, \
    PaymentTermsCallback, PalletSortCallback
from src.misc.enums import DeliveryOption


class RequestCreatingStates(StatesGroup):
    enter_deal_type = State()

    enter_usage_status = State()
    enter_size = State()
    enter_sort = State()

    enter_cost = State()
    enter_payment_terms = State()

    enter_delivery_option = State()
    enter_address = State()

    enter_phone = State()
    enter_email = State()


async def handle_cancel_button(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text='Создание заявки отменено',
        reply_markup=UserKeyboards.get_create_request()
    )


async def handle_start_command(message: Message, state: FSMContext):
    await state.clear()

    user = message.from_user
    create_user_if_not_exist(telegram_id=user.id, firstname=user.first_name, username=user.username)

    text = UserMessages.get_welcome(user_name=user.first_name)
    await message.answer(text=text, reply_markup=UserKeyboards.get_create_request())


async def handle_create_request_button(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Хорошо! Давайте создадим заявку', reply_markup=UserKeyboards.get_cancel_reply())
    await message.answer(text=UserMessages.ask_for_deal_type(), reply_markup=UserKeyboards.get_deal_types())
    await state.set_state(RequestCreatingStates.enter_deal_type)


async def handle_deal_type_callback(callback: CallbackQuery, callback_data: DealTypeCallback, state: FSMContext):
    await state.update_data(deal_type=callback_data.deal_type)

    await callback.message.edit_text(text=f"🔸Тип сделки: <b>{callback_data.deal_type}</b>", reply_markup=None)
    await callback.message.answer(
        text=UserMessages.ask_for_usage_status(),
        reply_markup=UserKeyboards.get_usage_statuses()
    )
    await state.set_state(RequestCreatingStates.enter_usage_status)


async def handle_usage_status_callback(callback: CallbackQuery, callback_data: UsageStatusCallback, state: FSMContext):
    await state.update_data(usage_status=callback_data.status)

    await callback.message.edit_text(text=f"🔸Состояние: <b>{callback_data.status}</b>", reply_markup=None)

    await callback.message.answer(text=UserMessages.ask_for_size(), reply_markup=UserKeyboards.get_sizes())
    await state.set_state(RequestCreatingStates.enter_size)


async def handle_size_callback(callback: CallbackQuery, callback_data: SizeCallback, state: FSMContext):
    if callback_data.size == 'write':
        await callback.message.delete()
        await callback.message.answer(
            text='📐 Введите размеры паллета в формате <b>ДЛИНА х ШИРИНА</b> (мм): \n\n'
                 '<i>Например: 1000х1000</i>')
        return

    await state.update_data(size=callback_data.size)
    await callback.message.edit_text(text=f"🔸Размер: <b>{callback_data.size}</b>", reply_markup=None)

    await callback.message.answer(text=UserMessages.ask_for_sort(), reply_markup=UserKeyboards.get_sorts())
    await state.set_state(RequestCreatingStates.enter_sort)


async def handle_size_message(message: Message, state: FSMContext):
    await state.update_data(size=message.text)
    await message.answer(text=UserMessages.ask_for_sort(), reply_markup=UserKeyboards.get_sorts())
    await state.set_state(RequestCreatingStates.enter_sort)


async def handle_pallet_sort_callback(callback: CallbackQuery, callback_data: PalletSortCallback, state: FSMContext):
    await state.update_data(sort=callback_data.sort)
    await callback.message.edit_text(text=f"🔸Сорт: <b>{callback_data.sort}</b>", reply_markup=None)

    await callback.message.answer(text=UserMessages.ask_for_cost(), reply_markup=UserKeyboards.get_cost())
    await state.set_state(RequestCreatingStates.enter_cost)


async def handle_agreement_cost_callback(callback: CallbackQuery, state: FSMContext):
    await state.update_data(cost=None)

    await callback.message.edit_text(text=f"🔸Стоимость: <b>Договорная</b>", reply_markup=None)
    await callback.message.answer(
        text=UserMessages.ask_payment_terms(), reply_markup=UserKeyboards.get_payment_terms()
    )
    await state.set_state(RequestCreatingStates.enter_payment_terms)


async def handle_write_cost_callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text='<b>₽</b> Напишите стоимость:')


async def handle_cost_message(message: Message, state: FSMContext):
    await state.update_data(cost=message.text)
    await message.answer(
        text=UserMessages.ask_payment_terms(), reply_markup=UserKeyboards.get_payment_terms()
    )
    await state.set_state(RequestCreatingStates.enter_payment_terms)


async def handle_payment_terms_callback(callback: CallbackQuery, callback_data: PaymentTermsCallback, state: FSMContext):
    await state.update_data(payment_terms=callback_data.term)

    await callback.message.edit_text(text=f"🔸Условия оплаты: <b>{callback_data.term}</b>", reply_markup=None)

    await callback.message.answer(
        text=UserMessages.ask_for_delivery_terms(), reply_markup=UserKeyboards.get_delivery_options()
    )
    await state.set_state(RequestCreatingStates.enter_delivery_option)


async def handle_delivery_options_callback(callback: CallbackQuery, callback_data: DeliveryOptionCallback, state: FSMContext):
    await state.update_data(delivery_option=callback_data.option)

    await callback.message.edit_text(text=f"🔸Условие поставки: <b>{callback_data.option}</b>", reply_markup=None)

    match callback_data.option:
        case DeliveryOption.PICKUP:
            text = UserMessages.ask_for_pickup_address()
        case _:
            text = UserMessages.ask_for_delivery_address()

    await callback.message.answer(text=text, reply_markup=None)
    await state.set_state(RequestCreatingStates.enter_address)


async def handle_address_message(message: Message, state: FSMContext):
    if len(message.text) < 5:
        await message.answer('Пожалуйста, предоставьте более подробную информацию')
        return

    await state.update_data(address=message.text)

    await message.answer(text=UserMessages.ask_for_phone())
    await state.set_state(RequestCreatingStates.enter_phone)


async def handle_phone_number_message(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)

    await message.answer(text=UserMessages.ask_for_email(), reply_markup=UserKeyboards.get_pass_email_entering())
    await state.set_state(RequestCreatingStates.enter_email)


async def handle_email_message(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    data = await state.get_data()

    await finish(data=data, bot=message.bot, user_id=message.from_user.id)
    await state.clear()


async def handle_pass_email_empty_callback(callback: CallbackQuery, state: FSMContext):
    await state.update_data(email=None)
    await callback.message.edit_reply_markup(reply_markup=None)
    data = await state.get_data()

    await finish(data=data, bot=callback.bot, user_id=callback.from_user.id)
    await state.clear()


async def finish(data: dict, user_id: int, bot: Bot):
    await bot.send_message(
        chat_id=user_id,
        text='✅ Готово! Ваша заявка отправлена на рассмотрение.',
        reply_markup=UserKeyboards.get_create_request()
    )

    user = users.get_user_or_none(telegram_id=user_id)
    post = PostRequest.create(
        user=user, deal_type=data.get('deal_type'), usage_status=data.get('usage_status'),
        delivery_option=data.get('delivery_option'), size=data.get('size'), cost=data.get('cost'),
        payment_terms=data.get('payment_terms'), sort=data.get('sort'),
        phone_number=data.get('phone_number'), address=data.get('address'), email=data.get('email')
    )
    await send_post_to_admins_approving(bot=bot, post=post)


def register_user_handlers(router: Router):
    # Команда /start
    router.message.register(handle_start_command, CommandStart())

    # Отмена создания заявки
    router.message.register(handle_cancel_button, F.text == 'Отменить')

    # Кнопка "Создать заявку"
    router.message.register(
        handle_create_request_button,
        F.text.lower().contains('создать заявку'),
        StateFilter(default_state)
    )

    # Тип сделки (покупка / продажа)
    router.callback_query.register(
        handle_deal_type_callback, DealTypeCallback.filter(), RequestCreatingStates.enter_deal_type
    )

    # Состояние (новое / бу)
    router.callback_query.register(
        handle_usage_status_callback, UsageStatusCallback.filter(), RequestCreatingStates.enter_usage_status
    )

    # Размер поддона
    router.callback_query.register(handle_size_callback, SizeCallback.filter(), RequestCreatingStates.enter_size)
    router.message.register(handle_size_message, RequestCreatingStates.enter_size)

    # Сорт
    router.callback_query.register(
        handle_pallet_sort_callback, PalletSortCallback.filter(), RequestCreatingStates.enter_sort
    )

    # Стоимость
    router.callback_query.register(
        handle_agreement_cost_callback, F.data == 'cost_by_agreement', RequestCreatingStates.enter_cost
    )
    router.callback_query.register(handle_write_cost_callback, F.data == 'write_cost', RequestCreatingStates.enter_cost)
    router.message.register(handle_cost_message, RequestCreatingStates.enter_cost)

    # Условия оплаты
    router.callback_query.register(
        handle_payment_terms_callback, PaymentTermsCallback.filter(), RequestCreatingStates.enter_payment_terms
    )

    # Условия доставки (доставка / самовывоз)
    router.callback_query.register(
        handle_delivery_options_callback, DeliveryOptionCallback.filter(), RequestCreatingStates.enter_delivery_option
    )

    # Адрес
    router.message.register(handle_address_message, RequestCreatingStates.enter_address)

    # Ввод телефона
    router.message.register(handle_phone_number_message, RequestCreatingStates.enter_phone)

    # Ввод почты
    router.message.register(handle_email_message, RequestCreatingStates.enter_email)
    router.callback_query.register(
        handle_pass_email_empty_callback, F.data == 'pass_email_empty', RequestCreatingStates.enter_email
    )
