# File: Makefile

# Variables
FRONTEND_DIR=client
BACKEND_DIR=epub_to_audio

.PHONY: build-frontend build-backend build-all run-backend run-frontend run-all

# Build frontend once
build-frontend:
	cd ${FRONTEND_DIR} && npm install && npm run build

build-backend:
	cd ${BACKEND_DIR} && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Start backend only
run-backend:
	cd ${BACKEND_DIR} && uvicorn epub_to_audio.api:app --host 0.0.0.0 --port 8000 --workers 4

# Serve frontend only (no build)
serve-frontend:
	cd ${FRONTEND_DIR} && npx serve -s dist -l 3000

# Run both (assuming already built)
run-all:
	cd ${BACKEND_DIR} && uvicorn epub_to_audio.api:app --host 0.0.0.0 --port 8000 --workers 4 & \
	cd ${FRONTEND_DIR} && npx serve -s dist -l 3000

# Run both and rebuild frontend
build-and-run-all: build-frontend build-backend run-all

