# Health Calculator Microservice with CI/CD Pipeline on Azure

## Overview

This project is a Python-based microservice that calculates health metrics—specifically, Body Mass Index (BMI) and Basal Metabolic Rate (BMR). It is built using Flask and designed with Pydantic for input validation. The service is containerized with Docker and run using Docker Compose. A Makefile provides convenient commands for common development tasks. A CI/CD pipeline uses GitHub Actions for automated testing and deployment to Azure App Service.

## Project Structure

```
health-calculator-service/
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # GitHub Actions workflow for CI/CD pipeline
├── templates/
│   └── index.html              # Simple HTML frontend for testing endpoints
├── .gitignore                  # Specifies intentionally untracked files that Git should ignore
├── app.py                      # Main Flask application with API endpoints (/bmi and /bmr)
├── deploy_azure_infra.sh       # Script to provision initial Azure resources
├── docker-compose.yml          # Docker Compose configuration for running the app
├── Dockerfile                  # Docker configuration for containerization
├── health_utils.py             # Utility functions for health metric calculations
├── Makefile                    # Automation script for Docker Compose tasks
├── models.py                   # Pydantic models for input validation
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies (used inside Docker)
└── test.py                     # Unit tests for BMI and BMR calculations
```

## Local Setup and Running Instructions using Makefile

1.  **Clone the Repository**
    ```bash
    git clone <your-repository-url>
    cd health-calculator-service
    ```

2.  **Prerequisites**
    * Ensure you have **Docker** and **Docker Compose** installed on your system. No local Python setup is required.

3.  **Build the Docker Image**
    Build the necessary Docker image using the Makefile:
    ```bash
    make build
    ```
    *(Note: This step is also run automatically by `make run` or `make test` if the image doesn't exist or needs updating).*

4.  **Run the Application Locally**
    Start the application using the Makefile:
    ```bash
    make run
    ```
    The application will build the image if needed and then start the service in detached mode. The API will be available at `http://localhost:5001`. You can also access a simple web interface at this address to test the endpoints visually.

5.  **Stop the Application**
    To stop the running application:
    ```bash
    make down
    ```

6.  **Testing**
    * **Run Unit Tests**: Executes tests inside a dedicated Docker container.
        ```bash
        make test
        ```
    * **Test Live Endpoints via Command Line**: Sends sample requests to the running application's endpoints (ensure the app is running with `make run` first).
        ```bash
        make test-endpoints
        ```
    * **Test Live Endpoints via Web Interface**: Access `http://localhost:5001` in your browser while the application is running (`make run`) to use the HTML forms.

7.  **Clean Up**
    Stop the application and remove associated containers, networks, and volumes:
    ```bash
    make clean
    ```

## API Endpoints

-   **GET /**
    -   Serves a simple HTML page (`templates/index.html`) that provides a user interface for making requests to the `/bmi` and `/bmr` endpoints. Access this in your browser when the service is running locally (`http://localhost:5001`).
-   **POST /bmi**
    -   Calculates Body Mass Index.
    -   **Request Body:**
        ```json
        {
          "height": 1.75,   // in meters
          "weight": 70      // in kilograms
        }
        ```
    -   **Success Response (200):**
        ```json
        {
          "bmi": 22.86
        }
        ```
    -   **Error Response (400):**
        ```json
        {
          "error": "Invalid input: <error details>"
        }
        ```
-   **POST /bmr**
    -   Calculates Basal Metabolic Rate.
    -   **Request Body:**
        ```json
        {
          "height": 175,    // in centimeters
          "weight": 70,     // in kilograms
          "age": 25,        // in years
          "gender": "male"  // "male" or "female"
        }
        ```
    -   **Success Response (200):**
        ```json
        {
          "bmr": 1665.92
        }
        ```
    -   **Error Response (400):**
        ```json
        {
          "error": "Invalid input: <error details>"
        }
        ```

## Deployment to Azure

Deployment involves two main stages: initial infrastructure setup and automated application updates via CI/CD.

1.  **Initial Azure Infrastructure Setup (One-Time Task)**
    * The `deploy_azure_infra.sh` script is provided to provision the necessary Azure resources: Resource Group, Azure Container Registry (ACR), App Service Plan, and the Web App for Containers.
    * **Prerequisites**: You need the Azure CLI installed and configured with appropriate permissions to create resources in your subscription. `jq` is also required for processing JSON output.
    * **Execution**: Run the script from your local machine:
        ```bash
        bash deploy_azure_infra.sh
        ```
    * **Output**: The script will output the names of the created resources and crucial values needed for the GitHub Actions CI/CD pipeline. These include:
        * `ACR_LOGIN_SERVER`
        * `ACR_USERNAME`
        * `ACR_PASSWORD` (one of the ACR passwords)
        * `AZURE_WEBAPP_PUBLISH_PROFILE` (XML content)

2.  **Configure GitHub Secrets**
    * In your GitHub repository settings (`Settings` > `Secrets and variables` > `Actions`), add the following repository secrets using the values obtained from the output of `deploy_azure_infra.sh`:
        * `ACR_LOGIN_SERVER`
        * `ACR_USERNAME`
        * `ACR_PASSWORD`
        * `AZURE_WEBAPP_PUBLISH_PROFILE`
    * You also need to update the `AZURE_APP_SERVICE_NAME` environment variable in the `.github/workflows/ci-cd.yml` file to match the name of the Web App created by the script (or your existing App Service name if you didn't use the script).

3.  **Automated Deployment via CI/CD**
    * The GitHub Actions workflow (`.github/workflows/ci-cd.yml`) is configured to automatically build, test, and deploy the application whenever changes are pushed to the `main` branch.
    * The workflow performs the following steps:
        * Checks out the code.
        * Sets up Python and installs dependencies (for the runner executing tests).
        * Runs unit tests.
        * Logs into Azure Container Registry using the configured secrets.
        * Builds the Docker image and tags it with the commit SHA and `latest`.
        * Pushes the tagged Docker image to ACR.
        * Deploys the newly pushed image (`:latest` tag) to the Azure App Service specified by `AZURE_APP_SERVICE_NAME` using the publish profile secret.
    * To deploy updates, simply push your code changes to the `main` branch.