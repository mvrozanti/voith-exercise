import pytest
from unittest.mock import AsyncMock
from voith_exercise.services.timeseries_service import TimeseriesService
from voith_exercise.models.historical_data import HistoricalData

@pytest.fixture
def mock_repository():
    """Fixture to provide a mocked repository."""
    repository = AsyncMock()
    return repository


@pytest.fixture
def service(mock_repository):
    """Fixture to provide the TimeseriesService with a mocked repository."""
    return TimeseriesService(repository=mock_repository)


@pytest.mark.asyncio
async def test_get_filtered_data(service, mock_repository):
    """Test get_filtered_data with valid filters."""
    mock_repository.fetch_filtered_data.return_value = {
        "timestamps": ["2024-01-01T00:00:00", "2024-01-02T00:00:00"],
        "prices": [50000.0, 51000.0],
        "volumes": [1000.0, 1100.0],
    }

    coin_id = "bitcoin"
    filters = {
        "start_date": "2024-01-01",
        "end_date": "2024-01-02",
        "min_price": 100.0,
        "max_price": 100000.0,
        "min_volume": None,
        "max_volume": None,
    }

    result = await service.get_filtered_data(coin_id, filters)

    assert result["timestamps"] == ["2024-01-01T00:00:00", "2024-01-02T00:00:00"]
    assert result["prices"] == [50000.0, 51000.0]
    assert result["volumes"] == [1000.0, 1100.0]
    mock_repository.fetch_filtered_data.assert_awaited_once_with(coin_id, filters)


@pytest.mark.asyncio
async def test_get_filtered_data_no_results(service, mock_repository):
    """Test get_filtered_data with no matching results."""
    mock_repository.fetch_filtered_data.return_value = {
        "timestamps": [],
        "prices": [],
        "volumes": [],
    }

    coin_id = "unknown_coin"
    filters = {}

    result = await service.get_filtered_data(coin_id, filters)

    assert result["timestamps"] == []
    assert result["prices"] == []
    assert result["volumes"] == []
    mock_repository.fetch_filtered_data.assert_awaited_once_with(coin_id, filters)


@pytest.mark.asyncio
async def test_get_summary_stats(service, mock_repository):
    """Test get_summary_stats with valid date range."""
    mock_repository.fetch_summary_stats.return_value = {
        "avg_price": 50000.0,
        "total_volume": 10000.0,
    }

    coin_id = "bitcoin"
    start_date = "2024-01-01"
    end_date = "2024-01-04"

    result = await service.get_summary_stats(coin_id, start_date, end_date)

    assert result["summary"]["avg_price"] == 50000.0
    assert result["summary"]["total_volume"] == 10000.0
    mock_repository.fetch_summary_stats.assert_awaited_once_with(coin_id, start_date, end_date)


@pytest.mark.asyncio
async def test_get_summary_stats_no_data(service, mock_repository):
    """Test get_summary_stats with no matching results."""
    mock_repository.fetch_summary_stats.return_value = {}

    coin_id = "unknown_coin"
    start_date = "2024-01-01"
    end_date = "2024-01-04"

    result = await service.get_summary_stats(coin_id, start_date, end_date)

    assert result == {"summary": None}
    mock_repository.fetch_summary_stats.assert_awaited_once_with(coin_id, start_date, end_date)


@pytest.mark.asyncio
async def test_get_paginated_data(service, mock_repository):
    """Test get_paginated_data with valid pagination."""
    mock_repository.fetch_paginated_data.return_value = [
        HistoricalData(timestamp="2024-01-01T00:00:00", price=50000.0, volume=1000.0),
        HistoricalData(timestamp="2024-01-02T00:00:00", price=51000.0, volume=1100.0),
    ]

    coin_id = "bitcoin"
    limit = 2
    offset = 0

    result = await service.get_paginated_data(coin_id, limit, offset)

    assert result["timestamps"] == ["2024-01-01T00:00:00", "2024-01-02T00:00:00"]
    assert result["prices"] == [50000.0, 51000.0]
    assert result["volumes"] == [1000.0, 1100.0]
    mock_repository.fetch_paginated_data.assert_awaited_once_with(coin_id, limit, offset)


@pytest.mark.asyncio
async def test_get_paginated_data_invalid_params(service, mock_repository):
    """Test get_paginated_data with invalid parameters."""
    coin_id = "bitcoin"
    limit = 0
    offset = -1

    with pytest.raises(ValueError, match="Coin ID must be provided, limit > 0, and offset >= 0."):
        await service.get_paginated_data(coin_id, limit, offset)
