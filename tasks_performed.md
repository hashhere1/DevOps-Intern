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
    - Authentication routes
    - Inventory routes
    - Category routes
- Created a separate `test_db` using **SQLite (in-memory)** for isolated testing.

---

# Date - Monday, July 28, 2025

---

## Testing Setup for FastAPI Inventory Management System

### Environment Setup

- Switched testing database from **PostgreSQL** to **SQLite**.
- Used environment variable `ENV=testing` to distinguish testing mode from production.

### Database Configuration

- Updated `database.py`:
    - Configured dynamic `DATABASE_URL` based on environment variable.
    - Added conditional `connect_args` for SQLite.
    - Disabled auto-creation of tables (`Base.metadata.create_all`) unless not in testing mode.

### Test Configuration

- Created a reusable `db()` fixture using SQLite in `conftest.py`.
- Used `TestingSessionLocal` to avoid interfering with main database.
- Populated test database with:
    - Categories
    - Suppliers
    - Users
    - Products
    - Sales
- Cleaned up test database after test module finishes.

### GitHub Actions CI

- Configured `main.yml` to:
    - Checkout code
    - Set up Python 3.10
    - Install dependencies via `requirements.txt`
    - Set `ENV=testing` and run tests using `pytest`

---

## Outcome

- Successfully isolated test environment using SQLite.
- Ensured PostgreSQL production database is untouched during testing.
- Set up automated tests on GitHub Actions using the testing database.

---

# Date - 29th July

# Week 1 – Day 1: IP Addressing Basics

## What I Learned

- Networking is how devices communicate over local or global networks.
- An **IP address** is a unique number assigned to each device to identify it on a network.
- There are two types of IP addresses:
    - **Private IP**: Used within local networks (e.g., `192.168.x.x`)
    - **Public IP**: Used to communicate with the internet (e.g., `103.x.x.x`)
- The same public IP can be shared by multiple devices using **NAT** (Network Address Translation).
- A **loopback IP (127.0.0.1)** refers to the local machine.
- I found my:
    - **Private IP** using the `ip a` command on Linux
    - **Public IP** using `curl ifconfig.me` or visiting `https://ifconfig.me`

## Practical Commands I Used

- `ip a` — to list all network interfaces and find the local IP
- `curl ifconfig.me` — to get my public IP from the terminal

## Key Takeaways

- **Private IP** is used inside your home or office network.
- **Public IP** is what websites and external services see when you connect to the internet.
- Tools like `curl`, `ip`, and browser-based sites help retrieve this info quickly.
- Knowing your IP addresses is essential for debugging, firewall setup, and Docker/Kubernetes networking later on.

# Week 1 – Day 2: OSI Model (7 Layers of Networking)

## What I Learned

The **OSI (Open Systems Interconnection)** model helps explain how data moves from my computer to another over a
network. It has **7 layers**, each responsible for a specific function in the communication process.

---

## The 7 Layers of the OSI Model

| Layer | Name         | Description                                          |
|-------|--------------|------------------------------------------------------|
| 7     | Application  | Interfaces like FastAPI, browsers, DNS, HTTP         |
| 6     | Presentation | Encoding, encryption, compression (e.g. SSL/TLS)     |
| 5     | Session      | Starts/stops communication sessions                  |
| 4     | Transport    | Breaks data into packets (TCP/UDP), ensures delivery |
| 3     | Network      | Routing and addressing (IP, routers)                 |
| 2     | Data Link    | MAC addressing, error detection                      |
| 1     | Physical     | Cables, Wi-Fi signals, hardware transmission         |

---

## Real Example: FastAPI Request

When I open `http://127.0.0.1:8000/items` in the browser:

- **Application Layer** handles the HTTP request to FastAPI
- **Transport Layer** splits the data into packets (TCP)
- **Network Layer** routes the request to the right IP
- **Physical Layer** sends data via Wi-Fi or cable

---

## Why This Is Useful in DevOps

| Layer | What I Can Troubleshoot            |
|-------|------------------------------------|
| 7     | App errors, broken API URLs        |
| 4     | Blocked ports (e.g., TCP 8000)     |
| 3     | Wrong IP, DNS issues, no routing   |
| 1     | Cable unplugged, Wi-Fi not working |

---

##  Practical Command Used

```bash
ping google.com






