from typing import Generic, Type, Union

from pyntone.client.app_client import AppClient
from pyntone.client.bulk_request_client import BulkRequestClient
from pyntone.client.record_client import RecordClient
from pyntone.http.http_client import HttpClent
from pyntone.kintone_request_config_builder import KintoneRequestConfigBuilder
from pyntone.models import KintoneRequest
from pyntone.models.auth import DiscriminatedAuth
from pyntone.models import RecordModelT


class KintoneRestAPIClient(Generic[RecordModelT]):
    def __init__(self, model: Type[RecordModelT], domain: str, auth: DiscriminatedAuth, default_app_id: Union[int, str, None] = None, guest_space_id: Union[None, int, str] = None):
        url = f'https://{domain}.cybozu.com'
        
        config_builder = KintoneRequestConfigBuilder(auth=auth, base_url=url)
        http_client = HttpClent(config_builder=config_builder)
        
        self.app = AppClient(model=model, http_client=http_client, default_app_id=default_app_id, guest_space_id=guest_space_id)
        self.record = RecordClient(model=model, http_client=http_client, default_app_id=default_app_id, guest_space_id=guest_space_id)
        self.__bulk_request = BulkRequestClient(http_client=http_client, guest_space_id=guest_space_id)

    def bulkRequest(self, params:list[KintoneRequest]):
        return self.__bulk_request.send(params)
