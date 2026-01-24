from pydantic import BaseModel
from typing_extensions import Annotated 
import operator

class critiqueClass(BaseModel):
    Agent_Node_name:str | None
    Critique : str | None

class AgentQueryObject(BaseModel):
    Agent_Node_name:str | None
    query : str | None
    Agent_first_Output : str | None
    final_output : str | None
    Critiques : Annotated[list[critiqueClass],operator.add]