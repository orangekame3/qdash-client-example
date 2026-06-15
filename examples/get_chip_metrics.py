from __future__ import annotations

from qdash.client import QDashApiError

from common import create_client, print_api_error, select_active_chip_id


def main() -> None:
    client = create_client()
    try:
        chip_id = select_active_chip_id(client)
        metrics = client.get_chip_metrics(chip_id)
        print(f"chip: {metrics.chip_id}")
        print(f"qubit metric groups: {len(metrics.qubit_metrics)}")
        print(f"coupling metric groups: {len(metrics.coupling_metrics)}")
        for metric_name, values in sorted(metrics.qubit_metrics.items())[:5]:
            entity_ids = ", ".join(sorted(values.keys())[:5])
            print(f"- {metric_name}: {entity_ids}")
    finally:
        client.close()


if __name__ == "__main__":
    try:
        main()
    except QDashApiError as exc:
        print_api_error(exc)
        raise SystemExit(1) from exc
