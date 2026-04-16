from fastapi import FastAPI


app = FastAPI()


@app.get("/health", tags=["health"], include_in_schema=False)
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
