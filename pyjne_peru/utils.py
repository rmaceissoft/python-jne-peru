from datetime import datetime, date
from typing import Optional


def parse_datetime(value: Optional[str], format="%d/%m/%Y %H:%M:%S") -> Optional[datetime]:
    if not value:
        return None
    return datetime.strptime(value.replace('.', ''), format)


def parse_date(value: Optional[str], format="%d/%m/%Y") -> Optional[date]:
    result = parse_datetime(value, format=format)
    if not result:
        return None
    return result.date()
