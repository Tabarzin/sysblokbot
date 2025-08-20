import json
import os
from typing import Dict, List

import pytest
from deepdiff import DeepDiff
from utils.json_loader import JsonLoader

from src.config_manager import ConfigManager
from src.db.db_client import DBClient
from src.drive.drive_client import GoogleDriveClient
from src.sheets.sheets_client import GoogleSheetsClient
from src.strings import StringsDBClient
from src.tg.sender import TelegramSender

ROOT_TEST_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_TEST_DIR = os.path.join(ROOT_TEST_DIR, "static")
SHEETS_TEST_DIR = os.path.join(STATIC_TEST_DIR, "sheets")
TRELLO_TEST_DIR = os.path.join(STATIC_TEST_DIR, "trello")

CONFIG_PATH = os.path.join(STATIC_TEST_DIR, "config.json")
CONFIG_OVERRIDE_PATH = os.path.join(STATIC_TEST_DIR, "config_override.json")


@pytest.fixture
def mock_config_manager(monkeypatch):
    config_manager = ConfigManager(CONFIG_PATH, CONFIG_OVERRIDE_PATH)
    config_manager.load_config_with_override()
    return config_manager


@pytest.fixture
def mock_config_jobs_manager(monkeypatch):
    config_manager = ConfigManager(CONFIG_PATH, CONFIG_OVERRIDE_PATH)
    return config_manager


@pytest.fixture
def mock_sheets_client(monkeypatch, mock_config_manager):
    def _authorize(self):
        pass

    # def _parse_gs_res(_, title_key_map: Dict, sheet_key: str, sheet_name: str = '') -> List[Dict]:

    #     load_json = JsonLoader(SHEETS_TEST_DIR).load_json

    #     if sheet_key == 'authors_sheet_key':
    #         return load_json('authors.json')
    #     elif sheet_key == 'curators_sheet_key':
    #         return load_json('curators.json')
    #     elif sheet_key == 'rubrics_registry_sheet_key':
    #         return load_json('rubrics.json')
    #     elif sheet_key == 'strings_sheet_key':
    #         return load_json('strings.json')

    monkeypatch.setattr(GoogleSheetsClient, "_authorize", _authorize)
    # monkeypatch.setattr(GoogleSheetsClient, '_parse_gs_res', _parse_gs_res)

    return GoogleSheetsClient(sheets_config=mock_config_manager.get_sheets_config())


@pytest.fixture
def mock_drive_client(monkeypatch, mock_config_manager):
    def _authorize(self):
        pass

    def _create_file(self, name: str, description: str, parents: List[str]) -> str:
        pass

    def _lookup_file_by_name(self, name: str) -> str:
        pass

    monkeypatch.setattr(GoogleDriveClient, "_authorize", _authorize)
    monkeypatch.setattr(GoogleDriveClient, "_create_file", _create_file)
    monkeypatch.setattr(GoogleDriveClient, "_lookup_file_by_name", _lookup_file_by_name)

    return GoogleDriveClient(drive_config=mock_config_manager.get_drive_config())


@pytest.fixture
def mock_telegram_bot(monkeypatch, mock_config_manager):
    return {}


@pytest.fixture
def mock_sender(monkeypatch, mock_config_manager, mock_telegram_bot):
    def send_to_chat_id(self, message_text: str, chat_id: int, **kwargs):
        pass

    monkeypatch.setattr(TelegramSender, "send_to_chat_id", send_to_chat_id)

    return TelegramSender(
        bot=mock_telegram_bot, tg_config=mock_config_manager.get_telegram_config()
    )


@pytest.fixture
def mock_db_client(mock_config_manager):
    return DBClient(db_config=mock_config_manager.get_db_config())


@pytest.fixture
def mock_strings_db_client(mock_config_manager):
    return StringsDBClient(
        strings_db_config=mock_config_manager.get_strings_db_config()
    )
