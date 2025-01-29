import datetime
import logging
import re

from decimal import Decimal

from schemas.response import DetailSchema, DataSchema, Metrics
from utils.enum import Language, FinInstitution

logger = logging.getLogger(__name__)


def detect_language(line: str, splited_text: list) -> tuple:
    logger.info("Start detecting language")
    change_place = splited_text[4].split(" ")
    full_name = f"{change_place[0]} {splited_text[2]} {change_place[1]}"

    if line in "Kaspi Gold":
        return (
            Language.ENG.value, 
            r"Card number: (\*\d+)",
            r"Account number: (\S+)",
            r"from (\d{2}\.\d{2}\.\d{2}) to (\d{2}\.\d{2}\.\d{2})",
            "Date Amount Transaction Details",
            splited_text[2],
        )
    elif "ВЫПИСКА" in line:
        return (
            Language.RUS.value,
            r"Номер карты: (\*\d+)",
            r"Номер счета: (\S+)",
            r"с (\d{2}\.\d{2}\.\d{2}) по (\d{2}\.\d{2}\.\d{2})",
            "Дата Сумма Операция Детали",
            full_name,
        )

    return (
        Language.KAZ.value,
        r"Карта нөмірі: (\*\d+)",
        r"Шот нөмірі: (\S+)",
        r"(\d{2}\.\d{2}\.\d{2})ж\. бастап (\d{2}\.\d{2}\.\d{2})ж\. дейінгі",
        "Күні Сомасы Операция Толығырақ",
        full_name,
    )


def extract_transactions(text: list[str]) -> list[DetailSchema]:
    logger.info("Start extracting transactions")
    transactions = []
    pattern = r"(\d{2}\.\d{2}\.\d{2})\s+[+-]\s+([\d\s]+,\d{2})\s+₸\s+(.+?)\s+([A-Za-z0-9].*)"

    for line in text:
        
        found = re.search(pattern, line)
        if found is None:
            continue

        date_str, amount_str, transaction_type, details = found.group(1), found.group(2), found.group(3), found.group(4)
        operation_date = datetime.datetime.strptime(date_str, "%d.%m.%y").date()
        amount = Decimal(amount_str.replace(" ", "").replace(",", "."))

        transactions.append(DetailSchema(
            amount=amount,
            operation_date=operation_date,
            transaction_type=transaction_type,
            details=details
        ))

    return transactions


def parse_text(text: str) -> DataSchema:
    logger.info("Parsing of the file")
    splited_text = text.splitlines()

    lang, card_pattern, account_pattern, date_pattern, element, full_name = detect_language(splited_text[0], splited_text)

    card_match = re.search(card_pattern, text)
    account_match = re.search(account_pattern, text)
    card_number = card_match.group(1) if card_match else ""
    number_account = account_match.group(1) if account_match else ""

    date_match = re.search(date_pattern, text)
    if date_match:
        from_date = datetime.datetime.strptime(date_match.group(1), "%d.%m.%y").date()
        to_date = datetime.datetime.strptime(date_match.group(2), "%d.%m.%y").date()
    else:
        from_date = None
        to_date = None
    
    ind = splited_text.index(element)
    transactions = extract_transactions(splited_text[ind+1:])

    avg_sum = sum(t.amount for t in transactions) / len(transactions) if transactions else Decimal(0)

    splited_name = full_name.split()

    data = {
        "financialInstitutionName": FinInstitution.KASPI,
        "cardNumber": card_number,
        "fromDate": from_date,
        "toDate": to_date,
        "details": transactions,
        "metrics": Metrics(
            from_date=datetime.datetime.combine(from_date, datetime.time.min) if from_date else None,
            to_date=datetime.datetime.combine(to_date, datetime.time.min) if to_date else None,
            statement_language=lang,
            name=splited_name[0],
            surname=splited_name[1],
            patronymic=splited_name[2] if len(splited_name) == 3 else "",
            full_name=full_name,
            fin_institut=FinInstitution.KASPI,
            card_number=card_number,
            number_account=number_account,
            avg_sum=avg_sum,
        ),
        "statementLanguage": lang,
        "fullName": full_name,
    }

    return DataSchema(**data)
