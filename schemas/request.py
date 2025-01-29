from pydantic import BaseModel


class ParseRequestSchema(BaseModel):
    base64_pdf: str
