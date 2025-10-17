

import json


def parse_file_ids(file_ids_data):
    if isinstance(file_ids_data, str):
        try:
            return json.loads(file_ids_data)
        except (json.JSONDecodeError, TypeError):
            return []
    return file_ids_data if file_ids_data else []