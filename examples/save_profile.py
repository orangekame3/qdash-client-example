from __future__ import annotations

from qdash.client import QDashConfig, QDashConfigError

PROFILE = "local"
BASE_URL = "http://localhost:5715"
API_TOKEN = "your-api-token"
PROJECT_ID = None
CF_ACCESS_CLIENT_ID = None
CF_ACCESS_CLIENT_SECRET = None

try:
    config = QDashConfig(
        base_url=BASE_URL,
        api_token=API_TOKEN,
        project_id=PROJECT_ID,
        cf_access_client_id=CF_ACCESS_CLIENT_ID,
        cf_access_client_secret=CF_ACCESS_CLIENT_SECRET,
    )
    saved_path = config.save(profile=PROFILE)
    print(f"profile: {PROFILE}")
    print(f"saved: {saved_path}")
except QDashConfigError as exc:
    print(f"QDash config error: {exc}")
    raise SystemExit(1) from exc
