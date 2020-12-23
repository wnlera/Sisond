import json
from io import BytesIO

class CheckResults:
    def __init__(self, json_result: list, processed_file: BytesIO):
        self.processed_file = processed_file
        self._json_result = json_result

    def json_result(self, url):
        # todo: неудачно место сборки json
        json_result = {
            "results": self._json_result,
            "fileUrl": url
        }
        return json.dumps(json_result)

