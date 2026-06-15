from __future__ import annotations

import asyncio

from qdash.client import QDashApiError

from common import create_client, print_api_error


async def main() -> None:
    client = create_client()
    try:
        config = await client.get_metrics_config_async()
        print(f"top-level keys: {', '.join(sorted(config.keys()))}")
    finally:
        client.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except QDashApiError as exc:
        print_api_error(exc)
        raise SystemExit(1) from exc
