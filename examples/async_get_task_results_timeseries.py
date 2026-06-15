from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta

from dotenv import load_dotenv
from qdash.client import QDashApiError, QDashClient

load_dotenv()

PARAMETER = "t1"
QID: str | None = None
LOOKBACK_DAYS = 30

client = QDashClient.from_env()
try:
    chip_id = client.get_default_chip_id()
    end_at_value = datetime.now(UTC)
    start_at_value = end_at_value - timedelta(days=LOOKBACK_DAYS)
    start_at = start_at_value.isoformat().replace("+00:00", "Z")
    end_at = end_at_value.isoformat().replace("+00:00", "Z")

    series = asyncio.run(
        client.get_task_results_timeseries_async(
            chip_id=chip_id,
            parameter=PARAMETER,
            qid=QID,
            start_at=start_at,
            end_at=end_at,
        )
    )
    point_count = sum(len(points) for points in series.data.values())
    print(f"time series: chip={chip_id} parameter={PARAMETER} points={point_count}")
except QDashApiError as exc:
    print(f"QDash API error: status={exc.status_code} message={exc}")
    raise SystemExit(1) from exc
finally:
    client.close()
