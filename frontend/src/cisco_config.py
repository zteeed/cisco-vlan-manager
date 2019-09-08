import json
from datetime import datetime
from typing import Dict, Optional

from config import INTERNAL_API_URL
from src import s


def get_content() -> Optional[Dict]:
    response = s.get(f'{INTERNAL_API_URL}/config')
    if response.status_code == 200:
        return json.loads(response.content)


def get_date(content: Optional[Dict]) -> str:
    if content is None:
        return ''
    date = content['time']
    date = datetime.strptime(date, "%m/%d/%Y %H:%M:%S")
    return date.strftime("%d-%m-%Y %H:%M:%S")
