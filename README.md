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

## Run

List chips, select an active chip, fetch the last 30 days of `t1`, and save a violin plot under
`outputs/`.

```bash
uv run python examples/quickstart.py
```

Change the plotted metric by editing the constants at the top of `examples/quickstart.py`.

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
