from __future__ import annotations

from qdash.client import QDashApiError

from common import create_client, print_api_error


def main() -> None:
    client = create_client()
    try:
        chips = client.list_chips()
        print(f"chips: {chips.total}")
        for chip in chips.chips:
            print(f"- {chip.chip_id} ({chip.activity_status})")
    finally:
        client.close()


if __name__ == "__main__":
    try:
        main()
    except QDashApiError as exc:
        print_api_error(exc)
        raise SystemExit(1) from exc
