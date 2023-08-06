from typing import Any, Union

from pydantic import BaseModel
from pyntone.kintone_request_config_builder import HttpMethod
from pyntone.models import EndpointName, HttpMethod
from pyntone.models.field import UpdateKey


class UpdateRecord(BaseModel):
    key: Union[int, str, UpdateKey]
    revision: Union[int, str, None] = None
    record: dict[str, Any]
    
    def data(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            'record': { key: { 'value': val } for key, val in self.record.items() },
        }
        if self.revision is not None:
            data['revision'] = self.revision

        if type(self.key) is UpdateKey:
            data['updateKey'] = self.key.dict()
        else:
            data['id'] = self.key
        return data

class DeleteRecord(BaseModel):
    id: Union[int, str]
    revision: Union[int, str] = -1
