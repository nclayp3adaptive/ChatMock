# Docker Deployment

## Quick Start
1) Setup env:
   cp .env.example .env

2) Create the auth directory if needed:
   mkdir -p ./data

3) Login:
   docker compose run --rm --service-ports chatmock-login login

   - The command prints an auth URL, copy paste it into your browser.
   - If your browser cannot reach the container's localhost callback, copy the full redirect URL from the browser address bar and paste it back into the terminal when prompted.
   - Server should stop automatically once it receives the tokens and they are saved.

4) Start the server:
   docker compose up -d chatmock

4) Free to use it in whichever chat app you like!

By default the compose file binds only to `127.0.0.1`, so the API is private unless you intentionally put it behind a reverse proxy or SSH tunnel.
The service also joins the shared `librechat-network` so an internal nginx proxy can reach it without exposing the container broadly.

## Configuration
Set options in `.env` or pass environment variables:
- `PORT`: Container listening port (default 8000)
- `CHATMOCK_BIND_IP`: host interface to bind to (default `127.0.0.1`)
- `CHATMOCK_IMAGE`: image tag to run (default `chatmock:local`)
- `CHATMOCK_DATA_DIR`: host path mounted at `/data` and expected to contain `auth.json`
- `VERBOSE`: `true|false` to enable request/stream logs
- `CHATGPT_LOCAL_REASONING_EFFORT`: minimal|low|medium|high|xhigh
- `CHATGPT_LOCAL_REASONING_SUMMARY`: auto|concise|detailed|none
- `CHATGPT_LOCAL_REASONING_COMPAT`: legacy|o3|think-tags|current
- `CHATGPT_LOCAL_FAST_MODE`: `true|false` to enable fast mode by default for supported models
- `CHATGPT_LOCAL_CLIENT_ID`: OAuth client id override (rarely needed)
- `CHATGPT_LOCAL_EXPOSE_REASONING_MODELS`: `true|false` to add reasoning model variants to `/v1/models`
- `CHATGPT_LOCAL_ENABLE_WEB_SEARCH`: `true|false` to enable default web search tool

## Logs
Set `VERBOSE=true` to include extra logging for troubleshooting upstream or chat app requests. Please include and use these logs when submitting bug reports.

## Test

```
curl -s http://localhost:8000/v1/chat/completions \
   -H 'Content-Type: application/json' \
   -d '{"model":"gpt-5-codex","messages":[{"role":"user","content":"Hello world!"}]}' | jq .
```
