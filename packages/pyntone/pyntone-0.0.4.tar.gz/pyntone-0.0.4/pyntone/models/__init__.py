from enum import Enum
from typing import Any, TypeVar, Union

from pydantic import BaseModel
from pyntone.models.base import KintoneBaseModel

RecordModelT = TypeVar('RecordModelT', bound=KintoneBaseModel)

class HttpMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'

class EndpointName(Enum):
    RECORD = 'record'
    RECORDS = 'records'
    RECORD_STATUS = 'record/status'
    RECORDS_STATUS = 'records/status'
    RECORD_ASSIGNEES = 'record/assignees'

class KintoneRequest(BaseModel):
    method: HttpMethod
    endpoint_name: EndpointName
    payload: dict[str, Any]

class KintoneRequestParams(BaseModel):
    url_params: dict[str, Any] = {}
    data: dict[str, Any] = {}

class App(BaseModel):
    app: Union[int, str]
    revision: Union[int, str]