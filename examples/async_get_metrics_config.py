from __future__ import annotations

import asyncio

from dotenv import load_dotenv
from qdash.client import QDashApiError, QDashClient

load_dotenv()

client = QDashClient.from_env()
try:
    config = asyncio.run(client.get_metrics_config_async())
    print(f"top-level keys: {', '.join(sorted(config.keys()))}")
except QDashApiError as exc:
    print(f"QDash API error: status={exc.status_code} message={exc}")
    raise SystemExit(1) from exc
finally:
    client.close()
