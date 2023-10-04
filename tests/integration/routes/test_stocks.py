import pandas as pd
from numpy import nan

from tests.integration.base import BaseTest


class TestStocksRoutes(BaseTest):
    """Test class to test event service."""

    def test_get_stocks__default_query_parameters__expected_success_default_response(  # noqa
        self,
    ) -> None:
        """Test to get stocks with default parameters."""
        # FIXTURE
        expected_first_stock = {
            "company_name": "Adani Ports and Special Economic Zone Ltd.",
            "industry": "SERVICES",
            "symbol": "ADANIPORTS",
            "series": "EQ",
            "isin_code": "INE742F01042",
            "file_format": "json",
            "created_at": "2023-10-04T00:00:00",
            "last_updated": "2023-10-04T00:00:00",
        }

        expected_last_stock = {
            "company_name": "Nestle India Ltd.",
            "industry": "CONSUMER GOODS",
            "symbol": "NESTLEIND",
            "series": "EQ",
            "isin_code": "INE239A01016",
            "file_format": "csv",
            "created_at": "2023-10-04T00:00:00",
            "last_updated": "2023-10-04T00:00:00",
        }
        # EXERCISE
        response = self.app_client.get("/api/v1/stocks")

        # ASSERT
        assert response.is_success

        stock_response = response.json()
        stocks = stock_response.get("stocks")

        assert len(stocks) == 6
        assert stock_response.get("total") == 6

        first_stock = stocks[0]
        del first_stock["id"]

        last_stock = stocks[-1]
        del last_stock["id"]

        assert first_stock == expected_first_stock
        assert last_stock == expected_last_stock

    def test_get_stocks__with_skip_limit_query_parameters__expected_success_with_limited_stocks(  # noqa
        self,
    ) -> None:
        """Test to get stocks.

        Query parameters with skip and limit.
        """
        # FIXTURE
        expected_first_stock = {
            "company_name": "Asian Paints Ltd.",
            "industry": "CONSUMER GOODS",
            "symbol": "ASIANPAINT",
            "series": "EQ",
            "isin_code": "INE021A01026",
            "file_format": "json",
            "created_at": "2023-10-04T00:00:00",
            "last_updated": "2023-10-04T00:00:00",
        }

        expected_last_stock = {
            "company_name": "Grasim Industries Ltd.",
            "industry": "CEMENT & CEMENT PRODUCTS",
            "symbol": "GRASIM",
            "series": "EQ",
            "isin_code": "INE047A01021",
            "file_format": "xlsx",
            "created_at": "2023-10-04T00:00:00",
            "last_updated": "2023-10-04T00:00:00",
        }

        # EXERCISE
        response = self.app_client.get("/api/v1/stocks?skip=1&limit=2")

        # ASSERT
        assert response.is_success

        stock_response = response.json()
        stocks = stock_response.get("stocks")

        assert len(stocks) == 2
        assert stock_response.get("total") == 6

        first_stock = stocks[0]
        del first_stock["id"]

        last_stock = stocks[-1]
        del last_stock["id"]

        assert first_stock == expected_first_stock
        assert last_stock == expected_last_stock

    def test_get_stocks__with_sort_by_descending_company_name_query_parameters__expected_success_descending_sort(  # noqa
        self,
    ) -> None:
        """Test to get stocks.

        Query parameters sort descending by 'company_name' field.
        """
        # FIXTURE
        expected_first_stock = {
            "company_name": "Nestle India Ltd.",
            "industry": "CONSUMER GOODS",
            "symbol": "NESTLEIND",
            "series": "EQ",
            "isin_code": "INE239A01016",
            "file_format": "csv",
            "created_at": "2023-10-04T00:00:00",
            "last_updated": "2023-10-04T00:00:00",
        }

        expected_last_stock = {
            "company_name": "Adani Ports and Special Economic Zone Ltd.",
            "industry": "SERVICES",
            "symbol": "ADANIPORTS",
            "series": "EQ",
            "isin_code": "INE742F01042",
            "file_format": "json",
            "created_at": "2023-10-04T00:00:00",
            "last_updated": "2023-10-04T00:00:00",
        }

        # EXERCISE
        response = self.app_client.get("/api/v1/stocks?sort=-company_name")

        # ASSERT
        assert response.is_success

        stock_response = response.json()
        stocks = stock_response.get("stocks")

        assert len(stocks) == 6
        assert stock_response.get("total") == 6

        first_stock = stocks[0]
        del first_stock["id"]

        last_stock = stocks[-1]
        del last_stock["id"]

        assert first_stock == expected_first_stock
        assert last_stock == expected_last_stock

    def test_get_stocks__with_sort_by_ascending_symbol_and_limit_skip_query_parameters__expected_success_ascending_sort(  # noqa
        self,
    ) -> None:
        """Test to get stocks.

        Query parameters sort ascending 'symbol' field, skip and limit.
        """
        # FIXTURE
        expected_first_stock = {
            "company_name": "Grasim Industries Ltd.",
            "industry": "CEMENT & CEMENT PRODUCTS",
            "symbol": "GRASIM",
            "series": "EQ",
            "isin_code": "INE047A01021",
            "file_format": "xlsx",
            "created_at": "2023-10-04T00:00:00",
            "last_updated": "2023-10-04T00:00:00",
        }

        expected_last_stock = {
            "company_name": "HCL Technologies Ltd.",
            "industry": "IT",
            "symbol": "HCLTECH",
            "series": "EQ",
            "isin_code": "INE860A01027",
            "file_format": "xlsx",
            "created_at": "2023-10-04T00:00:00",
            "last_updated": "2023-10-04T00:00:00",
        }

        # EXERCISE
        response = self.app_client.get(
            "/api/v1/stocks?skip=2&limit=2&sort=symbol"
        )

        # ASSERT
        assert response.is_success

        stock_response = response.json()
        stocks = stock_response.get("stocks")

        assert len(stocks) == 2
        assert stock_response.get("total") == 6

        first_stock = stocks[0]
        del first_stock["id"]

        last_stock = stocks[-1]
        del last_stock["id"]

        assert first_stock == expected_first_stock
        assert last_stock == expected_last_stock

    def test_get_stock_data__list_stocks_and_call_get_by_id__expected_success(  # noqa
        self,
    ) -> None:
        """Test to get stock by id."""
        # FIXTURE
        expected_stock = {
            "company_name": "Nestle India Ltd.",
            "industry": "CONSUMER GOODS",
            "symbol": "NESTLEIND",
            "series": "EQ",
            "isin_code": "INE239A01016",
            "file_format": "csv",
            "created_at": "2023-10-04T00:00:00",
            "last_updated": "2023-10-04T00:00:00",
        }

        expected_time_series = (
            pd.read_csv(
                "tests/integration/data/stocks-bucket/csv/NESTLEIND.csv"
            )
            .replace({nan: None})
            .rename(columns=self.STOCK_SERIES_RENAMER)
        )
        expected_time_series["date"] = pd.to_datetime(
            expected_time_series["date"]
        ).dt.strftime("%Y-%m-%dT%H:%M:%S")
        expected_time_series = expected_time_series.to_dict(orient="list")

        # EXERCISE
        response = self.app_client.get("/api/v1/stocks?sort=-company_name")
        list_stock_response = response.json()
        stocks = list_stock_response.get("stocks")
        stock = stocks[0]

        stock_id = stock.get("id")
        get_stock_response = self.app_client.get(f"/api/v1/stocks/{stock_id}")
        stock_data = get_stock_response.json()

        # ASSERT
        assert get_stock_response.is_success

        stock_time_series = stock_data.get("time_series")

        assert stock_data.get("company_name") == expected_stock["company_name"]
        assert stock_data.get("industry") == expected_stock["industry"]
        assert stock_data.get("symbol") == expected_stock["symbol"]
        assert stock_data.get("isin_code") == expected_stock["isin_code"]
        assert stock_data.get("file_format") == expected_stock["file_format"]
        assert stock_time_series == expected_time_series
