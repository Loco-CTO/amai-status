import uvicorn
import config
from main import app

if __name__ == "__main__":
    try:
        _, _, server_config = config.load_config()
        host = server_config.get("host", "0.0.0.0")
        port = server_config.get("port", 8182)
    except Exception as e:
        print(f"Warning: Could not load config: {e}")
        host = "0.0.0.0"
        port = 8182

    print(f"Starting 甘い Status API on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
