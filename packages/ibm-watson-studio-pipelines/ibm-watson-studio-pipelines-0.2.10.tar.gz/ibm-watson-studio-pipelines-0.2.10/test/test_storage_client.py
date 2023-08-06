from typing import Dict, Mapping

import requests
from ibm_cloud_sdk_core import DetailedResponse

from ibm_watson_studio_pipelines import WSPipelines
from ibm_watson_studio_pipelines.client import StorageClient


class InMemoryStorage(StorageClient):
    def __init__(self):
        self._fields: Dict[str, str] = {}

    def get_fields(self) -> Mapping[str, str]:
        return self._fields.copy()

    def _store_str_result(
            self,
            output_name: str,
            output_key: str,
            value: str,
    ) -> DetailedResponse:
        self._fields[output_key] = value
        response = requests.Response()
        response.request = requests.Request(
            method='PUT',
            url=output_key,
            headers={},
        )
        response.status_code = 202
        response.headers = {}
        return DetailedResponse(
            response=response,
            status_code=202,
        )

def test_00_result_serialization():
    apikey = ''
    client = WSPipelines(apikey)

    storage_client = InMemoryStorage()

    outputs = {
        'string': 'cos://0000000.xml',
        'int': 31415,
        'float': 3.1415,
        'array': ['cos://0000001.xml', 'cos://0000002.xml', 'cos://0000124.xml'],
        'dict': {
            'type': 'array',
            'value': ['a', 'b', 'c']
        },
    }
    outputs_artifacts = {
        el: f'path/to/{el}' for el in outputs.keys()
    }

    response = client._store_results_via_client(
        storage_client,
        outputs,
        outputs_artifacts,
    )
    assert response.status_code == 202
    assert storage_client.get_fields() == {
        'path/to/string': 'cos://0000000.xml',
        'path/to/int': '31415',
        'path/to/float': '3.1415',
        'path/to/array': '["cos://0000001.xml", "cos://0000002.xml", "cos://0000124.xml"]',
        'path/to/dict': '{"type": "array", "value": ["a", "b", "c"]}',
    }

def test_01_result_default_location():
    apikey = ''
    client = WSPipelines(apikey)

    storage_client = InMemoryStorage()

    outputs = {
        'string': 'cos://0000000.xml',
    }

    response = client._store_results_via_client(storage_client, outputs)
    assert response.status_code == 202
    assert storage_client.get_fields() == {
        '.ibm_watson_studio_pipelines/results/string': 'cos://0000000.xml',
    }
