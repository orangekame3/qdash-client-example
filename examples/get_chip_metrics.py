from __future__ import annotations

from dotenv import load_dotenv
from qdash.client import QDashApiError, QDashClient, QDashConfig

load_dotenv()

client = QDashClient(QDashConfig.from_env())
try:
    chips = client.list_chips().chips
    chip_id = None
    for chip in chips:
        if str(chip.activity_status) == "active":
            chip_id = chip.chip_id
            break
    if chip_id is None and chips:
        chip_id = chips[0].chip_id
    if chip_id is None:
        raise RuntimeError("No chips found.")

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
