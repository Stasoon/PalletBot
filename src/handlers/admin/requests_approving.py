from aiogram import Bot, Router, F
from aiogram.types import InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database.models import PostRequest, PostPublication
from src.misc.callback_factories import PostRequestValidationCallback
from config import PUBLICATION_CHANNEL_ID, APPROVING_CHANNEL_ID, PUBLICATION_CHAT_ID
from src.misc.enums import UsageStatus, DealType


def replace_spaces_to_dashes(s: str) -> str:
    return s.replace(', ', '_').replace(' ', '_')


def get_approve_or_deny_post(post: PostRequest) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='✅', callback_data=PostRequestValidationCallback(confirm='True', request_id=post.number))
    builder.button(text='❌', callback_data=PostRequestValidationCallback(confirm='False', request_id=post.number))
    return builder.as_markup()


def get_post_text(post: PostRequest, replace_contacts_by_link: str = None) -> str:
    cost_text = '#Договорная' if not post.cost else post.cost

    if replace_contacts_by_link:
        contacts_text = f'<a href="{replace_contacts_by_link}">Контакты</a>'
    else:
        contacts_text = f'<b>☎ Контакты:</b> {post.phone_number}'
        contacts_text += f' \n<b>✉ Почта:</b> {post.email}' if post.email else ''

    usage_status = 'Новые' if post.usage_status == UsageStatus.NEW else 'БУ'
    product_type = replace_spaces_to_dashes(post.product_type)

    return (
        f"<b>#{'Хочу_купить' if post.deal_type == DealType.BUY else 'Хочу_продать'}</b> \n\n"
        f"<b>📝 Наименование:</b> #{product_type} \n"
        f"<b>Вид:</b> {post.material} \n"
        f"<b>Размер:</b> #{post.size} \n"
        f"<b>Сорт:</b> #{post.sort} \n"
        f"<b>Состояние:</b> #{usage_status} \n"
        f"<b>Цена:</b> {cost_text} \n"
        f"<b>Условие оплаты:</b> {post.payment_terms} \n"
        f"<b>🚛 Условие поставки:</b> {post.delivery_option} \n"
        f"<b>📍 Адрес:</b> {post.address} \n"
        f"{contacts_text}"
    )


async def send_post_to_admins_approving(bot: Bot, post: PostRequest):
    text = get_post_text(post=post)
    markup = get_approve_or_deny_post(post=post)

    await bot.send_message(chat_id=APPROVING_CHANNEL_ID, text=text, reply_markup=markup)


async def handle_confirm_request(callback: CallbackQuery, callback_data: PostRequestValidationCallback):
    await callback.message.edit_text(text=f"{callback.message.html_text} \n\n✅ Опубликовано")

    post = PostRequest.get(number=callback_data.request_id)
    publication, is_created = PostPublication.get_or_create(post=post)
    if not is_created:
        return

    post_text = get_post_text(post=post)

    channel_url = 'https://t.me/pallettender'
    footer_text = (
        f'<b>🕵️‍♂️Найти,что хочу продать/купить🔍</b> \n'
        f'     #{replace_spaces_to_dashes(post.product_type)} \n\n'
        
        f'<b>Хочу участвовать в <a href="{channel_url}">PalletPrice | Тендер</a></b>'
    )

    # <b>Заявка №{publication.number}</b> \n\n
    channel_text = f"{post_text} \n\n{footer_text}"
    await callback.bot.send_message(chat_id=PUBLICATION_CHANNEL_ID, text=channel_text)

    # post_text = get_post_text(post=post, replace_contacts_by_link=channel_msg.get_url())
    # channel_text = f"<b>Заявка №{publication.number}</b> \n\n{post_text} \n\n{footer_text}"
    # await callback.bot.send_message(chat_id=PUBLICATION_CHAT_ID, text=channel_text)


async def handle_deny_request(callback: CallbackQuery):
    await callback.message.edit_text(text=f"{callback.message.html_text} \n\n❌ Отклонено")


def handle_requests_confirmation_handlers(router: Router):
    router.callback_query.register(handle_confirm_request, PostRequestValidationCallback.filter(F.confirm == 'True'))
    router.callback_query.register(handle_deny_request, PostRequestValidationCallback.filter(F.confirm == 'False'))

