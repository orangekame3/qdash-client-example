from __future__ import annotations

import asyncio

from dotenv import load_dotenv
from qdash.client import QDashApiError, QDashClient

load_dotenv()

client = QDashClient.from_env()
try:
    chips = asyncio.run(client.list_chips_async())
    print(f"chips: {chips.total}")
    for chip in chips.chips:
        print(f"- {chip.chip_id} ({chip.activity_status})")
except QDashApiError as exc:
    print(f"QDash API error: status={exc.status_code} message={exc}")
    raise SystemExit(1) from exc
finally:
    client.close()
