from pydantic import BaseModel

class FeedbackRequest(BaseModel):
    pergunta: str
    resposta: str
    feedback: str
