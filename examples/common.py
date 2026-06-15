from __future__ import annotations

from datetime import UTC, datetime, timedelta

from dotenv import load_dotenv
from qdash.client import QDashApiError, QDashClient, QDashConfig


def create_client() -> QDashClient:
    load_dotenv()
    return QDashClient(QDashConfig.from_env())


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


def date_range_for_last_days(days: int) -> tuple[str, str]:
    end_at = datetime.now(UTC)
    start_at = end_at - timedelta(days=days)
    return isoformat_z(start_at), isoformat_z(end_at)


def print_api_error(exc: QDashApiError) -> None:
    print(f"QDash API error: status={exc.status_code} message={exc}")
