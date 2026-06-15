from __future__ import annotations

import asyncio

from qdash.client import QDashApiError

from common import create_client, date_range_for_last_days, print_api_error, select_active_chip_id

PARAMETER = "t1"
QID: str | None = None
LOOKBACK_DAYS = 30


async def main() -> None:
    client = create_client()
    try:
        chip_id = select_active_chip_id(client)
        start_at, end_at = date_range_for_last_days(LOOKBACK_DAYS)
        series = await client.get_task_results_timeseries_async(
            chip_id=chip_id,
            parameter=PARAMETER,
            qid=QID,
            start_at=start_at,
            end_at=end_at,
        )
        point_count = sum(len(points) for points in series.data.values())
        print(f"time series: chip={chip_id} parameter={PARAMETER} points={point_count}")
    finally:
        client.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except QDashApiError as exc:
        print_api_error(exc)
        raise SystemExit(1) from exc
