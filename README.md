# Car Ratings API

This project provides an API for managing car ratings using FastAPI and MySQL.

## Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

Ensure you have the following installed on your system:

- Docker & Docker Compose
- Python 3.8 or later
- `pip` (Python package installer)

### Installation and Setup

1. **Start Docker Containers:**

   First, start the MySQL database container using Docker Compose:<br>
   `docker-compose up`

2. **Install Python Dependencies:**

   Install the required Python packages:<br>
   `pip install -r requirements.txt`

3. **Run the API:**

   Finally, start the FastAPI application:<br>
   `uvicorn app.main:app --reload`

4. **Run tests:**

   Run tests:<br>
   `pytest test\test_api.py`
