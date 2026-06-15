from __future__ import annotations

from qdash.client import QDashApiError, QDashClient, QDashConfig, QDashConfigError

from common import print_api_error

PROFILE = "local"


def main() -> None:
    config = QDashConfig.from_file(profile=PROFILE)
    client = QDashClient(config)
    try:
        chips = client.list_chips()
        print(f"profile: {PROFILE}")
        print(f"base_url: {config.base_url}")
        print(f"chips: {chips.total}")
        for chip in chips.chips:
            print(f"- {chip.chip_id} ({chip.activity_status})")
    finally:
        client.close()


if __name__ == "__main__":
    try:
        main()
    except QDashConfigError as exc:
        print(f"QDash config error: {exc}")
        print(
            "hint: run examples/save_profile.py first, or create "
            "~/.config/qdash/config.ini from qdash_config.ini.example."
        )
        raise SystemExit(1) from exc
    except QDashApiError as exc:
        print_api_error(exc)
        raise SystemExit(1) from exc
