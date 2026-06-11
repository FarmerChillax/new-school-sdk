# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`new-school-sdk` (PyPI: `school-sdk`) is a Python SDK for the ZFSoft (正方) university academic management system. It automates login (including CAPTCHA solving) and retrieves timetables, grades, and personal info via web scraping.

## Commands

```bash
# Install dependencies
uv sync              # all deps including dev
uv sync --no-dev     # runtime only

# Run the manual integration test (requires .env with SCHOOL_HOST, SCHOOL_ACCOUNT, SCHOOL_PASSWORD)
cd test && python test.py

# Format code
autopep8 --in-place --recursive school_sdk/

# Build package
uv build

# Documentation (local preview)
uv run --with mkdocs-material mkdocs serve
```

There is no pytest or automated test suite — only `test/test.py`, which is a manual integration test against a live school system.

## Architecture

### Two-client model

```
SchoolClient(host, captcha_type, ...)   ← school-level config + factory
    └── .user_login(account, password)
            └── UserClient              ← per-user session (wraps requests.Session)
                    ├── .get_schedule(year, term)
                    ├── .get_score(year, term)
                    └── .get_info()
```

`SchoolClient` is imported from `school_sdk/__init__.py` along with `UserClient`, `CAPTCHA`, and `KCAPTCHA`.

### Inheritance

`BaseUserClient` (HTTP helpers) ← `UserClient` (public API methods)

`BaseCrawler` (shared HTTP helpers) ← `ZFLogin`, `Schedule`, `Score`, `Info`

Both `BaseUserClient` and `BaseCrawler` expose `.get()` / `.post()` / `._request()` that auto-prepend `BASE_URL` to relative paths.

### Login flow (`client/api/login.py`)

1. GET login page → extract CSRF token
2. GET public key endpoint → RSA modulus + exponent
3. Optionally solve CAPTCHA:
   - **Slider** (`CAPTCHA`): pixel-column heuristic scan → simulated mouse track → POST to `/zfcaptchaLogin`
   - **Image** (`KCAPTCHA`): CNN inference via `check_code/` → 6-char alphanumeric code
4. POST credentials with RSA-encrypted password using the pure-Python `PyRsa/` module (port of jsbn)

### CAPTCHA recognition (`school_sdk/check_code/`)

- `ZFCaptchaDistinguish` wraps both CAPTCHA types
- Image captcha uses a 3-conv-layer CNN (`model.py`) with pre-trained weights in `model.pkl` (~39 MB binary committed to git), requiring PyTorch + torchvision
- Slider captcha uses a heuristic in `type.py`

### URL endpoint configuration

All API paths are defined in `school_sdk/config.py` as a `URL_ENDPOINT` dict. Every `SchoolClient` instance can override individual paths, making the SDK portable across different ZFSoft deployments with different URL prefixes.

### Term encoding

`TERM = {1: 3, 2: 12, 3: 16}` maps human-readable term numbers to ZFSoft internal codes.

## Known stubs and WIP

- `school_sdk/session/` — `RedisStorage` defined but not implemented
- `client/api/check.py` — stub class, no implementation
- `client/api/class_schedule.py` — WIP, contains hardcoded test data and writes debug JSON to disk
