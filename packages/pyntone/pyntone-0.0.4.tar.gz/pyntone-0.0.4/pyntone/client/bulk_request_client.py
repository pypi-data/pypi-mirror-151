from typing import Union

from pyntone.http.http_client import HttpClent
from pyntone.models import KintoneRequest, KintoneRequestParams
from pyntone.url import build_path


class BulkRequestClient:
    def __init__(self, http_client: HttpClent, guest_space_id: Union[int, str, None] = None) -> None:
        self.http_client = http_client
        self.guest_space_id = guest_space_id
        self.REQUESTS_LENGTH_LIMIT = 20
    
    def send(self, requests: list[KintoneRequest]):
        reqs = [
            {
                'method': req.method.value,
                'api': self._build_path_with_guest_space_id(req.endpoint_name.value),
                'payload': req.payload
            } for req in requests
        ]
        params = KintoneRequestParams(
            data={ 'requests': reqs }
        )
        path = self._build_path_with_guest_space_id('bulkRequest')
        return self.http_client.post(path, params)
    
    def _build_path_with_guest_space_id(self, endpoint_name: str) -> str:
        return build_path(endpoint=endpoint_name, guest_space_id=self.guest_space_id)
