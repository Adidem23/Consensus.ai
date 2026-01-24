from DB.db import db

collection = db["AgentAnswers"]

async def create_document(data: dict) -> dict:
    result = await collection.insert_one(data)
    return {"inserted_id": str(result.inserted_id)}


async def read_document(filter: dict) -> dict | None:
    return await collection.find_one(filter)


async def read_all_documents(filter: dict = {}) -> list:
    cursor = collection.find(filter)
    return [doc async for doc in cursor]


async def update_document(filter: dict, update: dict) -> bool:
    result = await collection.update_one(filter, update)
    return result.modified_count > 0


async def delete_document(filter: dict) -> bool:
    result = await collection.delete_one(filter)
    return result.deleted_count > 0
