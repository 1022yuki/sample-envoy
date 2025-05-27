from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.get("/token_exchange/{rest:path}")
async def token_exchange(_: Request, rest: str):
    new_token = "Bearer NEW_TOKEN_123"

    print(f"Received request for path: /{rest}")

    return Response(
        headers={
            "Authorization": new_token,
        },
    )
