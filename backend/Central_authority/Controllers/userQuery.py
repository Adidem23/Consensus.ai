import asyncio
from collections import defaultdict
from fastapi import APIRouter
from Views.userQuery import AgentQueryObject
from Model.agentQuery import *

router = APIRouter(prefix="/agentquery")

agent_locks = defaultdict(asyncio.Lock)

@router.get("/")
async def breathingMessage():
    return {"message": "Server is Up and Running!!"}


@router.post("/uploadRecord")
async def uploadRecordB(agentquery: AgentQueryObject):
    lock = agent_locks[agentquery.Agent_Node_name]

    async with lock:
        await create_document(agentquery.model_dump())

        return {
            "message": f"Record uploaded for {agentquery.Agent_Node_name} with query {agentquery.query}"
        }


@router.post("/searchForOtherRecords")
async def searchOtherModelRecords(agentQuery: AgentQueryObject):
    lock = agent_locks[agentQuery.Agent_Node_name]

    async with lock:
        records = await read_all_documents({
            "Agent_Node_name": {"$ne": agentQuery.Agent_Node_name}
        })

        for record in records:
            record["_id"] = str(record["_id"])

        return records


@router.post("/updateCritique")
async def updateCritiques(agentQuery: AgentQueryObject):
    lock = agent_locks[agentQuery.Agent_Node_name]

    async with lock:
        critiques_as_dicts = [
            critique.model_dump()
            for critique in agentQuery.Critiques
        ]

        await update_document(
            {"Agent_Node_name": agentQuery.Agent_Node_name},
            {
                "$push": {
                    "Critiques": {
                        "$each": critiques_as_dicts
                    }
                }
            }
        )

    return {"message": "Critiques updated successfully"}