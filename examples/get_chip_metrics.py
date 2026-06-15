from __future__ import annotations

from dotenv import load_dotenv
from qdash.client import QDashApiError, QDashClient

load_dotenv()

client = QDashClient.from_env()
try:
    chip_id = client.get_default_chip_id()
    metrics = client.get_chip_metrics(chip_id)
    print(f"chip: {metrics.chip_id}")
    print(f"qubit metric groups: {len(metrics.qubit_metrics)}")
    print(f"coupling metric groups: {len(metrics.coupling_metrics)}")
    for metric_name, values in sorted(metrics.qubit_metrics.items())[:5]:
        entity_ids = ", ".join(sorted(values.keys())[:5])
        print(f"- {metric_name}: {entity_ids}")
except QDashApiError as exc:
    print(f"QDash API error: status={exc.status_code} message={exc}")
    raise SystemExit(1) from exc
finally:
    client.close()
