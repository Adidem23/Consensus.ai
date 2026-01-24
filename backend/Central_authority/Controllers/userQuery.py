import os
from fastapi import APIRouter
from Views.userQuery import AgentQueryObject
from client_class import Agent_Client_Class
from Model.agentQuery import *

router=APIRouter(prefix="/agentquery")

@router.get("/")
def breathingMessage():
    return {"message":"Server is Up and Running!!"}

@router.post("/uploadRecord")
async def uploadRecordB(agentquery:AgentQueryObject):
    print(agentquery)
    first_query_object=agentquery
    await create_document(first_query_object)
    return {"messgage":f'Record uploaded for the {agentquery.Agent_Node_name} with query {agentquery.query}'}
