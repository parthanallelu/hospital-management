# Hospital Management System - Makefile
# Run "make run" to start the Flask server with one command

# Windows PowerShell commands
.PHONY: run install clean help

# Default target
help:
	@echo "Available commands:"
	@echo "  make run     - Start the Flask development server"
	@echo "  make install - Install all dependencies"
	@echo "  make clean   - Clean up cache files"

# Start Flask server with virtual env and environment variables
run:
	@echo "Starting Flask server..."
	@echo "Make sure you have set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in your .env file"
	@powershell -Command ".\venv\Scripts\Activate.ps1; python run.py"

# Install dependencies
install:
	@echo "Installing dependencies..."
	@powershell -Command ".\venv\Scripts\Activate.ps1; pip install -r requirements.txt"

# Clean cache files
clean:
	@echo "Cleaning cache files..."
	@powershell -Command "Remove-Item -Recurse -Force __pycache__ -ErrorAction SilentlyContinue"
	@powershell -Command "Remove-Item -Recurse -Force app\__pycache__ -ErrorAction SilentlyContinue"
	@powershell -Command "Remove-Item -Recurse -Force app\routes\__pycache__ -ErrorAction SilentlyContinue"
