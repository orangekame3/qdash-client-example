from __future__ import annotations

from dotenv import load_dotenv
from qdash.client import QDashApiError, QDashClient

load_dotenv()

client = QDashClient.from_env()
try:
    chips = client.list_chips()
    print(f"chips: {chips.total}")
    for chip in chips.chips:
        print(f"- {chip.chip_id} ({chip.activity_status})")
except QDashApiError as exc:
    print(f"QDash API error: status={exc.status_code} message={exc}")
    raise SystemExit(1) from exc
finally:
    client.close()
