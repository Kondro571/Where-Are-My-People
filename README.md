# Where Are My People

A Django REST API for managing devices (`Device`), assigning them to users (`User`), and logging their locations (`Location`).


## Setup

1. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
2. **Install required libraries:**
   ```bash
    pip install -r requirements.txt
   ```

3. **Make migrations and create a superuser:**

   ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    ```
4. **Run the server:**

   ```bash
    python manage.py runserver
    ```
5. **Access Django Admin:**

    http://localhost:8000/admin/

## API Endpoints

| Method | Endpoint                              | Description                                                    |
|--------|---------------------------------------|----------------------------------------------------------------|
| GET    | `/devices/`                           | List all devices with assignment status                        |
| POST   | `/devices/<device_id>/assign/`        | Assign a device to a user (requires `user_id` in JSON payload) |
| POST   | `/devices/<device_id>/unassign/`      | Unassign the device from its user                              |
| POST   | `/devices/<device_id>/location/`      | Report location (`latitude`, `longitude`, `ping_time`)         |
| GET    | `/users/<user_id>/location/`          | Get the last known location of a user                          |
| GET    | `/map/`                               | List locations of active devices (filterable by `user_id`, `device_type`) |


## Notes

- Device creation is done manually via Django Admin. There is no public POST endpoint for creating devices.

- The API uses Django's built-in User model (AbstractUser).

## If I had more time, I would...

- Add full CRUD endpoints for devices and users (e.g. POST /devices/)

- Add a custom user model

- Implement token-based authentication (e.g. JWT)

- Add automatic API documentation (e.g. Swagger or Redoc)

- Add better comments to explain how the code works.
