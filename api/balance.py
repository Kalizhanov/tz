import base64
import pdfplumber

from fastapi import APIRouter
from io import BytesIO

from schemas.request import ParseRequestSchema
from schemas.response import ParseResponseSchema
from utils.export import export_statement
from utils.parse import parse_text

router = APIRouter()


@router.post("/api/v1/parse")
def parse_base64(request: ParseRequestSchema) -> ParseResponseSchema:

    try:
        data_bytes = base64.b64decode(request.base64_pdf)
        with pdfplumber.open(BytesIO(data_bytes)) as file:
            text = "".join(page.extract_text() for page in file.pages)

        data = parse_text(text)
        export_statement(data)

    except Exception as exc: 
        return ParseResponseSchema(success=False, msg=str(exc))

    return ParseResponseSchema(success=True, data=data)



@router.get("/api/v1/convert")
async def decode_base64():
    path = "/Users/kalizhanov/Desktop/ENG.pdf"

    with open(path, "rb") as file:
        content = file.read()
        encoded_content = base64.b64encode(content)
        encoded_string = encoded_content.decode("utf-8")

    return {"base64_pdf": encoded_string}
