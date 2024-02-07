from aiogram import Bot, Router, F
from aiogram.types import InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database.models import PostRequest, PostPublication
from src.misc.callback_factories import PostRequestValidationCallback
from config import PUBLICATION_CHANNEL_ID, APPROVING_CHANNEL_ID
from src.misc.enums import UsageStatus


def get_approve_or_deny_post(post: PostRequest) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='✅', callback_data=PostRequestValidationCallback(confirm='True', request_id=post.number))
    builder.button(text='❌', callback_data=PostRequestValidationCallback(confirm='False', request_id=post.number))
    return builder.as_markup()


async def get_post_text(bot: Bot, post: PostRequest) -> str:
    cost_text = '#Договорная' if not post.cost else post.cost

    contacts_text = f'<b>Контакты:</b> {post.phone_number}'
    contacts_text += f' \n<b>Почта:</b> {post.email}' if post.email else ''
    if not (await bot.get_chat(chat_id=post.user.telegram_id)).has_private_forwards:
        contacts_text += f' \n<b>Телеграм:</b> <a href="tg://user?id={post.user.telegram_id}">{post.user.name}</a>'

    usage_status = 'Новый_поддон' if post.usage_status == UsageStatus.NEW else 'БУ_поддон'

    return (
        f"<b>Сделка:</b> #{post.deal_type} \n"
        f"<b>Наименование:</b> #{usage_status} \n"
        f"<b>Размер:</b> #{post.size} \n"
        f"<b>Сорт:</b> #{post.sort} \n"
        f"<b>Цена:</b> {cost_text} \n"
        f"<b>Условие оплаты:</b> {post.payment_terms} \n"
        f"<b>Условие поставки:</b> {post.delivery_option} \n"
        f"<b>Адрес:</b> {post.address} \n"
        f"{contacts_text}"
    )


async def send_post_to_admins_approving(bot: Bot, post: PostRequest):
    text = await get_post_text(bot=bot, post=post)
    markup = get_approve_or_deny_post(post=post)

    await bot.send_message(chat_id=APPROVING_CHANNEL_ID, text=text, reply_markup=markup)


async def handle_deny_request(callback: CallbackQuery):
    await callback.message.edit_text(text=f"{callback.message.html_text} \n\n❌ Отклонено")


async def handle_confirm_request(callback: CallbackQuery, callback_data: PostRequestValidationCallback):
    await callback.message.edit_text(text=f"{callback.message.html_text} \n\n✅ Опубликовано")

    post = PostRequest.get(number=callback_data.request_id)
    publication, is_created = PostPublication.get_or_create(post=post)
    if not is_created:
        return

    post_text = await get_post_text(bot=callback.bot, post=post)
    channel_url = 'https://t.me/palletprice'
    footer_text = (
        '<b>Будьте внимательны, перед сделкой самостоятельно проверяйте:</b> \n\n'
        '- участника сделки \n'
        '- условия сделки \n'
        '- ТУ товара \n\n'
        f'<b>Биржа <a href="{channel_url}">PalletPrice</a></b>'
    )
    text = f"<b>Заявка №{publication.number}</b> \n\n{post_text} \n\n{footer_text}"

    await callback.bot.send_message(chat_id=PUBLICATION_CHANNEL_ID, text=text)


def handle_requests_confirmation_handlers(router: Router):
    router.callback_query.register(handle_confirm_request, PostRequestValidationCallback.filter(F.confirm == 'True'))
    router.callback_query.register(handle_deny_request, PostRequestValidationCallback.filter(F.confirm == 'False'))
