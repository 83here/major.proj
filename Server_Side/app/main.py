import threading
from app.live_data import simulate_data
import uvicorn

if __name__ == "__main__":
    # Start background thread to simulate or ingest live data
    data_thread = threading.Thread(target=simulate_data, daemon=True)
    data_thread.start()

    # Run FastAPI server
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
