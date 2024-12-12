# api/unit_tests/mongodb_connectors_test.py
# export PYTHONPATH=$(pwd)

# Lib
import pytest
import pytest_asyncio
from unittest.mock import patch, AsyncMock
from uuid import uuid4

from services.mongodb_connectors import get_mongodb_client, get_collection, request_user_locations, request_user_hives
from models.user_objects_base_models import Locations
from utils.exceptions import CustomException




# Ignore Pydantic Warnings
@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest_asyncio.fixture
async def mock_mongodb_client():
    with patch('services.mongodb_connectors.AsyncIOMotorClient', new_callable=AsyncMock) as mock_client:
        yield mock_client
        await mock_client.close()


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest_asyncio.fixture
async def mock_get_collection():
    with patch('services.mongodb_connectors.get_collection', new_callable=AsyncMock) as mock_collection:
        yield mock_collection


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.asyncio
async def test_get_mongodb_client_success(mock_mongodb_client):
    client = await get_mongodb_client()
    assert client is not None


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.asyncio
async def test_get_mongodb_client_failure():
    with patch('services.mongodb_connectors.AsyncIOMotorClient', side_effect=Exception("Connection error")):
        with pytest.raises(CustomException) as exc_info:
            await get_mongodb_client()
        assert exc_info.value.message == "Failed to connect to the MongoDB database: Connection error"


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.asyncio
async def test_get_collection_failure():
    with patch('services.mongodb_connectors.get_mongodb_client', side_effect=Exception("Connection error")):
        with pytest.raises(CustomException) as exc_info:
            await get_collection("test_collection")
        assert exc_info.value.message == "Failed to connect to the MongoDB database: Connection error"


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.asyncio
async def test_request_user_locations_post(mock_get_collection):
    location = Locations(owner=str(uuid4()), name="location1", latitude=0.0, longitude=0.0)
    result = await request_user_locations(user_id=str(uuid4()), method="POST", location=location)
    assert result == {"status": "success", "message": "Location added", "location": location.model_dump()}


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.asyncio
async def test_request_user_locations_put(mock_get_collection):
    location = Locations(owner=str(uuid4()), name="location1", latitude=0.0, longitude=0.0)
    result = await request_user_locations(user_id=str(uuid4()), method="PUT", location=location)
    assert result == {"status": "success", "message": "Location updated"}


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.asyncio
async def test_request_user_locations_delete(mock_get_collection):
    location = Locations(owner=str(uuid4()), name="location1", latitude=0.0, longitude=0.0)
    result = await request_user_locations(user_id=str(uuid4()), method="DELETE", location=location)
    assert result == {"status": "success", "message": "Location deleted"}