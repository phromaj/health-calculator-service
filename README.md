# Health Calculator Microservice with CI/CD Pipeline on Azure 

## Overview

This project is a Python-based microservice that calculates health metrics—specifically, Body Mass Index (BMI) and Basal Metabolic Rate (BMR). It is built using Flask and designed with Pydantic for input validation. The service is containerized with Docker and run using Docker Compose. A Makefile provides convenient commands for Docker-based tasks. A CI/CD pipeline uses GitHub Actions for automated testing and deployment to Azure App Service.

## Project Structure

```
health-calculator-service/
├── .github/workflows/ci-cd.yml # GitHub Actions workflow for CI/CD pipeline
├── .gitignore                  # Specifies intentionally untracked files that Git should ignore
├── app.py                      # Main Flask application with API endpoints (/bmi and /bmr)
├── docker-compose.yml          # Docker Compose configuration for running the app
├── Dockerfile                  # Docker configuration for containerization
├── health_utils.py             # Utility functions for health metric calculations
├── Makefile                    # Automation script for Docker Compose tasks
├── models.py                   # Pydantic models for input validation
├── requirements.txt            # Python dependencies (used inside Docker)
├── test.py                     # Unit tests for BMI and BMR calculations
└── README.md                   # Project documentation
```

## Setup and Running Instructions

1.  **Clone the Repository** 🛠️
    ```bash
    git clone [https://github.com/yourusername/health-calculator-service.git](https://github.com/yourusername/health-calculator-service.git)
    cd health-calculator-service
    ```

2.  **Prerequisites** 🐳
    * Ensure you have **Docker** and **Docker Compose** installed on your system. No local Python setup is required.

3.  **Build the Docker Image** 🏗️
    Build the necessary Docker image using Docker Compose:
    ```bash
    make build
    ```
    *(This step is also run automatically when you execute `make run` or `make test` if the image doesn't exist or needs updating).*

4.  **Run the Application Locally** 🚀
    Start the application using Docker Compose:
    ```bash
    make run
    ```
    The application will build the image if needed and then start the service. The API will be available at `http://localhost:5000`.

5.  **Stop the Application** 🛑
    To stop the running application:
    ```bash
    make down
    ```

6.  **Testing** ✅
    Run the unit tests (this will execute inside a Docker container):
    ```bash
    make test
    ```
    You can also test the running endpoints (ensure the app is running with `make run` first, then open another terminal):
    ```bash
    make test-endpoints
    ```

## API Endpoints

-   **POST /bmi**
    -   **Request Body:**
        ```json
        {
          "height": 1.75,   // in meters
          "weight": 70      // in kilograms
        }
        ```
    -   **Response:**
        ```json
        {
          "bmi": 22.86
        }
        ```
-   **POST /bmr**
    -   **Request Body:**
        ```json
        {
          "height": 175,    // in centimeters
          "weight": 70,     // in kilograms
          "age": 25,        // in years
          "gender": "male"  // "male" or "female"
        }
        ```
    -   **Response:**
        ```json
        {
          "bmr": 1665.92   // Example value, rounded to 2 decimal places
        }
        ```

## CI/CD Pipeline

A GitHub Actions workflow (`.github/workflows/ci-cd.yml`) is configured to:
-   Run on pushes to the `main` branch.
-   Set up the Python environment (for the runner).
-   Install dependencies (for the runner's test step).
-   Run unit tests.
-   Build the Docker image.
-   Deploy the container to Azure App Service using the publish profile stored in the repository secrets (`AZURE_WEBAPP_PUBLISH_PROFILE`).

## Deployment to Azure ☁️

1.  **Create an Azure App Service:**
    * Create a new Web App in the [Azure Portal](https://portal.azure.com).
2.  **Configure GitHub Secrets:**
    * Download the publish profile from the Azure App Service.
    * In your GitHub repository settings, add a secret named `AZURE_WEBAPP_PUBLISH_PROFILE` with the content of the publish profile.
3.  **Deploy:**
    * Push changes to the `main` branch. The GitHub Actions workflow will trigger and deploy the new containerized version of the microservice.

## Additional Notes

-   **Modular Design:** The project is structured with clear separation of concerns (API, models, utilities, tests).
-   **Input Validation:** Uses Pydantic to enforce strict validation rules.
-   **Containerization:** Uses Docker and Docker Compose for consistent environments and easy execution via the Makefile.
-   **Automation:** Leverages Makefiles for streamlined Docker workflows and GitHub Actions for CI/CD.

---
