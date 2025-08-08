from pydantic import BaseModel

class ConsultaRequest(BaseModel):
    pergunta: str
    area: str = "previdenciario"
