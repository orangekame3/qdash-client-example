from __future__ import annotations

import asyncio

from qdash.client import QDashApiError

from common import create_client, print_api_error


async def main() -> None:
    client = create_client()
    try:
        chips = await client.list_chips_async()
        print(f"chips: {chips.total}")
        for chip in chips.chips:
            print(f"- {chip.chip_id} ({chip.activity_status})")
    finally:
        client.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except QDashApiError as exc:
        print_api_error(exc)
        raise SystemExit(1) from exc
