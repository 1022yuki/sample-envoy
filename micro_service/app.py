from fastapi import FastAPI

app = FastAPI()

@app.get("/{path:path}")
async def dummy(path: str):
    return {"micro_service": "ok", "path": f"/{path}"}
