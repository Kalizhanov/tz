import datetime
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def export_statement(data) -> None:
    logger.info("Start exporting statement")
    df = pd.DataFrame([{
        "FROM_DATE": data.from_date.strftime("%Y-%m-%d"),
        "TO_DATE": data.to_date.strftime("%Y-%m-%d"),
        "STATEMENT_LANGUAGE": data.statement_language,
        "FULL_NAME": data.full_name,
        "FINANSIAL_INSTITUTION": data.financial_institution_name,
        "AMOUNT": detail.amount,
        "DETAILS": detail.details,
        "OPERATION_DATE": detail.operation_date.strftime("%Y-%m-%d"),
        "TRANSACTION_TYPE": detail.transaction_type,
        "INSERT_DATE": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "CARD_NUMBER": data.card_number,
        "ST_CREATION_DATE": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ST_MODIFIED_DATE": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ST_SUBJECT": "Банковская выписка",
        "ST_AUTHOR": "Галымжан",
        "ST_TITLE": "Банковская выписка",
        "ST_PRODUCER": "KaspiBank"
    } for detail in data.details])
    
    output_file = "kaspi_statement.xlsx"
    df.to_excel(output_file, index=False)
