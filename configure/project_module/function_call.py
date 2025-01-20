from dateutil import parser
from django.utils.timezone import make_aware

def parse_date(date_value):
    if date_value:
        try:
            parsed_date = parser.parse(date_value)
            # Make the datetime timezone-aware
            if parsed_date.tzinfo is None:
                return make_aware(parsed_date)
            return parsed_date
        except Exception:
            return None  # Return None if parsing fails
