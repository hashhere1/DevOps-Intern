# Tasks Performed on 24th July

- Added a logging middleware.py file. This file defines a custom middleware for **FastAPI** to log details of every
  incoming HTTP request.
---
#### Purpose

- To log request information such as:
  - Client IP address
  - HTTP method (GET, POST, etc.)
  - Request path (URL endpoint)
  - Timestamp

- Logs are written to a file named `requests.log`.

---
#### How It Works (Brief)

1. A middleware class `LoggingMiddleware` is created.
2. For every incoming request:
   - It logs the client's IP, method, path, and timestamp.
   - Writes this info to a `requests.log` file.
3. Then it forwards the request to the intended route.

- Used to track who accessed what and when.
---
#### Output
- 2025-07-24 14:32:19 - IP: 127.0.0.1 | Method: GET | Path: /api/products
- 2025-07-24 14:33:02 - IP: 127.0.0.1 | Method: POST | Path: /api/login
- 2025-07-24 14:34:45 - IP: 192.168.1.10 | Method: DELETE | Path: /api/users/5
---
# Wrote Test Cases

- Wrote test cases for:
  -  Authentication routes
  -  Inventory routes
  - Category routes
- Created a separate `test_db` using **SQLite (in-memory)** for isolated testing.


