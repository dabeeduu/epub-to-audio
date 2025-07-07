#!/bin/bash

# Start backend
cd epub_to_audio
uvicorn epub_to_audio.api:app --host 0.0.0.0 --port 8000 --workers 4 &
BACK_PID=$!
cd ..

# Start frontend
cd client
npx serve -s dist -l 3000 &
FRONT_PID=$!
cd ..

# Wait a bit to let frontend server start
sleep 10

# Open browser
xdg-open http://localhost:3000 # Linux
# open http://localhost:3000   # macOS
# start http://localhost:3000  # Windows Git Bash

# Wait for backend to exit (so this script stays alive)
wait $BACK_PID
