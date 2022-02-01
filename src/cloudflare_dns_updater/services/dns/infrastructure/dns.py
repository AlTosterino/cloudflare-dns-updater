import asyncio
from typing import Collection, Optional

import attr
import httpx
from loguru import logger

from cloudflare_dns_updater.services.dns.dtos.update import UpdateDNSRecordDto
from cloudflare_dns_updater.services.dns.infrastructure.serializers.zone import (
    RecordsSerializer,
    UpdateRecordSerializer,
)
from cloudflare_dns_updater.services.dns.interfaces.dns import DNSService
from cloudflare_dns_updater.services.dns.value_objects import ZoneID
from cloudflare_dns_updater.services.dns.value_objects.record import DNSRecords

# TODO: Handle API Errors


class CloudflareService(DNSService):
    async def get_dns_records(self, zone_id: ZoneID) -> DNSRecords:
        resource_path = f"zones/{zone_id.hex}/dns_records"
        api_url_path = await self.__make_api_url(path=resource_path)
        query_params = {"type": "A"}
        request_result = await self.__make_request(
            method="GET", url=api_url_path, query_params=query_params
        )
        schema = RecordsSerializer.parse_obj(request_result["result"])
        return schema.to_value_object()

    async def update_dns_records(
        self, dtos: Collection[UpdateDNSRecordDto]
    ) -> DNSRecords:
        requests = []
        auth = await self.__make_authentication_header()
        for dto in dtos:
            resource_path = f"zones/{dto.zone_id.hex}/dns_records/{dto.id.hex}"
            api_url_path = await self.__make_api_url(path=resource_path)
            payload = UpdateRecordSerializer.parse_obj(attr.asdict(dto)).dict()
            request = httpx.Request("PUT", api_url_path, json=payload, headers=auth)
            requests.append(request)
        async with httpx.AsyncClient() as client:
            callable_requests = [client.send(request) for request in requests]
            results = await asyncio.gather(*callable_requests)
        schema = RecordsSerializer.parse_obj(
            [result.json()["result"] for result in results]
        )
        return schema.to_value_object()

    async def __make_authentication_header(self) -> dict:
        return {"Authorization": f"Bearer {self.API_TOKEN}"}

    async def __make_request(
        self,
        url: str,
        method: str,
        query_params: Optional[dict] = None,
        json_params: Optional[dict] = None,
    ) -> dict:
        msg_ = "Sending request to {}, with query_params {} and json_params {}"
        logger.debug(msg_, url, query_params, json_params)
        auth = await self.__make_authentication_header()
        request = httpx.Request(
            method, url, params=query_params, json=json_params, headers=auth
        )
        async with httpx.AsyncClient() as client:
            result = await client.send(request)
            result.raise_for_status()
        result_as_json: dict = result.json()
        logger.debug("Got response: {}", result_as_json)
        return result_as_json

    @staticmethod
    async def __make_api_url(path: str) -> str:
        return f"https://api.cloudflare.com/client/v4/{path}"
