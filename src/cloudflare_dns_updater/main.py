import asyncio

from cloudflare_dns_updater.injection import build_inject
from cloudflare_dns_updater.use_cases import GettingDeviceIP


async def main() -> None:
    # https://discuss.python.org/t/is-there-a-way-to-define-a-function-that-can-be-used-as-a-nomal-function-and-an-async-function/5262/5
    await GettingDeviceIP().execute()


if __name__ == "__main__":
    build_inject()
    asyncio.run(main())
