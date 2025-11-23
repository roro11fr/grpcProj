# 🌦️ Weather Forecast Platform – gRPC + FastAPI Gateway

This project is a **distributed weather forecasting system** built with **Python**, featuring:
- A **gRPC microservice** that fetches and stores real weather data.
- A **FastAPI Gateway** that exposes simple REST endpoints to the frontend or external clients.
- A **MongoDB database** used for persisting recent weather readings and historical data.

## 🚀 Architecture Overview

### 🔹 1. Weather gRPC Microservice
Located in: `services/weather/`

**Responsibilities:**
- Handles incoming gRPC requests from the Gateway.
- Fetches current weather data from the **OpenWeatherMap API**.
- Persists each reading into MongoDB (through its repository layer).
- Returns structured weather data (`city`, `temp_c`, `description`, `humidity`, `wind_speed`).

**Main technologies:**
- `grpcio`, `grpcio-tools`
- `httpx` (async HTTP client)
- `protobuf` (for defining service contracts)

Example gRPC call flow:
```
Gateway → gRPC Stub → WeatherServiceImpl → OpenWeatherClient → OpenWeatherMap API
```

### 🔹 2. FastAPI Gateway
Located in: `gateway/`

**Responsibilities:**
- Provides REST endpoints that communicate with the gRPC service.
- Handles response formatting for frontend consumption.
- Optionally reads weather history directly from MongoDB.

**Main endpoints:**
| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/api/health` | GET | Health check (returns `{status: "ok"}`) |
| `/api/weather?city=London` | GET | Fetch current weather for the given city |
| `/api/recent?city=London&limit=10` | GET | Retrieve recent saved readings |
| `/api/history?city=London&from=...&to=...` | GET | Retrieve aggregated history (hourly/minute buckets) |

### 🔹 3. Database
- **MongoDB 7.x** (containerized via Docker Compose)
- Collections store raw weather readings.
- Historical endpoints aggregate data with Mongo pipelines.

## 🧱 Project Structure
```
grpcProj/
│
├─ gateway/
│  ├─ application/app.py
│  ├─ routes/
│  ├─ services/
│  └─ core/
│
├─ services/
│  └─ weather/
│     ├─ interfaces/grpc/
│     ├─ infrastructure/
│     ├─ domain/repositories/
│     └─ core/
│
├─ docker-compose.yml
├─ requirements.txt
├─ pytest.ini
└─ tests/
```

## ⚙️ Setup & Run
### 1️⃣ Environment variables
```
OPENWEATHER_API_KEY=your_api_key_here
MONGO_URL=mongodb://mongo:27017
```
### 2️⃣ Run with Docker Compose
```
docker compose up --build
```
Starts:
- `weather-grpc` (gRPC server)
- `weather-gateway` (FastAPI app)
- `weather-mongo` (MongoDB)

### 3️⃣ Access
- Gateway → http://localhost:8080/api/weather?city=London
- gRPC → port 50052


## 📦 Tech Stack
| Layer | Technology |
|-------|-------------|
| API Gateway | FastAPI |
| gRPC Service | Python (grpcio, protobuf) |
| Data Source | OpenWeatherMap API |
| Database | MongoDB |
| Async Engine | asyncio + httpx + Motor |
| Testing | pytest, pytest-asyncio, coverage |

## 📘 License
MIT License © 2025 Robert Franciuc
Developed as part of a Data Engineering learning path demonstrating gRPC + FastAPI + MongoDB.
