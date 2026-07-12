# Cliuno Django template

## Installation

Make sure you have Python 3.12+ and [uv](https://docs.astral.sh/uv/) installed.

To install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

If you want to run the project using docker make sure you have installed docker.

To install docker go to [docker](https://docs.docker.com/get-docker/)

To run the project using docker:

```bash
docker compose up -d
```

## Clone the repository

```bash
git clone https://github.com/CLIuno/CLIuno-Django-template.git
```

Then install dependencies:

```bash
uv sync
```

## Usage

Copy the environment file:

```bash
cp .env.example .env
```

Run migrations:

```bash
uv run python manage.py migrate
```

Create a superuser (optional):

```bash
uv run python manage.py createsuperuser
```

Start the development server:

```bash
uv run python manage.py runserver
```

## Features

List of features that are already implemented:

| Status             | Feature                       |
| ------------------ | ----------------------------- |
| :white_check_mark: | Auth routes                   |
| :white_check_mark: | User routes                   |
| :white_check_mark: | Role routes                   |
| :white_check_mark: | Post routes                   |
| :white_check_mark: | Comment routes                |
| :white_check_mark: | Todo routes                   |
| :white_check_mark: | Follow routes                 |
| :white_check_mark: | Mailer                        |
| :white_check_mark: | OTP (TOTP) support            |
| :white_check_mark: | JWT authentication            |
| :white_check_mark: | SQLite database               |
| :white_check_mark: | Dockerize                     |
| :white_check_mark: | Role-based access control     |

## List of endpoints

### Auth

| Status             | Endpoint Description    | Method | Path                             |
| ------------------ | ----------------------- | ------ | -------------------------------- |
| :white_check_mark: | Login                   | POST   | `/api/v1/auth/login`             |
| :white_check_mark: | Register                | POST   | `/api/v1/auth/register`          |
| :white_check_mark: | Logout                  | POST   | `/api/v1/auth/logout`            |
| :white_check_mark: | Reset Password          | POST   | `/api/v1/auth/reset-password`    |
| :white_check_mark: | Forgot Password         | POST   | `/api/v1/auth/forgot-password`   |
| :white_check_mark: | Change Password         | POST   | `/api/v1/auth/change-password`   |
| :white_check_mark: | Send Verification Email | POST   | `/api/v1/auth/send-verify-email` |
| :white_check_mark: | Verify Email            | POST   | `/api/v1/auth/verify-email`      |
| :white_check_mark: | Check Token             | POST   | `/api/v1/auth/check-token`       |
| :white_check_mark: | Refresh Token           | POST   | `/api/v1/auth/refresh-token`     |
| :white_check_mark: | Verify OTP              | POST   | `/api/v1/auth/otp/verify`        |
| :white_check_mark: | Disable OTP             | POST   | `/api/v1/auth/otp/disable`       |
| :white_check_mark: | Validate OTP            | POST   | `/api/v1/auth/otp/validate`      |
| :white_check_mark: | Generate OTP            | POST   | `/api/v1/auth/otp/generate`      |

### Users

| Status             | Endpoint Description | Method | Path                               |
| ------------------ | -------------------- | ------ | ---------------------------------- |
| :white_check_mark: | Get current user     | GET    | `/api/v1/users/current`            |
| :white_check_mark: | Update current user  | PATCH  | `/api/v1/users/current`            |
| :white_check_mark: | Delete current user  | DELETE | `/api/v1/users/current`            |
| :white_check_mark: | Get user by username | GET    | `/api/v1/users/username/:username` |
| :white_check_mark: | Get all users        | GET    | `/api/v1/users`                    |
| :white_check_mark: | Get a user by ID     | GET    | `/api/v1/users/:id`                |
| :white_check_mark: | Update user by ID    | PATCH  | `/api/v1/users/:id`                |
| :white_check_mark: | Delete user by ID    | DELETE | `/api/v1/users/:id`                |
| :white_check_mark: | Get posts by user    | GET    | `/api/v1/users/posts`              |
| :white_check_mark: | Get roles by user    | GET    | `/api/v1/users/role`               |

### Roles

| Status             | Endpoint Description | Method | Path                           |
| ------------------ | -------------------- | ------ | ------------------------------ |
| :white_check_mark: | Get all roles        | GET    | `/api/v1/roles`                |
| :white_check_mark: | Get role by ID       | GET    | `/api/v1/roles/:id`            |
| :white_check_mark: | Create a role        | POST   | `/api/v1/roles`                |
| :white_check_mark: | Update role by ID    | PATCH  | `/api/v1/roles/:id`            |
| :white_check_mark: | Delete role by ID    | DELETE | `/api/v1/roles/:id`            |
| :white_check_mark: | Get users by role    | GET    | `/api/v1/roles/:role_id/users` |

### Posts

| Status             | Endpoint Description       | Method | Path                                            |
| ------------------ | -------------------------- | ------ | ----------------------------------------------- |
| :white_check_mark: | Get current user posts     | GET    | `/api/v1/posts/current-user`                    |
| :white_check_mark: | Get all posts              | GET    | `/api/v1/posts`                                 |
| :white_check_mark: | Get post by ID             | GET    | `/api/v1/posts/:id`                             |
| :white_check_mark: | Create a post              | POST   | `/api/v1/posts`                                 |
| :white_check_mark: | Update post by ID          | PATCH  | `/api/v1/posts/:id`                             |
| :white_check_mark: | Delete post by ID          | DELETE | `/api/v1/posts/:id`                             |
| :white_check_mark: | Get user by post           | GET    | `/api/v1/posts/:post_id/user`                   |
| :white_check_mark: | Get comments by post       | GET    | `/api/v1/posts/:post_id/comments`               |
| :white_check_mark: | Create comment             | POST   | `/api/v1/posts/:post_id/comments`               |
| :white_check_mark: | Update comment             | PATCH  | `/api/v1/posts/:post_id/comments/:id`           |
| :white_check_mark: | Delete comment             | DELETE | `/api/v1/posts/:post_id/comments/:id`           |

### Todos

| Status             | Endpoint Description       | Method | Path                          |
| ------------------ | -------------------------- | ------ | ----------------------------- |
| :white_check_mark: | Get current user todos     | GET    | `/api/v1/todos/current-user`  |
| :white_check_mark: | Get all todos              | GET    | `/api/v1/todos`               |
| :white_check_mark: | Get todo by ID             | GET    | `/api/v1/todos/:id`           |
| :white_check_mark: | Create a todo              | POST   | `/api/v1/todos`               |
| :white_check_mark: | Update todo by ID          | PATCH  | `/api/v1/todos/:id`           |
| :white_check_mark: | Delete todo by ID          | DELETE | `/api/v1/todos/:id`           |
| :white_check_mark: | Toggle todo complete       | PATCH  | `/api/v1/todos/:id/toggle`    |

### Follows

| Status             | Endpoint Description       | Method | Path                                   |
| ------------------ | -------------------------- | ------ | -------------------------------------- |
| :white_check_mark: | Follow user                | POST   | `/api/v1/follows/:user_id/follow`      |
| :white_check_mark: | Unfollow user              | DELETE | `/api/v1/follows/:user_id/follow`      |
| :white_check_mark: | Get followers              | GET    | `/api/v1/follows/:user_id/followers`   |
| :white_check_mark: | Get following              | GET    | `/api/v1/follows/:user_id/following`   |
| :white_check_mark: | Check if following         | GET    | `/api/v1/follows/:user_id/is-following`|
