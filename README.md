# Flask User Management API

A Flask-based API for managing users, including authentication, CRUD operations, and file uploads.

## Features

- **User Authentication**: Token-based authentication with role-based access control.
- **CRUD Operations**: Create, read, update, delete, and patch user data.
- **Pagination**: Fetch users with pagination support.
- **File Uploads**: Upload and retrieve user avatars.
- **Secure JWT Handling**: Token expiry and validation mechanisms.

## Endpoints

### User Management

- `GET /user/` - Fetch all users (requires authentication).
- `POST /user/add` - Add a new user (requires authentication).
- `PUT /user/update` - Update an existing user (requires authentication).
- `DELETE /user/delete/<id>` - Delete a user by ID (requires authentication).
- `PATCH /user/patch/<id>` - Update specific user fields (requires authentication).

### Pagination

- `GET /user/getall/limit/<limit>/page/<page>` - Fetch users with pagination (requires authentication).

### File Uploads

- `PUT /user/<id>/uploadAvatar` - Upload an avatar for a user (requires authentication).
- `GET /uploads/<fileName>` - Retrieve an uploaded avatar (requires authentication).

### Authentication

- `POST /user/login` - Login and receive a JWT token.

## Setup

- Configure the database in config/config.py

1. Clone the repository:
   ```bash
   git clone <repo-url>
   ```

## Run the app:

```bash
flask run

```
