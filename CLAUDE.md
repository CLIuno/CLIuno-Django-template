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
