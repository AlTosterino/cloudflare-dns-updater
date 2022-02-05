import asyncio

import typer

from cloudflare_dns_updater.injection import build_inject
from cloudflare_dns_updater.main import main
from cloudflare_dns_updater.settings import Settings


def run_app(debug: bool = typer.Option(False, help="Show debug log messages")) -> None:
    settings = Settings(DEBUG=debug)
    build_inject(settings=settings)
    asyncio.run(main())


def run() -> None:
    typer.run(run_app)
