from json import JSONDecodeError
from typing import Dict, Type, Optional, Any, Literal

import httpx
from pydantic import BaseModel
from core.api.models import _Unset

from core.api.endpoint import Endpoint


class ApiClient:
    def __init__(
            self,
            base_url: str,
            headers: Dict[str, str]
    ):
        self.base_url = base_url

        self.client = httpx.AsyncClient(
            headers=headers,
            timeout=30.0,
            follow_redirects=True,
        )
        self.endpoints: Dict[str, Endpoint] = {}

    def register_endpoint(
            self,
            path: str,
            name: str = None,
            method: Literal["GET", "POST", "DELETE", "PATCH"] = 'POST',
            *,
            body_validator: Optional[Type[BaseModel]] = None,
            query_validator: Optional[Type[BaseModel]] = None,
            response_validator: Optional[Type[BaseModel]] = None,
    ):
        if name is None:
            name = path.split("/")[-1]
        if name in self.endpoints:
            raise ValueError(f"Endpoint with name '{name}' already exists.")
        if method == "GET" and body_validator is not None:
            raise ValueError(
                "Method 'GET' cannot be used with body validator, as GET method doesn't have request body."
            )
        self.endpoints[name] = Endpoint(path, body_validator, query_validator, response_validator, method)

    def request(self, endpoint: Endpoint):
        async def _request(
                body: Optional[dict] = None,
                query_params: Optional[dict] = None,
                headers: Optional[dict] = None,
                **kwargs: Any,
        ) -> Any:
            validated_data = endpoint.validate_input_data(body, query_params)
            query_params: dict = validated_data.get('params')

            path = endpoint.path

            if query_params:
                pk = query_params.pop('pk', None)
                if "{id}" in path:
                    if isinstance(pk, int):
                        path = path.replace("{id}", str(pk))
                    else:
                        raise ValueError(f"Invalid pk parameter type. Expected int but got '{type(pk)}'")

                query_params = {key: val for key, val in query_params.items() if val != _Unset}

            url = f"{self.base_url}/{path}"

            final_headers = {**self.client.headers, **(headers or {})}
            data = validated_data.get("data")
            if isinstance(data, dict):
                data = {key: val for key, val in validated_data.get("data").items() if val != _Unset}

            response = await self.client.request(
                method=endpoint.method,
                url=url,
                data=data,
                params=query_params,
                headers=final_headers,
                **kwargs,
            )

            response.raise_for_status()

            try:
                response = response.json()
            except JSONDecodeError:
                response = {}

            validated_response = endpoint.validate_output_data(response)

            return validated_response

        return _request

    def __getattr__(self, name: str):
        if name in self.endpoints:
            endpoint = self.endpoints[name]
            return self.request(endpoint)
        return getattr(self.obj, name)
