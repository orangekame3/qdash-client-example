from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from qdash.client import QDashApiError, TimeSeriesData

from common import create_client, date_range_for_last_days, print_api_error, select_active_chip_id

PARAMETER = "t1"
QID: str | None = None
LOOKBACK_DAYS = 30
OUTPUT_DIR = Path("outputs")


def fetch_timeseries(chip_id: str) -> TimeSeriesData:
    client = create_client()
    try:
        start_at, end_at = date_range_for_last_days(LOOKBACK_DAYS)
        return client.get_task_results_timeseries(
            chip_id=chip_id,
            parameter=PARAMETER,
            qid=QID,
            start_at=start_at,
            end_at=end_at,
        )
    finally:
        client.close()


def plot_distribution(chip_id: str, series: TimeSeriesData) -> None:
    point_count = sum(len(points) for points in series.data.values())
    print(f"time series: chip={chip_id} parameter={PARAMETER} points={point_count}")
    if point_count == 0:
        print("plot: skipped; no data points found")
        return

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


def main() -> None:
    client = create_client()
    try:
        chip_id = select_active_chip_id(client)
    finally:
        client.close()

    series = fetch_timeseries(chip_id)
    plot_distribution(chip_id, series)


if __name__ == "__main__":
    try:
        main()
    except QDashApiError as exc:
        print_api_error(exc)
        raise SystemExit(1) from exc
