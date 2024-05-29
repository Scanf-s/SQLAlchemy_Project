import json
from datetime import date, timedelta
from decimal import Decimal


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, timedelta)):
            return str(obj)
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)