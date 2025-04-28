# ================
# File: Makefile
# ================
.PHONY: run down test build clean test-endpoints

# Build the image first (dependency for run and test)
run: build
	@echo "Running the application using Docker Compose..."
	docker-compose up -d

down:
	@echo "Stopping the application using Docker Compose..."
	docker-compose down

# Build the image before running tests in a container
test: build
	@echo "Running tests inside a Docker container..."
	docker-compose run --rm app python -m unittest discover -s . -p "test*.py"

build:
	@echo "Building the Docker image using Docker Compose..."
	docker-compose build

clean:
	@echo "Cleaning up Docker resources (optional)..."
	docker-compose down -v --remove-orphans
	docker system prune -af --volumes

test-endpoints:
	@echo "\nTesting BMI endpoint..."
	curl -X POST http://localhost:5001/bmi \
		-H "Content-Type: application/json" \
		-d '{"height": 1.75, "weight": 70}'
	@echo "\n\nTesting BMR endpoint..."
	curl -X POST http://localhost:5001/bmr \
		-H "Content-Type: application/json" \
		-d '{"height": 175, "weight": 70, "age": 30, "gender": "male"}'
	@echo "\n"