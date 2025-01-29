import datetime

from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

from utils.enum import FinInstitution


def to_camel(string: str) -> str:
    camel_case = ""
    for idx, word in enumerate(string.split("_")):
        if idx == 0:
            camel_case += word
            continue
        camel_case += word.capitalize()
    return camel_case


class CammelCaseModel(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True 


class DetailSchema(CammelCaseModel):
    amount: Decimal
    operation_date: datetime.date
    transaction_type: str
    details: str


class Metrics(BaseModel):
    from_date: datetime.datetime
    to_date: datetime.datetime
    statement_language: str
    name: str
    surname: str
    patronymic: Optional[str]
    full_name: str
    fin_institut: str = FinInstitution.KASPI
    card_number: str
    number_account: str
    avg_sum: Decimal


class DataSchema(CammelCaseModel):
    financial_institution_name: str = FinInstitution.KASPI
    card_number: str
    from_date: datetime.date
    to_date: datetime.date
    details: list[DetailSchema]
    metrics: Metrics
    statement_language: str
    full_name: str


class ParseResponseSchema(CammelCaseModel):
    success: bool
    msg: Optional[str] = None
    msg_type: Optional[str] = None
    data: Optional[DataSchema] = None
