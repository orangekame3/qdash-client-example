from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
from dotenv import load_dotenv
from qdash.client import QDashApiError, QDashClient

load_dotenv()

PARAMETER = "t1"
QID: str | None = None
LOOKBACK_DAYS = 30
OUTPUT_DIR = Path("outputs")

client = QDashClient.from_env()
try:
    chip_id = client.get_default_chip_id()
    end_at_value = datetime.now(UTC)
    start_at_value = end_at_value - timedelta(days=LOOKBACK_DAYS)
    start_at = start_at_value.isoformat().replace("+00:00", "Z")
    end_at = end_at_value.isoformat().replace("+00:00", "Z")

    series = client.get_task_results_timeseries(
        chip_id=chip_id,
        parameter=PARAMETER,
        qid=QID,
        start_at=start_at,
        end_at=end_at,
    )

    point_count = sum(len(points) for points in series.data.values())
    print(f"time series: chip={chip_id} parameter={PARAMETER} points={point_count}")
    if point_count == 0:
        print("plot: skipped; no data points found")
        raise SystemExit(0)

    labels: list[str] = []
    values: list[list[float | int]] = []
    for entity_id, points in sorted(series.data.items()):
        entity_values = [point.value for point in points]
        if entity_values:
            labels.append(entity_id)
            values.append(entity_values)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.violinplot(values, showmeans=True, showmedians=True)
    ax.set_title(f"{chip_id} {PARAMETER} distribution over last {LOOKBACK_DAYS} days")
    ax.set_xlabel("qid")
    ax.set_ylabel(PARAMETER)
    ax.set_xticks(range(1, len(labels) + 1), labels, rotation=45, ha="right")
    ax.grid(True, alpha=0.3)

    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / f"{chip_id}_{PARAMETER}_violin_last_{LOOKBACK_DAYS}_days.png"
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"plot: {output_path}")
except QDashApiError as exc:
    print(f"QDash API error: status={exc.status_code} message={exc}")
    raise SystemExit(1) from exc
finally:
    client.close()
