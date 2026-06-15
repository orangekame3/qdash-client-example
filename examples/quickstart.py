from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
from dotenv import load_dotenv
from qdash.client import QDashApiError, QDashClient, QDashConfig, TimeSeriesData


# Set PARAMETER and QID to change the plotted metric.
PARAMETER = "t1"
QID: str | None = None
LOOKBACK_DAYS = 30
OUTPUT_DIR = Path("outputs")


def print_chips(client: QDashClient) -> None:
    chips = client.list_chips()
    print(f"chips: {chips.total}")
    for chip in chips.chips:
        print(f"- {chip.chip_id} ({chip.activity_status})")


def select_active_chip_id(client: QDashClient) -> str:
    chips = client.list_chips().chips
    for chip in chips:
        if str(chip.activity_status) == "active":
            return chip.chip_id
    if chips:
        return chips[0].chip_id
    raise RuntimeError("No chips found.")


def isoformat_z(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def fetch_timeseries(client: QDashClient, chip_id: str) -> TimeSeriesData:
    end_at = datetime.now(UTC)
    start_at = end_at - timedelta(days=LOOKBACK_DAYS)

    return client.get_task_results_timeseries(
        chip_id=chip_id,
        parameter=PARAMETER,
        qid=QID,
        start_at=isoformat_z(start_at),
        end_at=isoformat_z(end_at),
    )


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
    load_dotenv()

    config = QDashConfig.from_env()
    client = QDashClient(config)
    try:
        print_chips(client)
        chip_id = select_active_chip_id(client)
        series = fetch_timeseries(client, chip_id)
        plot_distribution(chip_id, series)
    finally:
        client.close()


if __name__ == "__main__":
    try:
        main()
    except QDashApiError as exc:
        print(f"QDash API error: status={exc.status_code} message={exc}")
        raise SystemExit(1) from exc
