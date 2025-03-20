# Health Calculator Microservice with CI/CD Pipeline on Azure

## Overview

This project is a Python-based microservice that calculates health metrics—specifically, Body Mass Index (BMI) and Basal Metabolic Rate (BMR). It is built using Flask and is designed with a modular approach using Pydantic for input validation. The service is containerized with Docker, orchestrated with a Makefile, and a CI/CD pipeline is configured using GitHub Actions for automated testing and deployment to Azure App Service.

## Project Structure

\`\`\`
health-calculator-service/
├── app.py                      # Main Flask application with API endpoints (/bmi and /bmr)
├── health_utils.py             # Utility functions for health metric calculations
├── models.py                   # Pydantic models for input validation
├── Dockerfile                  # Docker configuration for containerization
├── Makefile                    # Automation script for setup, testing, running, and building
├── requirements.txt            # Python dependencies
├── test.py                     # Unit tests for BMI and BMR calculations
├── .github/workflows/ci-cd.yml # GitHub Actions workflow for CI/CD pipeline
└── README.md                   # Project documentation
\`\`\`

## Setup Instructions

1. **Clone the Repository**

   \`\`\`bash
   git clone https://github.com/yourusername/health-calculator-service.git
   cd health-calculator-service
   \`\`\`

2. **Install Dependencies**

   Use the provided Makefile command:
   
   \`\`\`bash
   make init
   \`\`\`

3. **Run the Application Locally**

   Start the Flask application by running:
   
   \`\`\`bash
   make run
   \`\`\`
   
   The API will be available at \`http://localhost:5000\`.

4. **Testing**

   Run the unit tests to ensure everything is working:
   
   \`\`\`bash
   make test
   \`\`\`

5. **Docker Build**

   Build the Docker image using:
   
   \`\`\`bash
   make build
   \`\`\`

## API Endpoints

- **POST /bmi**

  - **Request Body:**
    \`\`\`json
    {
      "height": 1.75,   // in meters
      "weight": 70      // in kilograms
    }
    \`\`\`
  - **Response:**
    \`\`\`json
    {
      "bmi": 22.86
    }
    \`\`\`

- **POST /bmr**

  - **Request Body:**
    \`\`\`json
    {
      "height": 175,    // in centimeters
      "weight": 70,     // in kilograms
      "age": 25,
      "gender": "male"
    }
    \`\`\`
  - **Response:**
    \`\`\`json
    {
      "bmr": 1665.92   // Example value, rounded to 2 decimal places
    }
    \`\`\`

## CI/CD Pipeline

A GitHub Actions workflow (\`.github/workflows/ci-cd.yml\`) is configured to:
- Run on pushes to the \`main\` branch.
- Set up the Python environment.
- Install dependencies.
- Run unit tests.
- Build the Docker image.
- Deploy the container to Azure App Service using the publish profile stored in the repository secrets (\`AZURE_WEBAPP_PUBLISH_PROFILE\`).

## Deployment to Azure

1. **Create an Azure App Service:**
   - Create a new Web App in the [Azure Portal](https://portal.azure.com).

2. **Configure GitHub Secrets:**
   - Download the publish profile from the Azure App Service.
   - In your GitHub repository settings, add a secret named \`AZURE_WEBAPP_PUBLISH_PROFILE\` with the content of the publish profile.

3. **Deploy:**
   - Push changes to the \`main\` branch. The GitHub Actions workflow will trigger and deploy the new containerized version of the microservice.

## Additional Notes

- **Modular Design:** The project is structured with clear separation of concerns (API, models, utilities, tests).
- **Input Validation:** Uses Pydantic to enforce strict validation rules.
- **Best Practices:** Follows best practices for Docker containerization, CI/CD automation, and Python coding standards.

---

Happy coding!
