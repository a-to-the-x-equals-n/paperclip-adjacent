# Paperclip Adjacent

A cross-platform, retro-styled desktop task manager with a Rust-based GUI and a Flask backend. 

Designed for minimalism, portability, and local persistence.

## Table of Contents

- [Usage](#usage)
  - [Supported Commands](#supported-commands)
- [Project Snapshot](#project-snapshot)
- [Quickstart](#quickstart)
  - [1. Flask Backend (API Server)](#1-flask-backend-api-server)
  - [2. egui Frontend (Rust App)](#2-egui-frontend-rust-app)
- [Tech Stack](#tech-stack)
  - [Frontend](#frontend)
  - [Backend](#backend)
  - [Development Tools](#development-tools)
  - [Environment](#environment)
- [Project Structure](#project-structure)
- [Build and Deployment](#build-and-deployment)
- [Notes](#notes)
- [Documentation & References](#documentation--references)

## Usage

This app uses SMS-to-Email gateways to enable task management via text messages. You can send a text message to a designated email address, where a listener processes incoming messages and responds accordingly. The response is sent back as an MMS through the gateway.

### Supported Commands:

- **`del [task ID]`** - Deletes the specified task.  
- **`new [task description]`** - Creates a new task with the given description.  
- **`all`** - Returns a list of all current tasks.  
- **`help`** - Lists all available commands.

## Project Snapshot

- Frontend: `eframe` + `egui` (Rust)
- Backend: Flask (Python)
- Data Storage: TinyDB with YAML serialization wrapper
- Debugging: Custom thread-safe inspection/debug decorator
- Deployment: Jenkins and Ngrok
- CI/CD: Makefile-driven automation

## Quickstart

To replicate the app's functionality, you need to set up automated email login using a Google email account. Make sure to store this email address in the backends `.env` file (described below).

>**NOTE:** By default, the `Smtp` class in `flask_app/api/models/email` uses Verizon's SMS/MMS gateways. Replace these values with your carrier's gateway settings if you are using a different provider. 

### 1. Flask Backend (API Server)

Python 3.11 or higher is recommended.

>NOTE: *Ensure the flask server is up and running before you attempt to login, otherwise the rust login auth hangs indefinitely during rust's async/await.*  

```bash
cd flask_app
touch api/.env
# Add values for: EMAIL, PASSWORD, IP, PORT, DB_PATH, TABLE
```
>NOTE: *all of the following bash commands are to be executed from inside __flask_app/__.*  

Install dependencies via `pyproject.toml`:

```bash
pip install .
```

Run the development server:

```bash
make run
```

Optional:

```bash
make tree        # shows directory structure
make clean       # removes build artifacts
```

---

### 2. egui Frontend (Rust App)

```bash
cd egui_app
touch .env
# Add your PHONE=... value
```

>NOTE: *This is the .env file that is used for login authentication.*    

Build and run the GUI:

```bash
cargo run
```
Optional:

```bash
make tree        # shows directory structure
make clean       # removes build artifacts
```

## Tech Stack

### Frontend
- **Rust:** `eframe` + `egui` for the graphical user interface (GUI)
- **Google Fonts:** Integrated for consistent typography

### Backend
- **Python:** Flask for the backend API
- **Flask Extensions:** `flask-cors` for cross-origin requests, `python-dotenv` for environment management
- **TinyDB:** Lightweight, local JSON database with a YAML serialization wrapper
- **PyYAML:** For configuration and serialization
- **Requests:** HTTP client for internal API calls

### Development Tools
- **Makefile:** Task automation and CI/CD pipeline control
- **Jenkins:** Automated build and deployment
- **Nox:** Python test automation and environment management
- **Pytest:** Unit testing framework
- **JQ:** JSON processing for clean HTTP responses in terminal (curl)
- **Cargo:** Rust package manager and build system
- **Ngrok:** Secure tunnel for local development

### Environment
- **WSL:** Windows Subsystem for Linux for cross-platform compatibility
- **Wayland:** GUI rendering support for Rust on Linux systems

## Project Structure

```bash
.
├── egui_app/                           # Rust frontend (desktop GUI)
│   ├── Makefile                        # Build/run commands for GUI
│   ├── .env                            # Contains: PHONE=...
│   ├── Cargo.toml                      # Rust dependencies and config
│   └── src/
│       ├── main.rs                     # Entry point for GUI app
│       ├── app.rs                      # App trait implementation
│       ├── client/                     # HTTP API client logic
│       │   ├── http.rs                 # Async functions for backend requests
│       │   └── mod.rs                  
│       ├── ui/                         # GUI components and state
│       │   ├── mod.rs
│       │   └── paperclip_adjacent.rs   # Main app struct + style
│       └── utils/                      # Helper functions (env, formatting)
│           ├── auth.rs                 # .env parsing and phone formatting
│           └── mod.rs
├── flask_app/                          # Python backend API
│   ├── Makefile                        # Build/test/run utilities
│   ├── .env                            # Required: EMAIL, PASSWORD, IP, PORT, DB_PATH, TABLE
│   ├── pyproject.toml                  # Python dependency + project config
│   ├── api/
│   │   ├── __main__.py                 # Flask entry point
│   │   ├── config.py                   # Environment and app settings
│   │   ├── routes.py                   # Endpoint definitions
│   │   ├── controllers/
│   │   │   └── mailman.py              # Email logic handler
│   │   ├── models/
│   │   │   ├── db/
│   │   │   │   ├── memcell.py          # TinyDB model
│   │   │   │   ├── yamel.py            # YAML adapter
│   │   │   │   ├── ystore.py           # Storage logic
│   │   │   │   └── data/               # Database dir placeholder
│   │   │   │       └── memcells.yaml   # Database records
│   │   │   └── email/
│   │   │       ├── imap.py             # IMAP login and parsing
│   │   │       └── smtp.py             # SMTP sending logic
│   │   └── utils/
│   │       ├── debuggernaut/           # Debug decorator lib
│   │       │   ├── heimdahl.py         # Logging helper
│   │       │   └── jotunheim.py        # Stacktrace printer
│   │       ├── goodboy.py              # Misc tools
│   │       └── singleton.py            # Singleton pattern metaclass
│   └── tests/                          # Pytest test cases
│       ├── test_memcell.py
│       ├── test_routes.py
│       └── test_yamel.py
```

## Build and Deployment

- Jenkins is used for CI pipeline and build automation
- Ngrok is used to expose local Flask server endpoints
- Makefiles support commands for both development and cleanup

## Notes

- Text entry capped at 160 characters per memcell
- App runs fully offline and does not require internet for core features

## Documentation & References

### Rust
- [Egui Demo Library (GitHub)](https://github.com/emilk/egui/tree/master/crates/egui_demo_lib/src/demo)
- [Egui Official Site](https://www.egui.rs/)
- [Eframe Documentation](https://docs.rs/eframe/latest/eframe/)

### Python
- [TinyDB Documentation](https://tinydb.readthedocs.io/en/latest/)
- [Flask Documentation](https://flask.palletsprojects.com/en/stable/)
- [Nox Documentation](https://nox.thea.codes/en/stable/)
- [Pytest Documentation](https://docs.pytest.org/en/stable/contents.html)