from motor.motor_asyncio import AsyncIOMotorClient

from gateway.core.settings import get_settings


def create_mongo_client() -> AsyncIOMotorClient:
    s = get_settings()
    return AsyncIOMotorClient(s.mongo_url)


def get_collection(client: AsyncIOMotorClient):
    s = get_settings()
    return client[s.mongo_db][s.mongo_coll]
