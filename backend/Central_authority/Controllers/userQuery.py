import os
from fastapi import APIRouter
from Views.userQuery import AgentQueryObject
# from client_class import Agent_Client_Class
from Model.agentQuery import *

router=APIRouter(prefix="/agentquery")

@router.get("/")
def breathingMessage():
    return {"message":"Server is Up and Running!!"}

@router.post("/uploadRecord")
async def uploadRecordB(agentquery:AgentQueryObject):
    print(agentquery)
    first_query_object=agentquery
    await create_document(first_query_object.model_dump())
    return {"messgage":f'Record uploaded for the {agentquery.Agent_Node_name} with query {agentquery.query}'}

@router.post("/searchForOtherRecords")
async def searchOtherModelRecords(agentQuery:AgentQueryObject):
    records=await read_all_documents({
        "Agent_Node_name":{"$ne":f'{agentQuery.Agent_Node_name}'}
    })

    for record in records:
        record["_id"] = str(record["_id"])

    return records

@router.post("/updateCritique")
async def updateCritiques(agentQuery: AgentQueryObject):

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
