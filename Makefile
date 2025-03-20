.PHONY: init run test build clean test-endpoints

init:
	@echo "Setting up virtual environment..."
	python -m venv .venv
	@echo "\nTo activate the virtual environment and install requirements:"
	@echo "- For Fish shell:    source .venv/bin/activate.fish"
	@echo "- For Windows:       .venv\\Scripts\\activate"
	@echo "- For Bash/Zsh:      source .venv/bin/activate"
	@echo "\nAfter activation, run:"
	@echo "pip install --upgrade pip"
	@echo "pip install -r requirements.txt"

run:
	@echo "Running the Flask app..."
	flask run --host=0.0.0.0 --port=9898

test:
	@echo "Running tests..."
	python -m unittest discover -s . -p "test*.py"

build:
	@echo "Building the Docker image..."
	docker build -t health-calculator-service .

clean:
	@echo "Cleaning up..."
	rm -rf __pycache__

test-endpoints:
	@echo "Testing BMI endpoint..."
	curl -X POST http://localhost:9898/bmi \
		-H "Content-Type: application/json" \
		-d '{"height": 1.75, "weight": 70}'
	@echo "\n\nTesting BMR endpoint..."
	curl -X POST http://localhost:9898/bmr \
		-H "Content-Type: application/json" \
		-d '{"height": 175, "weight": 70, "age": 30, "gender": "male"}'
