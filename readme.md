# Pathfndr - Amadeus APIs

## Stack

The application utilizes the following technologies:

- **Python 3.11 (Slim)**
- **Flask**
- **Redis**
- **Docker**

## Overview

The application provides a REST endpoint to discover the cheapest flight options between two cities. It uses the following parameters to filter flights:

- **`originCode`**: The airport code of the origin city.
- **`destinationCode`**: The airport code of the destination city.
- **`date`**: The departure date in `YYYY-MM-DD` format.
- **`no_cache`**: An optional binary flag:
  - `1`: Fetches the latest data directly from Amadeus.
  - `0`: Uses cached data from Redis.

The application provides another REST endpoint **/health** to check if server is running fine. ( health endpoint ).

Another endpoint **/flights/ping** return "**pong**" when a GET request is made.

### How It Works

1. **Data Fetching**: The application communicates with Amadeus APIs to retrieve comprehensive flight details.
2. **Caching**: Flight details are stored in Redis with a cache expiration time of 10 minutes. During this period, subsequent requests are served from the Redis cache for faster response times.
3. **Cache Refresh**: Once the cache expires, fresh data is fetched from Amadeus and the Redis cache is updated.

## Deployment

The application is fully Dockerized and can be started with a single shell command. Docker Compose handles environment variables, volume mounts, and container contexts automatically for a smooth deployment.

## Setup Steps

1. **Extract the Project:**
   - Extract the contents of the provided `.tar.gz` file.

2. **Create and Configure Environment File:**
   - Navigate to the project directory.
   - Create an `.env` file using `touch .env`.
   - Paste the environment variables provided in the email into the `.env` file.

3. **Set Up Virtual Environment:**
   - Create a virtual environment and activate it within the project directory.
   - python -m venv venv
   - source venv/bin/activate

4. **Ensure Docker is Running:**
   - Verify that Docker is running in the background.

5. **Navigate to Project Directory:**
   - Go to the project root directory and navigate to bash inside project root.

6. **Start the Project:**
   - Run the command `sh start_project.sh` to start the application, which will be served at port 8000.

7. **Reference Documentation:**
   - Consult the `README` file for additional details and GitHub repository information.

**Note** : The application uses docker compose v2 by default hence : 
docker compose will work if v1 is being used docker-compose will be only functional.
## API Collection can be found at : 

- www.google.com
