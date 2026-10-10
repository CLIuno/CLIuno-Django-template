# CLIuno Django template

Django 6 + DRF + SimpleJWT REST API (uv-managed) serving the CLIuno contract: JWT auth
(verify-email gated login, refresh, reset, OTP via pyotp), users, todos, posts+comments,
follows, roles — under `/api/v1`.

## Commands

```bash
uv sync                                   # install (uv.lock committed)
uv run python manage.py migrate           # sqlite db.sqlite3
uv run python manage.py runserver         # dev server
uv run python manage.py test              # test suite — keep it green
uv run python manage.py makemigrations src  # after model changes
```

If a foreign venv is active, `unset VIRTUAL_ENV` first. `.env` is optional
(sane dev defaults); set `SECRET_KEY` in production.

## Structure

`main/` (settings/urls) → `src/urls/` (per-resource url modules) → `src/views/` →
`src/models.py` / `src/serializers/`. **URL style**: REST method dispatch via
`src/urls/dispatch.py` (`method_dispatch(GET=..., POST=...)`); collections are
no-trailing-slash — prefix `path('posts', include(...))` + inner `'/<uuid:pk>'`
(string concatenation, deliberate).

## Contract rules this codebase follows

- Responses: `{'status', 'message', 'data'}` with exact keys frontends destructure
  (`data.users/user/todos/todo/posts/post/followers/following/isFollowing`, login `data.token`).
- Request keys: camelCase (`usernameOrEmail`, `refreshToken`, `oldPassword`/`newPassword`,
  `otp`); `forgot-password` takes `email`.
- One-time tokens live on the user (`reset_token`, `verify_token`); reset/verify-email
  look users up **by token**; registration stores the verify token it emails.
- The `user` role uses `get_or_create` (fresh clone needs no seeding).
- OTP endpoints act on `request.user` (`_resolve_request_user` helper).
- `GET /users` is IsAuthenticated (not admin); `PATCH/DELETE /users/:id` are admin.

## Conventions

Conventional commits; tests live in `src/tests/` and assert the contract shapes —
update them together with any envelope change.

## AI agents (Claude Code and friends)

- **Check the CLIuno skills first**: `npx cliuno@latest skills status` — if any is
  `missing`/`outdated`, run `npx cliuno@latest skills install` (adds `.claude/skills/cliuno-*`:
  the generator workflow, the scaffold guide, and the shared REST contract).
- **Generate resources, don't hand-write them**:
  `npx cliuno@latest make:resource Product --fields name:string,price:number,inStock:boolean`
  creates `src/serializers/product_serializers.py`, `src/views/product_views.py`, `src/urls/product_urls.py`, `src/tests/test_products.py` and registers it in `src/models.py`, `src/urls/__init__.py`, following this
  template's conventions and the `{status, message, data}` contract. `--dry-run` previews,
  re-running never duplicates registrations, `--force` overwrites.
- Single pieces: `make:model`, `make:migration` (→ `uv run python`), `make:controller`, `make:validator`, `make:test`. `npx cliuno@latest make` lists them.
- Then edit fields/business logic only, and run the gates above.
