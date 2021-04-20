from datetime import datetime, date
from typing import Optional


def parse_date(value: str, format="%d/%m/%Y") -> Optional[date]:
    if not value:
        return None
    return datetime.strptime(value, format).date()


def parse_datetime(value: str, format="%d/%m/%Y %H:%M:%S") -> Optional[datetime]:
    if not value:
        return None
    return datetime.strptime(value.replace('.', ''), format)
