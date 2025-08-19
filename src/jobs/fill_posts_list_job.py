import logging
from typing import Callable

from ..app_context import AppContext
from ..consts import TrelloListAlias
from ..strings import load
from ..tg.sender import pretty_send
from .base_job import BaseJob
from .utils import format_errors

logger = logging.getLogger(__name__)


class FillPostsListJob(BaseJob):
    @staticmethod
    def _execute(
        app_context: AppContext, send: Callable[[str], None], called_from_handler=False
    ):
        errors = {}
        registry_posts = []
        all_rubrics = app_context.db_client.get_rubrics()

        registry_posts += FillPostsListJob._retrieve_cards_for_registry(
            trello_client=app_context.trello_client,
            list_aliases=[TrelloListAlias.PUBLISHED],
            all_rubrics=all_rubrics,
            errors=errors,
            show_due=True,
            strict_archive_rules=True,
        )

        if len(errors) == 0:
            posts_added = app_context.sheets_client.update_posts_registry(
                registry_posts
            )
            if len(posts_added) == 0:
                paragraphs = [load("fill_posts_list_job__unchanged")]
            else:
                paragraphs = [load("fill_posts_list_job__success")] + [
                    "\n".join(
                        f"{index + 1}) {post_name}"
                        for index, post_name in enumerate(posts_added)
                    )
                ]
        else:
            paragraphs = format_errors(errors)

        pretty_send(paragraphs, send)
