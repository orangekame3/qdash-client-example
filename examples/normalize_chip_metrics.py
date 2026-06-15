from __future__ import annotations

from qdash.client import QDashClient, QDashConfig


def main() -> None:
    client = QDashClient(QDashConfig(base_url="http://example.invalid", api_token="example-token"))
    records = client.normalize_chip_metrics(
        "example-chip",
        {
            "qubit_metrics": [
                {
                    "qubit_id": "Q00",
                    "metrics": {
                        "t1": {
                            "value": 23.4,
                            "unit": "us",
                            "observed_at": "2026-06-15T00:00:00Z",
                        }
                    },
                }
            ],
            "coupling_metrics": [
                {
                    "entity_id": "Q00-Q01",
                    "metric_name": "cz_error",
                    "value": 0.012,
                    "observed_at": "2026-06-15T00:00:00Z",
                }
            ],
        },
    )

    for record in records:
        print(record)


if __name__ == "__main__":
    main()
