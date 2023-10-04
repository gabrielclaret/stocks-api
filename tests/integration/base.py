import logging
from datetime import timezone

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo.collection import Collection

from tests.integration.database import get_database as get_database_tests
from tests.integration.helper import (
    STOCK_METADATA,
    insert_document,
    serialize_csv,
    set_envs_for_tests,
)
from tests.integration.settings import get_settings as get_settings_tests

DEFAULT_TIMEZONE = timezone.utc


class BaseTest:
    """Class that defines base test."""

    def _setup_local_data(self, collection: Collection) -> None:
        """Insert local data for testing."""
        stock_metadata = serialize_csv(STOCK_METADATA)

        logging.info("inserting stocks...")
        for stock in stock_metadata:
            _stock = insert_document(collection, stock)

            logging.info(f"inserted stock with id [{_stock.id}]")

    def setup_class(self) -> None:
        """Class setup.

        Setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        set_envs_for_tests()
        self.settings = get_settings_tests()

        def _get_app() -> FastAPI:
            from api.config.settings import get_settings
            from api.dependencies.database import get_database
            from api.main import app

            app.dependency_overrides[get_settings] = get_settings_tests
            app.dependency_overrides[get_database] = get_database_tests

            return app

        self.app_client = TestClient(_get_app())

        self.database = get_database_tests()
        self.stocks_collection = self.database.get_collection("stocks")

        self.STOCK_SERIES_RENAMER = {
            "Date": "date",
            "Symbol": "symbol",
            "Series": "series",
            "Prev Close": "previous_close",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Last": "last",
            "Close": "close",
            "VWAP": "vwap",
            "Volume": "volume",
            "Turnover": "turnover",
            "Trades": "trades",
            "Deliverable Volume": "deliverable_volume",
            "%Deliverble": "deliverable_percent",
        }

    def setup_method(self) -> None:
        self._setup_local_data(self.stocks_collection)

    def teardown_method(self) -> None:
        """Teardown any state that was previously setup."""
        for collection in self.database.list_collection_names():
            self.database.drop_collection(collection)
