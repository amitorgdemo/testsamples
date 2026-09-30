import uvicorn
from app.api import create_app

app = create_app()

if __name__ == "__main__":
    # Launch local application deployment server with auto-reload activated
    uvicorn.run("main.py:app", host="127.0.0.1", port=8000, reload=True)
