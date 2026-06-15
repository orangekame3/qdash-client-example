from __future__ import annotations

from qdash.client import QDashApiError

from common import create_client, print_api_error


def main() -> None:
    client = create_client()
    try:
        config = client.get_metrics_config()
        print(f"top-level keys: {', '.join(sorted(config.keys()))}")
        for key, value in sorted(config.items())[:5]:
            print(f"- {key}: {type(value).__name__}")
    finally:
        client.close()


if __name__ == "__main__":
    try:
        main()
    except QDashApiError as exc:
        print_api_error(exc)
        raise SystemExit(1) from exc
