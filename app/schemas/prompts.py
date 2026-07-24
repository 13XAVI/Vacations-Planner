from pydantic import BaseModel

class RegisterPrompt(BaseModel):
    name:str
    template:str
    commit_message:str
    
    
class  PromptParams(BaseModel):
    name:str
    version:str
class PromptResponse(BaseModel):
    name:str
    version:str