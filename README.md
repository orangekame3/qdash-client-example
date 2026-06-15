# qdash-client-example

Small uv-managed examples for using `qdash-client` from Python scripts.

## Setup

Install dependencies with uv.

```bash
uv sync
```

Create a local environment file.

```bash
cp .env.example .env
```

Edit `.env` with your QDash API endpoint and token.

`QDASH_BASE_URL` must point to the API base URL. For local development this is usually
`http://localhost:5715`. If your deployment exposes the API under a prefix, include it in the
value, such as `https://your-qdash-instance/api`.

## Examples

Run the quickstart first. It lists chips, selects an active chip, fetches the last 30 days of
`t1`, and saves a violin plot under `outputs/`.

```bash
uv run python examples/quickstart.py
```

Each public `QDashClient` method also has a small script.

```bash
uv run python examples/list_chips.py
uv run python examples/get_chip_metrics.py
uv run python examples/get_metrics_config.py
uv run python examples/get_task_results_timeseries.py
uv run python examples/normalize_chip_metrics.py
uv run python examples/async_list_chips.py
uv run python examples/async_get_metrics_config.py
uv run python examples/async_get_task_results_timeseries.py
```

Change the plotted metric by editing the constants at the top of
`examples/get_task_results_timeseries.py`.

```python
PARAMETER = "t1"
QID = "Q00"
LOOKBACK_DAYS = 30
```

## Required Environment

`qdash-client` reads these values:

- `QDASH_BASE_URL`
- `QDASH_API_TOKEN`
- `QDASH_PROJECT_ID` if your QDash instance uses project-scoped access
- `QDASH_CF_ACCESS_CLIENT_ID` and `QDASH_CF_ACCESS_CLIENT_SECRET` if QDash is behind Cloudflare Access
