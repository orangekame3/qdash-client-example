from __future__ import annotations

from dotenv import load_dotenv
from qdash.client import QDashApiError, QDashClient

load_dotenv()

client = QDashClient.from_env()
try:
    config = client.get_metrics_config()
    print(f"top-level keys: {', '.join(sorted(config.keys()))}")
    for key, value in sorted(config.items())[:5]:
        print(f"- {key}: {type(value).__name__}")
except QDashApiError as exc:
    print(f"QDash API error: status={exc.status_code} message={exc}")
    raise SystemExit(1) from exc
finally:
    client.close()
