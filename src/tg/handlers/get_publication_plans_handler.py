import logging
from telegram import Update
from telegram.ext import CallbackContext

from ...app_context import AppContext
from ...jobs.publication_plans_job import PublicationPlansJob
from ...strings import load
from .utils import manager_only, direct_message_only, reply

logger = logging.getLogger(__name__)

TASK_NAME = "get_publication_plans"


@manager_only
@direct_message_only
def get_publication_plans(update: Update, tg_context: CallbackContext) -> None:
    """
    Хендлер для команды получения отчета о планах публикаций.
    Использует FocalboardClient для получения данных.
    """
    logger.info("get_publication_plans: start")
    app_context = AppContext()

    try:
        # Отправляем статусное сообщение
        reply(load("publication_plans_generating"), update)
        logger.info("get_publication_plans: sent status message")

        # Функция для отправки сообщений через Telegram
        def send(text: str):
            reply(text, update)

        # Запускаем job для генерации отчета
        PublicationPlansJob._execute(
            app_context=app_context, send=send, called_from_handler=True
        )

        logger.info("get_publication_plans: report sent successfully")

    except Exception as e:
        logger.error("get_publication_plans: error %s", e, exc_info=True)
        reply(load("publication_plans_error"), update)


# Версия для Trello (если нужна обратная совместимость)
@manager_only
@direct_message_only
def get_publication_plans_trello(update: Update, tg_context: CallbackContext) -> None:
    """
    Версия хендлера для работы с Trello.
    """
    logger.info("get_publication_plans_trello: start")
    _get_publication_plans_base(update, tg_context, use_focalboard=False)


# Версия для Focalboard
@manager_only
@direct_message_only
def get_publication_plans_focalboard(
    update: Update, tg_context: CallbackContext
) -> None:
    """
    Версия хендлера для работы с Focalboard.
    """
    logger.info("get_publication_plans_focalboard: start")
    _get_publication_plans_base(update, tg_context, use_focalboard=True)


def _get_publication_plans_base(
    update: Update, tg_context: CallbackContext, use_focalboard: bool = True
) -> None:
    """
    Базовая функция для генерации отчета о планах публикаций.
    По аналогии с _get_task_report_base из get_tasks_report.py

    Args:
        update: Telegram update object
        tg_context: Telegram callback context
        use_focalboard: Если True, использует FocalboardClient, иначе TrelloClient
    """
    logger.info(
        "_get_publication_plans_base: start with use_focalboard=%s", use_focalboard
    )
    app_context = AppContext()

    try:
        # Отправляем статусное сообщение
        reply(load("publication_plans_generating"), update)
        logger.info("_get_publication_plans_base: sent status message")

        # Функция для отправки сообщений через Telegram
        def send(text: str):
            reply(text, update)

        # Запускаем job с нужным клиентом
        # TODO: если нужна поддержка TrelloClient, создать отдельный job или параметр
        PublicationPlansJob._execute(
            app_context=app_context, send=send, called_from_handler=True
        )

        logger.info(
            "_get_publication_plans_base: report sent successfully (focalboard=%s)",
            use_focalboard,
        )

    except Exception as e:
        logger.error(
            "_get_publication_plans_base: error %s (focalboard=%s)",
            e,
            use_focalboard,
            exc_info=True,
        )
        reply(load("publication_plans_error"), update)
