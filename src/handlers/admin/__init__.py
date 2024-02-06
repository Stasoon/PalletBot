from aiogram import Router

from .admin_menu import register_admin_menu_handlers
from .requests_approving import handle_requests_confirmation_handlers
from .statistic import register_admin_statistic_handlers
from .mailing import register_mailing_handlers


def register_admin_handlers(router: Router):
    register_admin_menu_handlers(router)
    register_admin_statistic_handlers(router)
    register_mailing_handlers(router)
    handle_requests_confirmation_handlers(router)
