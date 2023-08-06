import json
from flask import Response
from resp_builder.inmutables import _DictKey
from resp_builder.config import _name_file_codes
from resp_builder.config import _default_mimetype
from resp_builder.config import _default_response
from resp_builder.config import _default_status_code
from resp_builder.interfaces import ResponseBuilderInterface as Rbi


class ResponseBuilder(Rbi):
    _codes: dict

    def __init__(self):
        self._codes = self._file_to_dict()

    def __file_to_dict(self) -> dict:
        file = open(_name_file_codes)
        return json.load(file)

    def _get_data_from_code(self, code: str):
        if code is None:
            raise Exception
        json_data: dict = self._codes.get(code)
        if json_data is None:
            return _default_response
        return json_data

    def response(
            self,
            data: dict = {},
            status_code: int = _default_status_code,
            extradata: dict = {},
            is_merge: bool = True,
            mimetype: str = _default_mimetype
    ):
        if not data and not extradata and is_merge:
            data = data | extradata
        else:
            data['data'] = extradata

        if data is None:
            return Response(json.dumps(_default_response), status=status_code)
        return Response(json.dumps(data), status=status_code, mimetype=mimetype)
