import logging
from typing import Callable

from ..app_context import AppContext
from ..consts import TrelloListAlias
from ..strings import load
from ..tg.sender import pretty_send
from .base_job import BaseJob
from .utils import format_errors

logger = logging.getLogger(__name__)


class PublicationPlansJob(BaseJob):
    @staticmethod
    def _execute(
        app_context: AppContext, send: Callable[[str], None], called_from_handler=False
    ):
        paragraphs = [load("publication_plans_job__intro")]  # list of paragraph strings
        errors = {}

        paragraphs += PublicationPlansJob._retrieve_cards_for_paragraph(
            trello_client=app_context.trello_client,
            title=load("publication_plans_job__title_publish_this_week"),
            list_aliases=(TrelloListAlias.PROOFREADING, TrelloListAlias.DONE),
            errors=errors,
            show_due=True,
            strict_archive_rules=True,
        )

        paragraphs += PublicationPlansJob._retrieve_cards_for_paragraph(
            trello_client=app_context.trello_client,
            title=load("common_report__section_title_editorial_board"),
            list_aliases=(
                TrelloListAlias.EDITED_NEXT_WEEK,
                TrelloListAlias.TO_SEO_EDITOR,
            ),
            errors=errors,
            show_due=False,
            need_illustrators=False,
            strict_archive_rules=False,
        )

        paragraphs.append(load("publication_plans_job__outro"))

        if len(errors) > 0:
            paragraphs = format_errors(errors)

        pretty_send(paragraphs, send)
