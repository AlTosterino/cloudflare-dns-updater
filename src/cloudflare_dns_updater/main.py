import asyncio

from cloudflare_dns_updater.injection import build_inject
from cloudflare_dns_updater.queries import DeviceIPQuery
from cloudflare_dns_updater.queries.dns import DNSRecordsQuery
from cloudflare_dns_updater.services.dns.value_objects import ZoneID


async def main() -> None:
    # https://discuss.python.org/t/is-there-a-way-to-define-a-function-that-can-be-used-as-a-nomal-function-and-an-async-function/5262/5
    zone_id = ZoneID("457aba5ea6227a7f4d672e8845a2d5e9")
    device_ip, dns_records = await asyncio.gather(
        *[DeviceIPQuery.execute(), DNSRecordsQuery.execute(zone_id=zone_id)]
    )
    print(device_ip)
    print(dns_records)


if __name__ == "__main__":
    build_inject()
    asyncio.run(main())
