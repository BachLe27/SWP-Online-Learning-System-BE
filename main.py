from fastapi import FastAPI

from api.v1 import app as api_v1_app

app = FastAPI()

app.mount("/api/v1", api_v1_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="localhost", port=8000, debug=True, reload=True)
